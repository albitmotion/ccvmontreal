from flask import Flask, render_template, jsonify, flash, request

from app import (
    app,
    db,
    Members,
    ExecutiveMembers,
    Meetings,
    Memberships,
    Surveys,
    get_payment_status,
    AnnualReports,
    Activities,
    News,
    Banners,
    Quotes,
    TaskRepartitionTexts,
    TaskRepartitionFiles,
    save_file,
    delete_file,
    get_background,
    AddRegister,
    UpdateRegister,
    DeleteRegister,
)
from webforms import ExecutiveMemberForm

from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import uuid as uuid
import os


REGISTER_TYPE = "Executive Member"
S3_FOLDER = "images/executive_member_pics/"
TEMPLATE_FOLDER = "executive_members"


class AddRegisterExecutiveMember(AddRegister):
    def checkIfExists(self):
        self.register = ExecutiveMembers.query.filter_by(
            email=self.request.form["email"]
        ).first()
        return self.register

    def createRegister(self):
        self.register = ExecutiveMembers()
        hashed_pw = generate_password_hash(
            self.form.password_hash.data, method="pbkdf2:sha256"
        )
        self.register = ExecutiveMembers()
        self.register.name = self.request.form["name"]
        self.register.email = self.request.form["email"]
        self.register.bio = self.request.form["bio"]
        self.register.role = self.request.form["role"]
        self.register.order = self.request.form["order"]
        self.register.telephone = self.request.form["telephone"]
        if "english" in self.request.form:
            self.register.english = bool(self.request.form["english"])
        else:
            self.register.english = 0
        if "french" in self.request.form:
            self.register.french = bool(self.request.form["french"])
        else:
            self.register.french = 0
        self.register.preferable = self.request.form["preferable"]
        self.register.organization = self.request.form["organization"]
        self.register.executive_member_pic = self.unique_filename
        self.register.password_hash = hashed_pw


class UpdateRegisterExecutiveMember(UpdateRegister):
    def updateRegister(self):
        self.register.name = self.form.name.data
        self.register.email = self.form.email.data
        self.register.bio = self.form.bio.data
        self.register.english = self.form.english.data
        self.register.french = self.form.french.data
        self.register.preferable = self.form.preferable.data
        self.register.role = self.form.role.data
        self.register.order = self.form.order.data
        self.register.telephone = self.form.telephone.data
        self.register.organization = self.form.organization.data
        if self.request.files["executive_member_pic"]:
            self.register.executive_member_pic = self.unique_filename


