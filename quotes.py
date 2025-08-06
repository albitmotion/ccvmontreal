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
    # if form.validate_on_submit():
    #     quote = Quotes.query.filter_by(title=form.title.data).first()
    #     if quote is None:
    #
    #         # Save in database
    #         quote = Quotes(
    #             title=form.title.data,
    #             text=form.text.data,
    #             author=form.author.data,
    #             organization=form.organization.data,
    #             visible=form.visible.data,
    #             fontSize=form.fontSize.data,
    #         )
    #         db.session.add(quote)
    #         db.session.commit()
    #         flash("Quote added successfully!")
    #
    #         form.title.data = ""
    #         form.text.data = ""
    #         form.author.data = ""
    #         form.organization.data = ""
    #         form.visible.data = ""
    #         form.fontSize.data = ""
    #
    # return render_template(
    #     "content/add_quote.html",
    #     form=form,
    # )


@app.route("/update_quote/<int:id>", methods=["GET", "POST"])
def update_quote(id):
    form = QuoteForm()
    register = Quotes.query.get_or_404(id)

    updateRegister = UpdateRegisterQuote(
        request, register, form, REGISTER_TYPE, S3_FOLDER, TEMPLATE_FOLDER, None
    )
    return updateRegister.returnTemplate()
    # quote_to_update = Quotes.query.get_or_404(id)
    # if request.method == "POST":
    #     quote_to_update.title = form.title.data
    #     quote_to_update.text = request.form.get("text")
    #     quote_to_update.author = form.author.data
    #     quote_to_update.organization = form.organization.data
    #     quote_to_update.visible = form.visible.data
    #     quote_to_update.fontSize = form.fontSize.data
    #
    #     try:
    #         db.session.commit()
    #         flash("Quote updated successfully!")
    #         return render_template(
    #             "content/update_quote.html", form=form, quote_to_update=quote_to_update
    #         )
    #     except:
    #         flash("Error: Not possible to update quote.")
    #         return render_template(
    #             "content/update_quote.html", form=form, quote_to_update=quote_to_update
    #         )
    # else:
    #     return render_template(
    #         "content/update_quote.html", form=form, quote_to_update=quote_to_update
    #     )


@app.route("/delete_quote/<int:id>", methods=["GET", "POST"])
def delete_quote(id):
    register = Quotes.query.get_or_404(id)
    form = QuoteForm()

    deleteRegister = DeleteRegister(
        register, form, REGISTER_TYPE, S3_FOLDER, TEMPLATE_FOLDER, None
    )
    return deleteRegister.returnTemplate()
    #
    # try:
    #     db.session.delete(quote_to_update)
    #     db.session.commit()
    #     flash("Quote deleted successfully!")
    #
    #     form.title.data = ""
    #     form.text.data = ""
    #     form.author.data = ""
    #     form.organization.data = ""
    #     form.visible.data = ""
    #     form.fontSize.data = ""
    #
    #     return render_template(
    #         "content/update_quote.html", form=form, quote_to_update=quote_to_update
    #     )
    # except:
    #     flash("Error: Not possible to delete quote.")
    #     return render_template(
    #         "content/update_quote.html", form=form, quote_to_update=quote_to_update
    #     )
