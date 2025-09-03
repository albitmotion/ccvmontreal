from flask import Flask, render_template, jsonify, flash, request
from app import app, db, Members, Quotes, AddRegister, UpdateRegister, DeleteRegister
from webforms import QuoteForm

from werkzeug.utils import secure_filename
import uuid as uuid
import os


REGISTER_TYPE = "Quote"
S3_FOLDER = "images/quotes/"
TEMPLATE_FOLDER = "content"


class AddRegisterQuote(AddRegister):
    def checkIfExists(self):
        self.register = Quotes.query.filter_by(title=self.form.title.data).first()
        return self.register

    def createRegister(self):
        self.register = Quotes()
        self.register.title = self.form.title.data
        self.register.text = self.form.text.data
        self.register.author = self.form.author.data
        self.register.organization = self.form.organization.data
        self.register.visible = self.form.visible.data
        self.register.fontSize = self.form.fontSize.data


class UpdateRegisterQuote(UpdateRegister):
    def updateRegister(self):
        self.register.title = self.form.title.data
        self.register.text = self.form.text.data
        self.register.author = self.form.author.data
        self.register.organization = self.form.organization.data
        self.register.visible = self.form.visible.data
        self.register.fontSize = self.form.fontSize.data


@app.route("/add_quote", methods=["GET", "POST"])
def add_quote():
    form = QuoteForm()
    form_fields = [
        form.title,
        form.text,
        form.author,
        form.organization,
        form.visible,
        form.fontSize,
    ]

    addRegister = AddRegisterQuote(
        request, form, REGISTER_TYPE, S3_FOLDER, form_fields, TEMPLATE_FOLDER, ""
    )
    return addRegister.returnTemplate()


@app.route("/update_quote/<int:id>", methods=["GET", "POST"])
def update_quote(id):
    form = QuoteForm()
    register = Quotes.query.get_or_404(id)

    updateRegister = UpdateRegisterQuote(
        request, register, form, REGISTER_TYPE, S3_FOLDER, TEMPLATE_FOLDER, None
    )
    return updateRegister.returnTemplate()


@app.route("/delete_quote/<int:id>", methods=["GET", "POST"])
def delete_quote(id):
    register = Quotes.query.get_or_404(id)
    form = QuoteForm()

    deleteRegister = DeleteRegister(
        register, form, REGISTER_TYPE, S3_FOLDER, TEMPLATE_FOLDER, None
    )
    return deleteRegister.returnTemplate()
