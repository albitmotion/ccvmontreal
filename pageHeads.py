from flask import Flask, render_template, jsonify, flash, request
from app import (
    app,
    db,
    Members,
    PageHeads,
    save_file,
    delete_file,
    AddRegister,
    UpdateRegister,
    DeleteRegister,
)
from webforms import PageHeadForm

from werkzeug.utils import secure_filename
import uuid as uuid
import os


REGISTER_TYPE = "PageHead"
S3_FOLDER = "images/pageHeads/"
TEMPLATE_FOLDER = "content"


class AddRegisterPageHead(AddRegister):
    def checkIfExists(self):
        self.register = PageHeads.query.filter_by(
            filename=self.form.filename.data
        ).first()
        return self.register

    def createRegister(self):
        pageHeads = PageHeads.query.all()
        for pageHead in pageHeads:
            db.session.commit()

        self.register = PageHeads()
        self.register.filename = self.request.files["file"].filename
        self.register.file = self.unique_filename


class UpdateRegisterPageHead(UpdateRegister):
    def updateRegister(self):
        pageHeads = PageHeads.query.all()

        if self.unique_filename:
            self.register.filename = self.request.files["file"].filename
            self.register.file = self.unique_filename


@app.route("/add_pageHeader", methods=["GET", "POST"])
def add_pageHead():
    form = PageHeadForm()
    form_fields = [
        form.filename,
        form.file,
    ]

    addRegister = AddRegisterPageHead(
        request, form, REGISTER_TYPE, S3_FOLDER, form_fields, TEMPLATE_FOLDER
    )
    return addRegister.returnTemplate()


@app.route("/update_pageHead/<int:id>", methods=["GET", "POST"])
def update_pageHead(id):
    form = PageHeadForm()
    register = PageHeads.query.get_or_404(id)
    form_fields = [
        form.filename,
        form.file,
    ]

    updateRegister = UpdateRegisterPageHead(
        request, register, form, REGISTER_TYPE, S3_FOLDER, TEMPLATE_FOLDER
    )
    return updateRegister.returnTemplate()


@app.route("/delete_pageHead/<int:id>", methods=["GET", "POST"])
def delete_pageHead(id):
    register = PageHeads.query.get_or_404(id)
    form = PageHeadForm()

    deleteRegister = DeleteRegister(
        register, form, REGISTER_TYPE, S3_FOLDER, TEMPLATE_FOLDER
    )
    return deleteRegister.returnTemplate()
