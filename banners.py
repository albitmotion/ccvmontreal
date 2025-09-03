from flask import Flask, render_template, jsonify, flash, request
from app import (
    app,
    db,
    Members,
    Banners,
    save_file,
    delete_file,
    AddRegister,
    UpdateRegister,
    DeleteRegister,
)
from webforms import BannerForm

from werkzeug.utils import secure_filename
import uuid as uuid
import os


REGISTER_TYPE = "Banner"
S3_FOLDER = "images/banners/"
TEMPLATE_FOLDER = "content"


class AddRegisterBanner(AddRegister):
    def checkIfExists(self):
        self.register = Banners.query.filter_by(
            filename=self.form.filename.data
        ).first()
        return self.register

    def createRegister(self):
        if self.form.visible.data == True:
            banners = Banners.query.filter_by(visible=True)
            for banner in banners:
                banner.visible = False
                db.session.commit()

        self.register = Banners()
        self.register.filename = self.request.files["file"].filename
        self.register.file = self.unique_filename
        self.register.visible = self.form.visible.data


class UpdateRegisterBanner(UpdateRegister):
    def updateRegister(self):
        if self.form.visible.data == True:
            banners = Banners.query.filter_by(visible=True)
            for banner in banners:
                banner.visible = False
                db.session.commit()

        if self.unique_filename:
            self.register.filename = self.request.files["file"].filename
            self.register.file = self.unique_filename
        self.register.visible = self.form.visible.data


@app.route("/add_banner", methods=["GET", "POST"])
def add_banner():
    form = BannerForm()
    form_fields = [
        form.filename,
        form.file,
        form.visible,
    ]

    addRegister = AddRegisterBanner(
        request, form, REGISTER_TYPE, S3_FOLDER, form_fields, TEMPLATE_FOLDER
    )
    return addRegister.returnTemplate()


@app.route("/update_banner/<int:id>", methods=["GET", "POST"])
def update_banner(id):
    form = BannerForm()
    register = Banners.query.get_or_404(id)
    form_fields = [
        form.filename,
        form.file,
        form.visible,
    ]

    updateRegister = UpdateRegisterBanner(
        request, register, form, REGISTER_TYPE, S3_FOLDER, TEMPLATE_FOLDER
    )
    return updateRegister.returnTemplate()


@app.route("/delete_banner/<int:id>", methods=["GET", "POST"])
def delete_banner(id):
    register = Banners.query.get_or_404(id)
    form = BannerForm()

    deleteRegister = DeleteRegister(
        register, form, REGISTER_TYPE, S3_FOLDER, TEMPLATE_FOLDER
    )
    return deleteRegister.returnTemplate()
