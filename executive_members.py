from flask import Flask, render_template, jsonify, flash, request

from app import (
    app,
    db,
    Members,
    Meetings,
    Memberships,
    Surveys,
    get_payment_status,
    AnnualReports,
    Activities,
    News,
    Banners,
    Quotes,
    Pages,
    TaskRepartitionTexts,
    TaskRepartitionFiles,
    save_file,
    delete_file,
    get_background,
    AddRegister,
    UpdateRegister,
    DeleteRegister,
)
from webforms import MemberForm

from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import uuid as uuid
import os


REGISTER_TYPE = "Executive Member"
S3_FOLDER = "images/member_pics/"
TEMPLATE_FOLDER = "executive_members"


class AddRegisterMember(AddRegister):
    def checkIfExists(self):
        self.register = Members.query.filter_by(
            email=self.request.form["email"]
        ).first()
        return self.register

    def createRegister(self):
        self.register = Members()
        hashed_pw = generate_password_hash(
            self.form.password_hash.data, method="pbkdf2:sha256"
        )
        self.register = Members()
        self.register.name = self.request.form["name"]
        self.register.role = self.request.form["role"]
        self.register.roleFR = self.request.form["roleFR"]
        self.register.email = self.request.form["email"]
        self.register.bioEN = self.request.form["bioEN"]
        self.register.bioFR = self.request.form["bioFR"]
        self.register.telephone = self.request.form["telephone"]
        if "english" in self.request.form:
            self.register.english = bool(self.request.form["english"])
        if "french" in self.request.form:
            self.register.french = bool(self.request.form["french"])
        self.register.preferable = self.request.form["preferable"]
        self.register.organizationEN = self.request.form["organizationEN"]
        self.register.organizationFR = self.request.form["organizationFR"]
        self.register.category = "Executive Member"
        self.register.volunteers = self.request.form["volunteers"]
        self.register.member_pic = self.unique_filename
        self.register.password_hash = hashed_pw


class UpdateRegisterMember(UpdateRegister):
    def updateRegister(self):
        self.register.name = self.form.name.data
        self.register.email = self.form.email.data
        self.register.bioEN = self.form.bioEN.data
        self.register.bioFR = self.form.bioFR.data
        self.register.english = self.form.english.data
        self.register.french = self.form.french.data
        self.register.preferable = self.form.preferable.data
        self.register.role = self.form.role.data
        self.register.roleFR = self.form.roleFR.data
        self.register.order = self.form.order.data
        self.register.telephone = self.form.telephone.data
        self.register.organizationEN = self.form.organizationEN.data
        self.register.organizationFR = self.form.organizationFR.data
        if self.request.files["member_pic"]:
            self.register.member_pic = self.unique_filename


@app.route("/executive_member_area/")
def executive_member_area():
    form = MemberForm()
    executive_member = Members.query.filter_by(
        id=app.config["CURRENT_USER_ID"]
    ).first()
    task_repartitionText = TaskRepartitionTexts.query.filter_by(id=1).first()
    task_repartition_files = TaskRepartitionFiles.query.order_by(
        TaskRepartitionFiles.filename
    )
    our_executive_members = Members.query.filter_by(category="Executive Member").order_by(Members.name)
    our_members = Members.query.filter_by(category="Member").order_by(Members.name)
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
            "roleFR": member.roleFR,
            "organizationEN": member.organizationEN,
            "organizationFR": member.organizationFR,
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
    title = Pages.query.filter_by(url="/title").first()
    subtitle = Pages.query.filter_by(url="/subtitle").first()
    buttons = [
        {"name": "My Info", "nameFR": "Mes informations", "link": "#myInfo"},
        {"name": "Task Repartition", "nameFR": "Task Repartition", "link": "#taskRepartition"},
        {"name": "Payment Status", "nameFR": "Statut du paiement", "link": "#paymentList"},
        {"name": "Member Attendance", "nameFR": "Présence des membres", "link": "#attendanceList"},
        {"name": "Surveys", "nameFR": "Enquêtes", "link": "#surveysList"},
        {"name": "Meetings", "nameFR": "Réunions", "link": "#meetings_list"},
        {"name": "Executive Members", "nameFR": "Membres exécutifs", "link": "#executive_member_list"},
        {"name": "Members", "nameFR": "Membres", "link": "#member_list"},
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
        title_member="Members",
        member_payments=member_payments,
        deletable=True,
        form=form,
        s3_root=app.config["S3_ROOT"],
        background=get_background(),
        title=title,
        subtitle=subtitle,
    )


