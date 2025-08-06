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
    # if form.validate_on_submit():
    #     annualReport = AnnualReports.query.filter_by(
    #         filename=form.filename.data
    #     ).first()
    #     if annualReport is None:
    #         # Save file name to database
    #         if request.files["file"]:
    #             form.filename.data = request.files["file"].filename
    #
    #             # Save File
    #             unique_filename = save_file(form.file.data, "docs/annualReports/")
    #             form.file.data = unique_filename
    #
    #         # Save in database
    #         annualReport = AnnualReports(
    #             filename=form.filename.data,
    #             file=form.file.data,
    #             visible=form.visible.data,
    #         )
    #         db.session.add(annualReport)
    #         db.session.commit()
    #         flash("Annual Report added successfully!")
    #
    #         form.filename.data = ""
    #         form.file.data = ""
    #         form.visible.data = ""
    #
    # return render_template(
    #     "content/add_annualReport.html",
    #     form=form,
    # )


@app.route("/update_annualReport/<int:id>", methods=["GET", "POST"])
def update_annualReport(id):
    form = AnnualReportForm()
    register = AnnualReports.query.get_or_404(id)

    updateRegister = UpdateRegisterAnnualReport(
        request, register, form, REGISTER_TYPE, S3_FOLDER, TEMPLATE_FOLDER
    )
    return updateRegister.returnTemplate()
    # annualReport_to_update = AnnualReports.query.get_or_404(id)
    # if request.method == "POST":
    #
    #     if request.files["file"]:
    #         if annualReport_to_update.file:
    #             delete_file("docs/annualReports/" + annualReport_to_update.file)
    #         unique_filename = save_file(request.files["file"], "docs/annualReports/")
    #
    #         annualReport_to_update.file = unique_filename
    #         annualReport_to_update.filename = request.files["file"].filename
    #
    #     annualReport_to_update.visible = form.visible.data
    #
    #     try:
    #         db.session.commit()
    #         flash("Annual Report updated successfully!")
    #         return render_template(
    #             "content/update_annualReport.html",
    #             form=form,
    #             annualReport_to_update=annualReport_to_update,
    #         )
    #     except:
    #         flash("Error")
    #         return render_template(
    #             "content/update_annualReport.html",
    #             form=form,
    #             annualReport_to_update=annualReport_to_update,
    #         )
    # else:
    #     return render_template(
    #         "content/update_annualReport.html",
    #         form=form,
    #         annualReport_to_update=annualReport_to_update,
    #     )


@app.route("/delete_annualReport/<int:id>", methods=["GET", "POST"])
def delete_annualReport(id):
    register = AnnualReports.query.get_or_404(id)
    form = AnnualReportForm()

    deleteRegister = DeleteRegister(
        register, form, REGISTER_TYPE, S3_FOLDER, TEMPLATE_FOLDER
    )
    return deleteRegister.returnTemplate()
    #
    # try:
    #     db.session.delete(annualReport_to_update)
    #     db.session.commit()
    #     flash("Annual Report deleted successfully!")
    #     print("delete 1")
    #     if annualReport_to_update.file:
    #         print("delete 2" + "docs/annualReports/" + annualReport_to_update.file)
    #         delete_file("docs/annualReports/" + annualReport_to_update.file)
    #         print("delete 3")
    #     print("delete 4")
    #     form.file.data = ""
    #     form.visible.data = ""
    #
    #     return render_template(
    #         "content/update_annualReport.html",
    #         form=form,
    #         annualReport_to_update=annualReport_to_update,
    #     )
    # except:
    #     flash("Error: Not possible to delete Annual Report.")
    #     return render_template(
    #         "content/update_annualReport.html",
    #         form=form,
    #         annualReport_to_update=annualReport_to_update,
    #     )
