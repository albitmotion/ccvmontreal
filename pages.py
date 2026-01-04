from flask import Flask, render_template, jsonify, flash, request
from app import app, db, Members, Pages, AddRegister, UpdateRegister, DeleteRegister
from webforms import PageForm

from werkzeug.utils import secure_filename
import uuid as uuid
import os

REGISTER_TYPE = "Page"
S3_FOLDER = ""
TEMPLATE_FOLDER = "content"


class AddRegisterPage(AddRegister):
    def checkIfExists(self):
        self.register = Pages.query.filter_by(name=self.form.name.data).first()
        return self.register

    def createRegister(self):
        self.register = Pages()
        self.register.name = self.form.name.data
        self.register.url = self.form.url.data
        self.register.textEN = self.request.form.get("ck1")
        self.register.textFR = self.request.form.get("ck2")


class UpdateRegisterPage(UpdateRegister):
    def updateRegister(self):
        self.register.name = self.form.name.data
        self.register.url = self.form.url.data
        self.register.textEN = self.request.form.get("ck1")
        self.register.textFR = self.request.form.get("ck2")
        # self.register.textFR = self.form.textFR.data


@app.route("/add_page", methods=["GET", "POST"])
def add_page():
    form = PageForm()
    form_fields = [
        form.name,
        form.url,
        form.textEN,
        form.textFR,
    ]

    addRegister = AddRegisterPage(
        request, form, REGISTER_TYPE, S3_FOLDER, form_fields, TEMPLATE_FOLDER, ""
    )
    return addRegister.returnTemplate()


@app.route("/update_page/<int:id>", methods=["GET", "POST"])
def update_page(id):
    form = PageForm()
    register = Pages.query.get_or_404(id)

    updateRegister = UpdateRegisterPage(
        request, register, form, REGISTER_TYPE, S3_FOLDER, TEMPLATE_FOLDER, None
    )
    return updateRegister.returnTemplate()


@app.route("/delete_page/<int:id>", methods=["GET", "POST"])
def delete_page(id):
    register = Pages.query.get_or_404(id)
    form = PageForm()

    deleteRegister = DeleteRegister(
        register, form, REGISTER_TYPE, S3_FOLDER, TEMPLATE_FOLDER, None
    )
    return deleteRegister.returnTemplate()