@app.route("/executive_member_area/")
def executive_member_area():
    form = ExecutiveMemberForm()
    executive_member = ExecutiveMembers.query.filter_by(
        id=app.config["CURRENT_USER_ID"]
    ).first()
    task_repartitionText = TaskRepartitionTexts.query.filter_by(id=1).first()
    task_repartition_files = TaskRepartitionFiles.query.order_by(
        TaskRepartitionFiles.filename
    )
    our_executive_members = ExecutiveMembers.query.order_by(ExecutiveMembers.name)
    our_members = Members.query.order_by(Members.name)
    surveys = Surveys.query.order_by(Surveys.title)
    meetings = Meetings.query.order_by(Meetings.date)

    member_payments = []
    for member in our_members:
        memberships = Memberships.query.filter_by(id=member.id).order_by(
            Memberships.start
        )
        first_membership = (
            Memberships.query.filter_by(member_id=member.id)
            .order_by(Memberships.end)
            .first()
        )
        last_membership = (
            Memberships.query.filter_by(member_id=member.id)
            .order_by(Memberships.end.desc())
            .first()
        )
        payment_status = get_payment_status(last_membership)
        member_since = ""
        if first_membership:
            member_since = first_membership.start
        meeetings_attendee = []
        if memberships:
            try:
                for meeting in member.meetings_attendance:
                    meeetings_attendee.append(meeting.date)
            except:
                pass
        perc = 0
        meetings_active = []
        for meeting in meetings:
            if member_since:
                if meeting.date >= member_since:
                    meetings_active.append(meeting.date)
        if meetings_active:
            perc = int((100 * len(member.meetings_attendance)) / len(meetings_active))

        member_payment = {
            "id": member.id,
            "name": member.name,
            "role": member.role,
            "organization": member.organization,
            "status": payment_status["status"],
            "warning_icon": payment_status["warning_icon"],
            "remembered": payment_status["remembered"],
            "member_since": member_since,
            "expiration_date": payment_status["expiration_date"],
            "member_pic": member.member_pic,
            "meeetings_attendee": meeetings_attendee,
            "meetings_active": meetings_active,
            "perc": perc,
        }
        member_payment["memberships"] = memberships
        member_payments.append(member_payment)
    buttons = [
        {"name": "My Info", "link": "#myInfo"},
        {"name": "Task Repartition", "link": "#taskRepartition"},
        {"name": "Payment Status", "link": "#paymentList"},
        {"name": "Member Attendance", "link": "#attendanceList"},
        {"name": "Surveys", "link": "#surveysList"},
        {"name": "Meetings", "link": "#meetings_list"},
        {"name": "Executive Members", "link": "#executive_member_list"},
        {"name": "Members", "link": "#member_list"},
    ]
    return render_template(
        "executive_members/executive_member_area.html",
        executive_member=executive_member,
        task_repartitionText=task_repartitionText,
        task_repartition_files=task_repartition_files,
        our_members=our_members,
        our_executive_members=our_executive_members,
        is_executive_member=True,
        buttons=buttons,
        surveys=surveys,
        meetings=meetings,
        title="Members",
        member_payments=member_payments,
        deletable=True,
        form=form,
        s3_root=app.config["S3_ROOT"],
        background=get_background(),
    )


@app.route("/add_executive_member", methods=["GET", "POST"])
def add_executive_member():
    form = ExecutiveMemberForm()
    form_fields = [
        form.name,
        form.email,
        form.bio,
        form.english,
        form.french,
        form.role,
        form.order,
        form.telephone,
        form.organization,
        form.executive_member_pic,
        form.password_hash,
    ]

    addRegister = AddRegisterExecutiveMember(
        request,
        form,
        REGISTER_TYPE,
        S3_FOLDER,
        form_fields,
        TEMPLATE_FOLDER,
        "executive_member_pic",
    )
    return addRegister.returnTemplate()
    # name = None
    # form = ExecutiveMemberForm()
    # if form.validate_on_submit():
    #     user = ExecutiveMembers.query.filter_by(email=form.email.data).first()
    #     unique_filename = ""
    #     # Save file name to database
    #     if user is None:
    #         if request.files["executive_member_pic"].filename:
    #             # Upload Image
    #             unique_filename = save_file(
    #                 form.executive_member_pic.data, "images/executive_member_pics/"
    #             )
    #         hashed_pw = generate_password_hash(
    #             form.password_hash.data, method="pbkdf2:sha256"
    #         )
    #         executiveMember = ExecutiveMembers(
    #             name=form.name.data,
    #             email=form.email.data,
    #             bio=form.bio.data,
    #             english=form.english.data,
    #             french=form.french.data,
    #             role=form.role.data,
    #             order=form.order.data,
    #             telephone=form.telephone.data,
    #             organization=form.organization.data,
    #             executive_member_pic=unique_filename,
    #             password_hash=hashed_pw,
    #         )
    #         db.session.add(executiveMember)
    #         db.session.commit()
    #         flash(
    #             "Executive Member <strong>%s</strong> added successfully!"
    #             % form.name.data
    #         )
    # our_executive_members = ExecutiveMembers.query.order_by(ExecutiveMembers.name)
    # return render_template(
    #     "executive_members/add_executive_member.html",
    #     form=form,
    #     name=name,
    #     our_executive_members=our_executive_members,
    # )


