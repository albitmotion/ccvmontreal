from flask import Flask, render_template, jsonify, flash, request
from app import (
    app,
    db,
    Members,
    Meetings,
    Memberships,
    Surveys,
    save_file,
    delete_file,
    AddRegister,
    UpdateRegister,
    DeleteRegister,
)
from webforms import SurveyForm

from werkzeug.utils import secure_filename
import uuid as uuid
import os


REGISTER_TYPE = "Survey"
S3_FOLDER = "docs/surveys/"
TEMPLATE_FOLDER = "surveys"


class AddRegisterSurvey(AddRegister):
    def checkIfExists(self):
        self.register = Surveys.query.filter_by(title=self.form.title.data).first()
        return self.register

    def createRegister(self):
        self.register = Surveys()
        self.register.title = self.form.title.data
        self.register.start = self.form.start.data
        self.register.end = self.form.end.data
        self.register.responders = self.form.responders.data
        if self.unique_filename:
            self.register.file = self.unique_filename


class UpdateRegisterSurvey(UpdateRegister):
    def updateRegister(self):
        self.register.title = self.form.title.data
        self.register.start = self.form.start.data
        self.register.end = self.form.end.data
        self.register.responders = self.form.responders.data
        if self.unique_filename:
            self.register.file = self.unique_filename


# SURVEY FORM/DATABASE ----------------------------------------------------
@app.route("/add_survey", methods=["GET", "POST"])
def add_survey():
    form = SurveyForm()
    form_fields = [
        form.title,
        form.start,
        form.end,
        form.responders,
        form.file,
    ]

    addRegister = AddRegisterSurvey(
        request, form, REGISTER_TYPE, S3_FOLDER, form_fields, TEMPLATE_FOLDER
    )
    return addRegister.returnTemplate()


@app.route("/update_survey/<int:id>", methods=["GET", "POST"])
def update_survey(id):
    form = SurveyForm()
    register = Surveys.query.get_or_404(id)

    updateRegister = UpdateRegisterSurvey(
        request, register, form, REGISTER_TYPE, S3_FOLDER, TEMPLATE_FOLDER
    )
    return updateRegister.returnTemplate()


@app.route("/delete_survey/<int:id>", methods=["GET", "POST"])
def delete_survey(id):
    survey_to_delete = Surveys.query.get_or_404(id)

    deleteRegister = DeleteRegister(
        register, form, REGISTER_TYPE, S3_FOLDER, TEMPLATE_FOLDER
    )
    return deleteRegister.returnTemplate()
