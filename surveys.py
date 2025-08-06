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

    # if form.validate_on_submit():
    #     survey = Surveys.query.filter_by(title=form.title.data).first()
    #
    #     if request.files["file"].filename:
    #         unique_filename = save_file(form.file.data, "docs/surveys/")
    #     form.file.data = unique_filename
    #
    #     if survey is None:
    #         survey = Surveys(
    #             title=form.title.data,
    #             start=form.start.data,
    #             end=form.end.data,
    #             responders=form.responders.data,
    #             file=form.file.data,
    #         )
    #         db.session.add(survey)
    #         db.session.commit()
    #         flash("Survey added successfully!")
    #
    #         title = form.title.data
    #         form.title.data = ""
    #         form.start.data = ""
    #         form.end.data = ""
    #
    # return render_template(
    #     "surveys/add_survey.html",
    #     form=form,
    #     title=title,
    # )


@app.route("/update_survey/<int:id>", methods=["GET", "POST"])
def update_survey(id):
    form = SurveyForm()
    register = Surveys.query.get_or_404(id)

    updateRegister = UpdateRegisterSurvey(
        request, register, form, REGISTER_TYPE, S3_FOLDER, TEMPLATE_FOLDER
    )
    return updateRegister.returnTemplate()
    # title = None
    # survey_to_update = Surveys.query.get_or_404(id)
    # if request.method == "POST":
    #     survey_to_update.title = request.form["title"]
    #     survey_to_update.start = request.form["start"]
    #     survey_to_update.end = request.form["end"]
    #     survey_to_update.responders = request.form["responders"]
    #
    #     # Save file name to database
    #     if request.files["file"].filename:
    #         if survey_to_update.file:
    #             delete_file("docs/surveys/" + survey_to_update.file)
    #         unique_filename = save_file(form.file.data, "docs/surveys/")
    #
    #     survey_to_update.file = unique_filename
    #
    #     try:
    #         db.session.commit()
    #         flash("Meeting updated successfully!")
    #         return render_template(
    #             "surveys/update_survey.html",
    #             form=form,
    #             survey_to_update=survey_to_update,
    #         )
    #     except:
    #         flash("Error")
    #         return render_template(
    #             "surveys/update_survey.html",
    #             form=form,
    #             survey_to_update=survey_to_update,
    #         )
    # else:
    #     return render_template(
    #         "surveys/update_survey.html", form=form, survey_to_update=survey_to_update
    #     )


@app.route("/delete_survey/<int:id>", methods=["GET", "POST"])
def delete_survey(id):
    survey_to_delete = Surveys.query.get_or_404(id)

    deleteRegister = DeleteRegister(
        register, form, REGISTER_TYPE, S3_FOLDER, TEMPLATE_FOLDER
    )
    return deleteRegister.returnTemplate()
    # title = None
    # form = SurveyForm()
    # try:
    #     db.session.delete(survey_to_delete)
    #     db.session.commit()
    #     flash("Survey deleted successfully!")
    #
    #     if survey_to_delete.file:
    #         delete_file("docs/surveys/" + survey_to_delete.file)
    #
    #     title = survey_to_delete.title
    #
    #     return render_template(
    #         "surveys/update_survey.html",
    #         form=form,
    #         title=title,
    #         survey_to_update=survey_to_delete,
    #     )
    # except:
    #     flash("Error")
    #     return render_template(
    #         "surveys/update_survey.html",
    #         form=form,
    #         title=title,
    #         survey_to_update=survey_to_delete,
    #     )
