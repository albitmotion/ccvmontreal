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
    # if form.validate_on_submit():
    #     activity = Activities.query.filter_by(title=form.title.data).first()
    #     if activity is None:
    #         # Save file name to database
    #         form.filename.data = request.files["file"].filename
    #
    #         # Save File
    #         if form.file.data:
    #             unique_filename = save_file(form.file.data, "images/activities/")
    #             form.file.data = unique_filename
    #
    #         # Save in database
    #         activity = Activities(
    #             title=form.title.data,
    #             text=form.text.data,
    #             date=form.date.data,
    #             hour=form.hour.data,
    #             address=form.address.data,
    #             file=form.file.data,
    #         )
    #         db.session.add(activity)
    #         db.session.commit()
    #         flash("Activity added successfully!")
    #
    #         form.title.data = ""
    #         form.text.data = ""
    #         form.date.data = ""
    #         form.hour.data = ""
    #         form.address.data = ""
    #         form.file.data = ""
    #     else:
    #         flash("Error: An activity with this title already exists.")
    #
    # return render_template(
    #     "content/add_activity.html",
    #     form=form,
    # )


@app.route("/update_activity/<int:id>", methods=["GET", "POST"])
def update_activity(id):
    form = ActivityForm()
    register = Activities.query.get_or_404(id)

    updateRegister = UpdateRegisterActivity(
        request, register, form, REGISTER_TYPE, S3_FOLDER, TEMPLATE_FOLDER
    )
    return updateRegister.returnTemplate()
    # activity_to_update = Activities.query.get_or_404(id)
    # if request.method == "POST":
    #     if request.files["file"]:
    #         # form.filename.data = request.files["file"].filename
    #         if activity_to_update.file:
    #             delete_file("images/activities/" + activity_to_update.file)
    #         # Save File
    #         unique_filename = save_file(form.file.data, "images/activities/")
    #         # form.file.data = unique_filename
    #
    #         # unique_filename = save_file(
    #         #     request.files["file"], "images/activities/" + request.files["file"]
    #         # )
    #
    #         activity_to_update.file = unique_filename
    #         activity_to_update.filename = request.files["file"].filename
    #
    #     activity_to_update.text = request.form.get("ckeditor")
    #     activity_to_update.date = form.date.data
    #     activity_to_update.hour = form.hour.data
    #     activity_to_update.address = form.address.data
    #     activity_to_update.title = form.title.data
    #
    #     try:
    #         db.session.commit()
    #         flash("Activity updated successfully!")
    #         return render_template(
    #             "content/update_activity.html",
    #             form=form,
    #             activity_to_update=activity_to_update,
    #         )
    #     except:
    #         flash("Error")
    #         return render_template(
    #             "content/update_activity.html",
    #             form=form,
    #             activity_to_update=activity_to_update,
    #         )
    # else:
    #     return render_template(
    #         "content/update_activity.html",
    #         form=form,
    #         activity_to_update=activity_to_update,
    #     )


@app.route("/delete_activity/<int:id>", methods=["GET", "POST"])
def delete_activity(id):
    register = Activities.query.get_or_404(id)
    form = ActivityForm()

    deleteRegister = DeleteRegister(
        register, form, REGISTER_TYPE, S3_FOLDER, TEMPLATE_FOLDER
    )
    return deleteRegister.returnTemplate()
    #
    # try:
    #     db.session.delete(activity_to_delete)
    #     db.session.commit()
    #     flash("Activity deleted successfully!")
    #
    #     if activity_to_delete.file:
    #         delete_file("images/activities/" + activity_to_delete.file)
    #
    #     form.title.data = ""
    #     form.text.data = ""
    #     form.date.data = ""
    #     form.hour.data = ""
    #     form.address.data = ""
    #     form.file.data = ""
    #
    #     return render_template(
    #         "content/update_activity.html",
    #         form=form,
    #         activity_to_update=activity_to_delete,
    #     )
    # except:
    #     flash("Error: Not possible to delete activity.")
    #     return render_template(
    #         "content/update_activity.html",
    #         form=form,
    #         activity_to_update=activity_to_delete,
    #     )