@app.route("/update_executive_member/<int:id>", methods=["GET", "POST"])
def update_executive_member(id):
    form = ExecutiveMemberForm()
    register = ExecutiveMembers.query.get_or_404(id)
    form_fields = [
        form.name.data,
        form.email.data,
        form.bio.data,
        form.english.data,
        form.french.data,
        form.role.data,
        form.order.data,
        form.telephone.data,
        form.organization.data,
        form.executive_member_pic,
        form.password_hash,
    ]

    updateRegister = UpdateRegisterExecutiveMember(
        request,
        register,
        form,
        REGISTER_TYPE,
        S3_FOLDER,
        TEMPLATE_FOLDER,
        "executive_member_pic",
    )
    return updateRegister.returnTemplate()
    # executive_member_to_update = ExecutiveMembers.query.get_or_404(id)
    # if request.method == "POST":
    #     executive_member_to_update.name = request.form["name"]
    #     executive_member_to_update.role = request.form["role"]
    #     executive_member_to_update.bio = request.form["bio"]
    #     executive_member_to_update.email = request.form["email"]
    #     executive_member_to_update.telephone = request.form["telephone"]
    #     executive_member_to_update.order = request.form["order"]
    #     executive_member_to_update.english = form.english.data
    #     executive_member_to_update.french = form.french.data
    #     # executive_member_to_update.preferable = form.preferable.data
    #     executive_member_to_update.organization = request.form["organization"]
    #
    #     # Save file name to database
    #     if request.files["executive_member_pic"]:
    #         if executive_member_to_update.executive_member_pic:
    #             delete_file(
    #                 "images/executive_member_pics/"
    #                 + executive_member_to_update.executive_member_pic
    #             )
    #         unique_filename = save_file(
    #             form.executive_member_pic.data, "images/executive_member_pics/"
    #         )
    #         executive_member_to_update.executive_member_pic = unique_filename
    #
    #     try:
    #         db.session.commit()
    #         flash(
    #             "Executive Member <strong>%s</strong> updated successfully!"
    #             % executive_member_to_update.name
    #         )
    #         return render_template(
    #             "executive_members/update_executive_member.html",
    #             form=form,
    #             executive_member_to_update=executive_member_to_update,
    #             deletable=True,
    #         )
    #     except:
    #         flash("Error")
    #         return render_template(
    #             "executive_members/update_executive_member.html",
    #             form=form,
    #             executive_member_to_update=executive_member_to_update,
    #             deletable=True,
    #         )
    # else:
    #     return render_template(
    #         "executive_members/update_executive_member.html",
    #         form=form,
    #         executive_member_to_update=executive_member_to_update,
    #         deletable=True,
    #         s3_root=app.config["S3_ROOT"],
    #     )


@app.route("/delete_executive_member/<int:id>", methods=["GET", "POST"])
def delete_executive_member(id):
    form = ExecutiveMemberForm()
    register = ExecutiveMembers.query.get_or_404(id)

    deleteRegister = DeleteRegister(
        register,
        form,
        REGISTER_TYPE,
        S3_FOLDER,
        TEMPLATE_FOLDER,
        "executive_member_pic",
    )
    return deleteRegister.returnTemplate()
    # name = None
    #
    # try:
    #     db.session.delete(executive_member_to_delete)
    #     db.session.commit()
    #
    #     if executive_member_to_delete.executive_member_pic:
    #         delete_file(
    #             "images/executive_member_pics/"
    #             + executive_member_to_delete.executive_member_pic
    #         )
    #
    #     flash(
    #         "Executive Member <strong>%s</strong> deleted successfully!"
    #         % executive_member_to_delete.name
    #     )
    #
    #     name = executive_member_to_delete.name
    #
    #     return render_template(
    #         "executive_members/update_executive_member.html",
    #         form=form,
    #         name=name,
    #         executive_member_to_update=executive_member_to_delete,
    #     )
    # except:
    #     return render_template(
    #         "executive_members/update_executive_member.html",
    #         form=form,
    #         name=name,
    #         executive_member_to_update=executive_member_to_delete,
    #     )