@app.route("/add_executive_member", methods=["GET", "POST"])
def add_executive_member():
    print('ADD EXECUTIVE MEMBER')
    form = MemberForm()
    form_fields = [
        form.name,
        form.role,
        form.roleFR,
        form.email,
        form.bioEN,
        form.bioFR,
        form.telephone,
        form.english,
        form.french,
        form.preferable,
        form.organizationEN,
        form.organizationFR,
        form.volunteers,
        form.member_pic,
        form.password_hash,
    ]

    addRegister = AddRegisterMember(
        request,
        form,
        REGISTER_TYPE,
        S3_FOLDER,
        form_fields,
        TEMPLATE_FOLDER,
        "member_pic",
    )
    return addRegister.returnTemplate()


@app.route("/update_executive_member/<int:id>", methods=["GET", "POST"])
def update_executive_member(id):
    deletable = request.args.get("deletable")
    form = MemberForm()
    register = Members.query.get_or_404(id)
    form_fields = [
        form.name.data,
        form.email.data,
        form.bioEN.data,
        form.bioFR.data,
        form.english.data,
        form.french.data,
        form.role.data,
        form.roleFR.data,
        form.order.data,
        form.telephone.data,
        form.organizationEN.data,
        form.organizationFR.data,
        form.member_pic,
        form.password_hash,
    ]

    updateRegister = UpdateRegisterMember(
        request,
        register,
        form,
        REGISTER_TYPE,
        S3_FOLDER,
        TEMPLATE_FOLDER,
        "member_pic",
        deletable=deletable,
    )
    return updateRegister.returnTemplate()


@app.route("/delete_executive_member/<int:id>", methods=["GET", "POST"])
def delete_executive_member(id):
    form = MemberForm()
    register = Members.query.get_or_404(id)

    deleteRegister = DeleteRegister(
        register,
        form,
        REGISTER_TYPE,
        S3_FOLDER,
        TEMPLATE_FOLDER,
        "member_pic",
    )
    return deleteRegister.returnTemplate()


@app.route("/update_executive_password/<int:id>", methods=["GET", "POST"])
def update_executive_password(id):
    form = MemberForm()
    executive_member_to_update = Members.query.get_or_404(id)
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
    activities = Activities.query.order_by(Activities.titleEN)
    news = News.query.order_by(News.title)
    annualReports = AnnualReports.query.order_by(AnnualReports.filename)
    banners = Banners.query.order_by(Banners.filename)
    quotes = Quotes.query.order_by(Quotes.title)
    pages = Pages.query.order_by(Pages.url)
    title = Pages.query.filter_by(url="/title").first()
    subtitle = Pages.query.filter_by(url="/subtitle").first()
    buttons = [
        {"name": "Activities", "nameFR": "Activités", "link": "#activities"},
        {"name": "News", "nameFR": "Nouvelles", "link": "#news"},
        {"name": "Annual Reports", "nameFR": "Rapports annuels", "link": "#annualReports"},
        {"name": "Banners", "nameFR": "Bannières", "link": "#banners"},
        {"name": "Quotes", "nameFR": "Citations", "link": "#quotes"},
    ]
    return render_template(
        "content/content_management.html",
        activities=activities,
        news=news,
        annualReports=annualReports,
        banners=banners,
        quotes=quotes,
        pages=pages,
        buttons=buttons,
        s3_root=app.config["S3_ROOT"],
        background=get_background(),
        title=title,
        subtitle=subtitle,
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
