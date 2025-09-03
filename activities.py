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
        self.register = Activities.query.filter_by(title=self.form.title.data).first()
        return self.register

    def createRegister(self):
        self.register = Activities()
        self.register.title = self.form.title.data
        self.register.text = self.form.text.data
        self.register.date = self.form.date.data
        self.register.hour = self.form.hour.data
        self.register.address = self.form.address.data
        if self.unique_filename:
            self.register.file = self.unique_filename


class UpdateRegisterActivity(UpdateRegister):
    def updateRegister(self):
        self.register.title = self.form.title.data
        self.register.text = self.request.form.get("ckeditor")
        self.register.date = self.form.date.data
        self.register.hour = self.form.hour.data
        self.register.address = self.form.address.data
        if self.unique_filename:
            self.register.file = self.unique_filename


@app.route("/add_activity", methods=["GET", "POST"])
def add_activity():
    form = ActivityForm()
    form_fields = [
        form.title,
        form.text,
        form.date,
        form.hour,
        form.address,
        form.file,
    ]

    addRegister = AddRegisterActivity(
        request, form, REGISTER_TYPE, S3_FOLDER, form_fields, TEMPLATE_FOLDER
    )
    return addRegister.returnTemplate()


@app.route("/update_activity/<int:id>", methods=["GET", "POST"])
def update_activity(id):
    form = ActivityForm()
    register = Activities.query.get_or_404(id)

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