@app.route("/update_executive_password/<int:id>", methods=["GET", "POST"])
def update_executive_password(id):
    form = ExecutiveMemberForm()
    executive_member_to_update = ExecutiveMembers.query.get_or_404(id)
    if request.method == "POST":
        hashed_pw = generate_password_hash(
            form.password_hash.data, method="pbkdf2:sha256"
        )
        executive_member_to_update.password_hash = hashed_pw
        try:
            db.session.commit()
            flash(
                "Executive Member <strong>%s</strong> password updated successfully!"
                % executive_member_to_update.name
            )
            return render_template(
                "executive_members/update_executive_member.html",
                form=form,
                register_to_update=executive_member_to_update,
                deletable=True,
                s3_root=app.config["S3_ROOT"],
            )
        except:
            flash("Error")
            return render_template(
                "executive_members/update_executive_member.html",
                form=form,
                register_to_update=executive_member_to_update,
                deletable=True,
                s3_root=app.config["S3_ROOT"],
            )
    else:
        return render_template(
            "executive_members/update_password.html",
            form=form,
            register_to_update=executive_member_to_update,
            deletable=True,
            s3_root=app.config["S3_ROOT"],
        )


@app.route("/content_management")
def content_management():
    activities = Activities.query.order_by(Activities.title)
    news = News.query.order_by(News.title)
    annualReports = AnnualReports.query.order_by(AnnualReports.filename)
    banners = Banners.query.order_by(Banners.filename)
    quotes = Quotes.query.order_by(Quotes.title)
    buttons = [
        {"name": "Activities", "link": "#activities"},
        {"name": "News", "link": "#news"},
        {"name": "Annual Reports", "link": "#annualReports"},
        {"name": "Banners", "link": "#banners"},
        {"name": "Quotes", "link": "#quotes"},
    ]
    return render_template(
        "content/content_management.html",
        activities=activities,
        news=news,
        annualReports=annualReports,
        banners=banners,
        quotes=quotes,
        buttons=buttons,
        s3_root=app.config["S3_ROOT"],
        background=get_background(),
    )


@app.route("/update_meeting_attendance/<int:id>", methods=["GET", "POST"])
def update_meeting_attendance(id):
    meeting = Meetings.query.filter_by(id=id).first()
    members = Members.query.order_by(Members.name)
    return render_template(
        "executive_members/update_meeting_attendance.html",
        meeting=meeting,
        members=members,
        s3_root=app.config["S3_ROOT"],
    )


@app.route("/update_member_attendance/<int:id>", methods=["GET", "POST"])
def update_member_attendance(id):
    member = Members.query.filter_by(id=id).first()
    meetings = Meetings.query.order_by(Meetings.date)

    memberships = Memberships.query.filter_by(id=member.id).order_by(Memberships.start)
    first_membership = (
        Memberships.query.filter_by(member_id=member.id)
        .order_by(Memberships.end)
        .first()
    )
    last_membership = (
        Memberships.query.filter_by(member_id=member.id)
        .order_by(Memberships.end.desc())
        .first()
    )
    payment_status = get_payment_status(last_membership)
    member_since = ""
    member_to = ""

    if first_membership:
        member_since = first_membership.start
    if last_membership:
        member_to = last_membership.end
    meetings_active = []
    for meeting in meetings:
        if meeting.date >= member_since:
            meetings_active.append(meeting)
    perc = int((100 * len(member.meetings_attendance)) / len(meetings_active))

    return render_template(
        "executive_members/update_member_attendance.html",
        meetings=meetings,
        member=member,
        member_since=member_since,
        member_to=member_to,
        perc=perc,
    )
