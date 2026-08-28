from flask import Flask, render_template, jsonify, flash, request
from app import (
    app,
    db,
    Members,
    AnnualReports,
    save_file,
    delete_file,
    AddRegister,
    UpdateRegister,
    DeleteRegister,
)
from webforms import AnnualReportForm

from werkzeug.utils import secure_filename
import uuid as uuid
import os


REGISTER_TYPE = "Annual Report"
S3_FOLDER = "docs/annualReports/"
TEMPLATE_FOLDER = "content"


class AddRegisterAnnualReport(AddRegister):
    def checkIfExists(self):
        self.register = AnnualReports.query.filter_by(
            filename=self.form.filename.data
        ).first()
        return self.register

    def createRegister(self):
        self.register = AnnualReports()
        self.register.filename = self.request.files["file"].filename
        self.register.file = self.unique_filename
        self.register.visible = self.form.visible.data


class UpdateRegisterAnnualReport(UpdateRegister):
    def updateRegister(self):
        if self.unique_filename:
            self.register.filename = self.request.files["file"].filename
            self.register.file = self.unique_filename
        self.register.visible = self.form.visible.data


@app.route("/add_annualReport", methods=["GET", "POST"])
def add_annualReport():
    form = AnnualReportForm()
    form_fields = [
        form.filename,
        form.file,
        form.visible,
    ]

    addRegister = AddRegisterAnnualReport(
        request, form, REGISTER_TYPE, S3_FOLDER, form_fields, TEMPLATE_FOLDER
    )
    return addRegister.returnTemplate()


@app.route("/update_annualReport/<int:id>", methods=["GET", "POST"])
def update_annualReport(id):
    form = AnnualReportForm()
    register = AnnualReports.query.get_or_404(id)

    updateRegister = UpdateRegisterAnnualReport(
        request, register, form, REGISTER_TYPE, S3_FOLDER, TEMPLATE_FOLDER
    )
    return updateRegister.returnTemplate()


@app.route("/delete_annualReport/<int:id>", methods=["GET", "POST"])
def delete_annualReport(id):
    register = AnnualReports.query.get_or_404(id)
    form = AnnualReportForm()

    deleteRegister = DeleteRegister(
        register, form, REGISTER_TYPE, S3_FOLDER, TEMPLATE_FOLDER
    )
    return deleteRegister.returnTemplate()
