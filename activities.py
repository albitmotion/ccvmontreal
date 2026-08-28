from flask import Flask, render_template, jsonify, flash, request
from app import (
    app,
    db,
    Members,
    Activities,
    save_file,
    delete_file,
    AddRegister,
    UpdateRegister,
    DeleteRegister,
)
from webforms import ActivityForm

from werkzeug.utils import secure_filename
import uuid as uuid
import os


REGISTER_TYPE = "Activity"
S3_FOLDER = "images/activities/"
TEMPLATE_FOLDER = "content"


class AddRegisterActivity(AddRegister):
    def checkIfExists(self):
        self.register = Activities.query.filter_by(titleEN=self.form.titleEN.data).first()
        return self.register

    def createRegister(self):
        self.register = Activities()
        self.register.titleEN = self.form.titleEN.data
        self.register.titleFR = self.form.titleFR.data
        self.register.textEN = self.form.textEN.data
        self.register.textFR = self.form.textFR.data
        self.register.date = self.form.date.data
        self.register.hourEN = self.form.hourEN.data
        self.register.hourFR = self.form.hourFR.data
        self.register.addressEN = self.form.addressEN.data
        self.register.addressFR = self.form.addressFR.data
        if self.unique_filename:
            self.register.file = self.unique_filename


class UpdateRegisterActivity(UpdateRegister):
    def updateRegister(self):
        self.register.titleEN = self.form.titleEN.data
        self.register.titleFR = self.form.titleFR.data
        self.register.textEN = self.form.textEN.data
        self.register.textFR = self.form.textFR.data
        self.register.date = self.form.date.data
        self.register.hourEN = self.form.hourEN.data
        self.register.hourFR = self.form.hourFR.data
        self.register.addressEN = self.form.addressEN.data
        self.register.addressFR = self.form.addressFR.data
        if self.unique_filename:
            self.register.file = self.unique_filename


@app.route("/add_activity", methods=["GET", "POST"])
def add_activity():
    form = ActivityForm()
    form_fields = [
        form.titleEN,
        form.titleFR,
        form.textEN,
        form.textFR,
        form.date,
        form.hourEN,
        form.hourFR,
        form.addressEN,
        form.addressFR,
        form.file,
    ]

    addRegister = AddRegisterActivity(
        request, form, REGISTER_TYPE, S3_FOLDER, form_fields, TEMPLATE_FOLDER
    )
    return addRegister.returnTemplate()


@app.route("/update_activity/<int:id>", methods=["GET", "POST"])
def update_activity(id):
    register = Activities.query.get_or_404(id)
    form = ActivityForm(obj=register)

    updateRegister = UpdateRegisterActivity(
        request, register, form, REGISTER_TYPE, S3_FOLDER, TEMPLATE_FOLDER
    )
    return updateRegister.returnTemplate()


@app.route("/delete_activity/<int:id>", methods=["GET", "POST"])
def delete_activity(id):
    register = Activities.query.get_or_404(id)
    form = ActivityForm()

    deleteRegister = DeleteRegister(
        register, form, REGISTER_TYPE, S3_FOLDER, TEMPLATE_FOLDER
    )
    return deleteRegister.returnTemplate()
