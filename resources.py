from flask import Flask, render_template, jsonify, flash, request
from app import (
    app,
    db,
    Members,
    Meetings,
    Memberships,
    Resources,
    save_file,
    delete_file,
    AddRegister,
    UpdateRegister,
    DeleteRegister,
)
from webforms import ResourceForm

from werkzeug.utils import secure_filename
import uuid as uuid
import os


REGISTER_TYPE = "Resource"
S3_FOLDER = "docs/resources/"
TEMPLATE_FOLDER = "resources"


class AddRegisterResource(AddRegister):
    def checkIfExists(self):
        self.register = Resources.query.filter_by(nameEN=self.form.nameEN.data).first()
        return self.register

    def createRegister(self):
        self.register = Resources()
        self.register.nameEN = self.form.nameEN.data
        self.register.nameFR = self.form.nameFR.data
        self.register.descriptionEN = self.form.descriptionEN.data
        self.register.descriptionFR = self.form.descriptionFR.data
        self.register.url = self.form.url.data
        if self.unique_filename:
            self.register.file = self.unique_filename


class UpdateRegisterResource(UpdateRegister):
    def updateRegister(self):
        self.register.nameEN = self.form.nameEN.data
        self.register.nameFR = self.form.nameFR.data
        self.register.descriptionEN = self.form.descriptionEN.data
        self.register.descriptionFR = self.form.descriptionFR.data
        self.register.url = self.form.url.data
        if self.unique_filename:
            self.register.file = self.unique_filename

# RESOURCES FORM/DATABASE ----------------------------------------------------
@app.route("/add_resource", methods=["GET", "POST"])
def add_resource():
    form = ResourceForm()
    form_fields = [
        form.nameEN,
        form.nameFR,
        form.descriptionEN,
        form.descriptionFR,
        form.url,
        form.file,
    ]

    addRegister = AddRegisterResource(
        request, form, REGISTER_TYPE, S3_FOLDER, form_fields, TEMPLATE_FOLDER
    )
    return addRegister.returnTemplate()


@app.route("/update_resource/<int:id>", methods=["GET", "POST"])
def update_resource(id):
    form = ResourceForm()
    register = Resources.query.get_or_404(id)

    updateRegister = UpdateRegisterResource(
        request, register, form, REGISTER_TYPE, S3_FOLDER, TEMPLATE_FOLDER
    )
    return updateRegister.returnTemplate()


@app.route("/delete_resource/<int:id>", methods=["GET", "POST"])
def delete_resource(id):
    form = ResourceForm()
    resource_to_delete = Resources.query.get_or_404(id)

    deleteRegister = DeleteRegister(
        resource_to_delete, form, REGISTER_TYPE, S3_FOLDER, TEMPLATE_FOLDER
    )
    return deleteRegister.returnTemplate()
