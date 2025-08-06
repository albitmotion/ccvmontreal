from flask import render_template, request
from app import app, News, AddRegister, UpdateRegister, DeleteRegister
from webforms import NewsForm
from datetime import date


REGISTER_TYPE = "News"
S3_FOLDER = "images/news/"
TEMPLATE_FOLDER = "content"


class AddRegisterNews(AddRegister):
    def checkIfExists(self):
        self.register = News.query.filter_by(title=self.request.form["title"]).first()
        return self.register

    def createRegister(self):
        self.register = News()
        self.register.title = self.request.form["title"]
        self.register.text = self.request.form["text"]
        self.register.type = self.request.form["type"]
        self.register.author = self.request.form["author"]
        self.register.date = date.today()
        self.register.file = self.unique_filename


class UpdateNews(UpdateRegister):
    def updateRegister(self):
        self.register.title = self.form.title.data
        self.register.text = self.request.form.get("ckeditor")
        self.register.type = self.form.type.data
        self.register.author = self.form.author.data
        self.register.date = self.form.date.data


@app.route("/add_news", methods=["GET", "POST"])
def add_news():
    form = NewsForm()
    form_fields = [form.title, form.text, form.type, form.date, form.file, form.author]

    addRegister = AddRegisterNews(
        request, form, REGISTER_TYPE, S3_FOLDER, form_fields, TEMPLATE_FOLDER
    )
    return addRegister.returnTemplate()


@app.route("/update_news/<int:id>", methods=["GET", "POST"])
def update_news(id):
    form = NewsForm()
    register = News.query.get_or_404(id)

    updateRegister = UpdateNews(
        request, register, form, REGISTER_TYPE, S3_FOLDER, TEMPLATE_FOLDER
    )
    return updateRegister.returnTemplate()


@app.route("/delete_news/<int:id>", methods=["GET", "POST"])
def delete_news(id):
    register = News.query.get_or_404(id)
    form = NewsForm()

    deleteRegister = DeleteRegister(
        register, form, REGISTER_TYPE, S3_FOLDER, TEMPLATE_FOLDER
    )
    return deleteRegister.returnTemplate()


@app.route("/news/<int:id>", methods=["GET", "POST"])
def view_news(id):
    news = News.query.filter_by(id=id).first()
    return render_template(
        "content/view_news.html",
        news=news,
    )
