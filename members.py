from flask import Flask, render_template, jsonify, flash, request

from app import (
    app,
    db,
    Members,
    Meetings,
    Memberships,
    save_file,
    delete_file,
    AddRegister,
    UpdateRegister,
    DeleteRegister,
)
from webforms import MemberForm

from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import uuid as uuid
import os

REGISTER_TYPE = "Member"
S3_FOLDER = "images/member_pics/"
TEMPLATE_FOLDER = "members"


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
        self.register.email = self.request.form["email"]
        self.register.telephone = self.request.form["telephone"]
        if "english" in self.request.form:
            self.register.english = bool(self.request.form["english"])
        if "french" in self.request.form:
            self.register.french = bool(self.request.form["french"])
        self.register.preferable = self.request.form["preferable"]
        self.register.organization = self.request.form["organization"]
        self.register.volunteers = self.request.form["volunteers"]
        self.register.member_pic = self.unique_filename
        self.register.password_hash = hashed_pw


class UpdateRegisterMember(UpdateRegister):
    def updateRegister(self):
        self.register.name = self.form.name.data
        self.register.role = self.form.role.data
        self.register.email = self.form.email.data
        self.register.telephone = self.form.telephone.data
        self.register.organization = self.form.organization.data
        self.register.volunteers = self.form.volunteers.data
        self.register.english = self.form.english.data
        self.register.french = self.form.french.data
        self.register.preferable = self.form.preferable.data
        if self.request.files["member_pic"]:
            self.register.member_pic = self.unique_filename

class DeleteRegisterMember(DeleteRegister):
    def deleteDependencies(self):
        member_id = self.register.id
        memberships = Memberships.query.filter_by(member_id=member_id).all()
        for membership in memberships:
            delete_file(self.s3_folder + self.register.member_pic)
            db.session.delete(membership)
            db.session.commit()


@app.route("/member_area/")
def member_area():
    form = MemberForm()
    id = app.config["CURRENT_USER_ID"]

    our_members = Members.query.order_by(Members.name)
    meetings = Meetings.query.order_by(Meetings.date)
    member = Members.query.filter_by(id=id).first()
    memberships = Memberships.query.filter_by(member_id=id)
    first_membership = (
        Memberships.query.filter_by(member_id=id).order_by(Memberships.end).first()
    )
    last_membership = (
        Memberships.query.filter_by(member_id=id)
        .order_by(Memberships.end.desc())
        .first()
    )
    buttons = [
        {"name": "My Info", "anchor": "myInfo"},
        {"name": "My Membership", "anchor": "myMembership"},
        {"name": "Meetings", "anchor": "meetings_list"},
        {"name": "Contact Other Members", "anchor": "member_list"},
    ]
    return render_template(
        "members/member_area.html",
        our_members=our_members,
        executive_member=False,
        buttons=buttons,
        meetings=meetings,
        member=member,
        form=form,
        Memberships=memberships,
        first_membership=first_membership,
        last_membership=last_membership,
        deletable=False,
        title="Contact Other Members",
        s3_root=app.config["S3_ROOT"],
    )


@app.route("/add_member", methods=["GET", "POST"])
def add_member():
    form = MemberForm()
    form_fields = [
        form.name,
        form.role,
        form.email,
        form.telephone,
        form.english,
        form.french,
        form.preferable,
        form.organization,
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


@app.route("/update_member/<int:id>", methods=["GET", "POST"])
def update_member(id):
    form = MemberForm()
    register = Members.query.get_or_404(id)
    form_fields = [
        form.name,
        form.role,
        form.email,
        form.telephone,
        form.english,
        form.french,
        form.preferable,
        form.organization,
        form.volunteers,
        form.member_pic,
        form.password_hash,
    ]

    updateRegister = UpdateRegisterMember(
        request, register, form, REGISTER_TYPE, S3_FOLDER, TEMPLATE_FOLDER, "member_pic"
    )
    return updateRegister.returnTemplate()


@app.route("/delete_member/<int:id>", methods=["GET", "POST"])
def delete_member(id):
    register = Members.query.get_or_404(id)
    form = MemberForm()
    register_type = "Member"
    s3_folder = "images/member_pics/"
    template_folder = "members"

    deleteRegister = DeleteRegisterMember(
        register, form, REGISTER_TYPE, S3_FOLDER, TEMPLATE_FOLDER, "member_pic"
    )
    return deleteRegister.returnTemplate()


@app.route("/update_member_password/<int:id>", methods=["GET", "POST"])
def update_member_password(id):
    form = MemberForm()
    member_to_update = Members.query.get_or_404(id)
    if request.method == "POST":
        hashed_pw = generate_password_hash(
            form.password_hash.data, method="pbkdf2:sha256"
        )
        member_to_update.password_hash = hashed_pw
        try:
            db.session.commit()
            flash("Member password updated successfully!")
            return render_template(
                "members/update_member.html",
                form=form,
                register_to_update=member_to_update,
                s3_root=app.config["S3_ROOT"],
            )
        except:
            flash("Error: It was not possible to update this user password.")
            return render_template(
                "members/update_member.html",
                form=form,
                register_to_update=member_to_update,
                s3_root=app.config["S3_ROOT"],
            )
    else:
        return render_template(
            "members/update_password.html",
            form=form,
            register_to_update=member_to_update,
            s3_root=app.config["S3_ROOT"],
        )


@app.route("/view_member/<int:id>")
def view_member(id):
    member = Members.query.get_or_404(id)
    return render_template(
        "members/view_member.html",
        member=member,
        s3_root=app.config["S3_ROOT"],
    )
