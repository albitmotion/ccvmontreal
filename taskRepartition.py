from flask import Flask, render_template, jsonify, flash, request
from app import (
    app,
    db,
    Members,
    TaskRepartitionTexts,
    TaskRepartitionFiles,
    save_file,
    AddRegister,
    UpdateRegister,
    DeleteRegister,
)

from webforms import TaskRepartitionTextForm, TaskRepartitionFileForm

from werkzeug.utils import secure_filename
import uuid as uuid
import os


REGISTER_TYPE = "Task Repartition File"
S3_FOLDER = "docs/taskRepartitions/"
TEMPLATE_FOLDER = "content"


class AddRegisterTaskRepartition(AddRegister):
    def checkIfExists(self):
        self.register = TaskRepartitionFiles.query.filter_by(
            filename=self.request.files["file"].filename
        ).first()
        return self.register

    def createRegister(self):
        self.register = TaskRepartitionFiles()
        self.register.file = self.unique_filename
        self.register.filename = self.request.files["file"].filename


class UpdateTaskRepartition(UpdateRegister):
    def updateRegister(self):
        self.register.file = self.unique_filename
        self.register.filename = self.request.files["file"].filename


@app.route("/add_task_repartition_file", methods=["GET", "POST"])
def add_task_repartition_file():
    form = TaskRepartitionFileForm()
    form_fields = [form.file, form.filename]

    addRegister = AddRegisterTaskRepartition(
        request, form, REGISTER_TYPE, S3_FOLDER, form_fields, TEMPLATE_FOLDER
    )
    return addRegister.returnTemplate()


@app.route("/update_task_repartition_file/<int:id>", methods=["GET", "POST"])
def update_task_repartition_file(id):
    form = TaskRepartitionFileForm()
    register = TaskRepartitionFiles.query.get_or_404(id)

    updateRegister = UpdateTaskRepartition(
        request, register, form, REGISTER_TYPE, S3_FOLDER, TEMPLATE_FOLDER
    )
    return updateRegister.returnTemplate()


@app.route("/delete_task_repartition_file/<int:id>", methods=["GET", "POST"])
def delete_task_repartition_file(id):
    register = TaskRepartitionFiles.query.get_or_404(id)
    form = TaskRepartitionFileForm()

    deleteRegister = DeleteRegister(
        register, form, REGISTER_TYPE, S3_FOLDER, TEMPLATE_FOLDER
    )
    return deleteRegister.returnTemplate()


@app.route("/update_task_repartition/<int:id>", methods=["GET", "POST"])
def update_task_repartition(id):
    form = TaskRepartitionTextForm()
    task_to_update = TaskRepartitionTexts.query.get_or_404(1)
    if request.method == "POST":

        task_to_update.text = request.form.get("ckeditor")
        try:
            db.session.commit()
            flash("Task Repartition Text updated successfully!")

            return render_template(
                "content/update_task_repartition_text.html",
                form=form,
                task_to_update=task_to_update,
            )
        except:
            flash("Error")
            return render_template(
                "content/update_task_repartition_text.html",
                form=form,
                task_to_update=task_to_update,
            )
    else:
        return render_template(
            "content/update_task_repartition_text.html",
            form=form,
            task_to_update=task_to_update,
        )
