from flask import Flask, render_template, jsonify, flash, request
from app import (
    app,
    db,
    Members,
    Meetings,
    Memberships,
    get_payment_status,
    AddRegister,
    UpdateRegister,
    DeleteRegister,
)
from webforms import MembershipForm

from werkzeug.utils import secure_filename
import uuid as uuid
import os

REGISTER_TYPE = "Membership"
S3_FOLDER = "docs/memberships/"
TEMPLATE_FOLDER = "memberships"


class AddRegisterMembership(AddRegister):
    def checkIfExists(self):
        self.register = Memberships.query.filter_by(
            member_id=self.member_id, start=self.request.form["start"]
        ).first()
        return self.register

    def createRegister(self):
        self.register = Memberships()
        self.register.file = self.unique_filename
        self.register.name = self.request.files["file"].filename
        self.register.start = self.request.form["start"]
        self.register.end = self.request.form["end"]
        self.register.member_id = self.member_id


class UpdateRegisterMembership(UpdateRegister):
    def updateRegister(self):
        self.register.start = self.form.start.data
        self.register.end = self.form.end.data
        self.register.remembered = self.form.remembered.data


@app.route("/add_membership/<int:member_id>", methods=["GET", "POST"])
def add_membership(member_id):
    form = MembershipForm()
    form_fields = [form.start, form.end, form.remembered, form.file]

    addRegister = AddRegisterMembership(
        request,
        form,
        REGISTER_TYPE,
        S3_FOLDER,
        form_fields,
        TEMPLATE_FOLDER,
        "file",
        member_id,
    )
    return addRegister.returnTemplate()


@app.route("/update_memberships/<int:id>")
def update_memberships(id):
    member = Members.query.filter_by(id=id).first()
    first_membership = (
        Memberships.query.filter_by(member_id=id).order_by(Memberships.end).first()
    )
    last_membership = (
        Memberships.query.filter_by(member_id=id)
        .order_by(Memberships.end.desc())
        .first()
    )
    memberships = Memberships.query.filter_by(member_id=id)
    payment_status = get_payment_status(last_membership)
    return render_template(
        "/memberships/update_memberships.html",
        member=member,
        first_membership=first_membership,
        last_membership=last_membership,
        memberships=memberships,
    )


@app.route("/update_membership/<int:id>", methods=["GET", "POST"])
def update_membership(id):
    form = MembershipForm()
    register = Memberships.query.get_or_404(id)

    updateRegister = UpdateRegisterMembership(
        request, register, form, REGISTER_TYPE, S3_FOLDER, TEMPLATE_FOLDER
    )
    return updateRegister.returnTemplate()

    # form = MembershipForm()
    # membership = Memberships.query.filter_by(id=id).first()
    # member = Members.query.filter_by(id=membership.member_id).first()
    # if form.validate_on_submit():
    #     membership.start = form.start.data
    #     membership.end = form.end.data
    #     membership.remembered = form.remembered.data
    #     db.session.commit()
    #     flash("Membership updated successfully!")
    # return render_template(
    #     "/memberships/update_membership.html",
    #     form=form,
    #     member=member,
    #     membership=membership,
    # )


@app.route("/delete_membership/<int:id>", methods=["GET", "POST"])
def delete_membership(id):
    form = MembershipForm()
    register = Memberships.query.get_or_404(id)

    deleteRegister = DeleteRegister(
        register, form, REGISTER_TYPE, S3_FOLDER, TEMPLATE_FOLDER
    )
    return deleteRegister.returnTemplate()


@app.route("/remind/<int:id>")
def remind(id):
    member = Members.query.filter_by(id=id).first()
    last_membership = (
        Memberships.query.filter_by(member_id=id)
        .order_by(Memberships.end.desc())
        .first()
    )
    return render_template(
        "/memberships/reminder.html", member=member, last_membership=last_membership
    )


# Aline - Expired - jan
# 2020-2021
# 2021-2022
# 2022-2023
# 2023-2024 feb

# Sev - Paid nov
# 2022-2023
# 2023-2024
# 2024-2025
# 2025-2026

# Member 1 - Almost Expired - remembered
# 2024-2025 - jul

# Member 2 - Almost Expired - not remembered
# 2024-2025 - jul
