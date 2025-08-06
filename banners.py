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
    # if form.validate_on_submit():
    #     banner = Banners.query.filter_by(filename=form.filename.data).first()
    #     if banner is None:
    #         # If visible uncheck others
    #         if form.visible.data == True:
    #             banners = Banners.query.filter_by(visible=True)
    #             for banner in banners:
    #                 banner.visible = False
    #                 db.session.commit()
    #
    #         # Save file name to database
    #         form.filename.data = request.files["file"].filename
    #
    #         # Save File
    #         if form.file.data:
    #             unique_filename = save_file(form.file.data, "images/banners/")
    #             form.file.data = unique_filename
    #
    #         # Save in database
    #         banner = Banners(
    #             filename=form.filename.data,
    #             file=form.file.data,
    #             visible=form.visible.data,
    #         )
    #         db.session.add(banner)
    #         db.session.commit()
    #         flash("Banner added successfully!")
    #
    #         form.filename.data = ""
    #         form.file.data = ""
    #         form.visible.data = ""
    #
    # return render_template(
    #     "content/add_banner.html",
    #     form=form,
    # )


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
    # banner_to_update = Banners.query.get_or_404(id)
    # if request.method == "POST":
    #     if form.visible.data == True:
    #         banners = Banners.query.filter_by(visible=True)
    #         for banner in banners:
    #             banner.visible = False
    #             db.session.commit()
    #
    #     if request.files["file"]:
    #         if banner_to_update.file:
    #             delete_file("images/banners/" + banner_to_update.file)
    #         unique_filename = save_file(request.files["file"], "images/banners")
    #
    #         banner_to_update.file = unique_filename
    #         banner_to_update.filename = request.files["file"].filename
    #
    #     banner_to_update.visible = form.visible.data
    #
    #     try:
    #         db.session.commit()
    #         flash("Banner updated successfully!")
    #         return render_template(
    #             "content/update_banner.html",
    #             form=form,
    #             banner_to_update=banner_to_update,
    #         )
    #     except:
    #         flash("Error")
    #         return render_template(
    #             "content/update_banner.html",
    #             form=form,
    #             banner_to_update=banner_to_update,
    #         )
    # else:
    #     return render_template(
    #         "content/update_banner.html", form=form, banner_to_update=banner_to_update
    #     )


@app.route("/delete_banner/<int:id>", methods=["GET", "POST"])
def delete_banner(id):
    register = Banners.query.get_or_404(id)
    form = BannerForm()

    deleteRegister = DeleteRegister(
        register, form, REGISTER_TYPE, S3_FOLDER, TEMPLATE_FOLDER
    )
    return deleteRegister.returnTemplate()
    #
    # try:
    #     db.session.delete(banner_to_update)
    #     db.session.commit()
    #     flash("Banner deleted successfully!")
    #
    #     if banner_to_update.file:
    #         delete_file("images/banners/" + banner_to_update.file)
    #
    #     form.file.data = ""
    #     form.visible.data = ""
    #
    #     return render_template(
    #         "content/update_banner.html", form=form, banner_to_update=banner_to_update
    #     )
    # except:
    #     flash("Error: Not possible to delete Banner.")
    #     return render_template(
    #         "content/update_banner.html", form=form, banner_to_update=banner_to_update
    #     )
