from flask import Flask, render_template, jsonify, flash, request
from flask_sqlalchemy import SQLAlchemy

from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor

from webforms import MemberForm, ExecutiveMemberForm, SurveyForm, MeetingForm

# from routes.members import members_page
# from yourapplication.simple_page import simple_page

from sqlalchemy import desc
from flask_migrate import Migrate

from flask_wtf.file import FileField
from datetime import datetime, timedelta
from datetime import date
import json
import random

from werkzeug.utils import secure_filename
import uuid as uuid
import os


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, DateField, IntegerField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash


import os
import boto3
import json


os.environ["AWS_DEFAULT_REGION"] = "us-east-2"
bucket_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": f"arn:aws:s3:::ccvmontreal/*",
        }
    ],
}

s3_client = boto3.client("s3")
s3_client.put_bucket_policy(Bucket="ccvmontreal", Policy=json.dumps(bucket_policy))


app = Flask(__name__)
ckeditor = CKEditor(app)
app.config["S3"] = s3_client

if app.debug:
    UPLOAD_FOLDER = "static/upload/"
    app.config["S3_BASE_FOLDER"] = "dev/"
    app.config["S3_ROOT"] = "https://s3.us-east-2.amazonaws.com/ccvmontreal/dev"
    app.config["DOWNLOAD"] = "static/download/"
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "mysql+pymysql://root:password123@localhost/cvv"
    )
else:
    UPLOAD_FOLDER = "/app/static/upload/"
    app.config["S3_BASE_FOLDER"] = "prod/"
    app.config["S3_ROOT"] = "https://s3.us-east-2.amazonaws.com/ccvmontreal/prod"
    app.config["DOWNLOAD"] = "/home/albitmotion/temp/"
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "mysql+pymysql://albitmotion:zL3)G01w@albitmotion.mysql.pythonanywhere-services.com/albitmotion$ccvmontreal"
    )
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ucocfesi3a50sp:pd433ef3bdce54e70213c225eeb3635b196db7de24db82f7bad98f30d35820253@c34u0gd6rbe7bo.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d6eq465ijvjihi'

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["CURRENT_USER_ID"] = None
app.config["IS_EXECUTIVE_MEMBER"] = None
app.config["SECRET_KEY"] = "secretKey"

db = SQLAlchemy(app)
with app.app_context():
    db.create_all()
migrate = Migrate(app, db)


attendance = db.Table(
    "attendance",
    db.Column("member_id", db.Integer, db.ForeignKey("members.id")),
    db.Column("meeting_id", db.Integer, db.ForeignKey("meetings.id")),
)


# Database Model
class Members(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(70), nullable=False)
    email = db.Column(db.String(50))
    telephone = db.Column(db.String(20))
    english = db.Column(db.Boolean)
    french = db.Column(db.Boolean)
    preferable = db.Column(db.String(100))
    organization = db.Column(db.String(100))
    volunteers = db.Column(db.Integer)
    member_since = db.Column(db.DateTime)
    member_pic = db.Column(db.String(400), nullable=True)
    password_hash = db.Column(db.String(128))
    meetings_attendance = db.relationship(
        "Meetings", secondary=attendance, backref="member_attendance"
    )

    @property
    def password(self):
        raise AttributeError("Password is not readable attribute!")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # expiration_date = db.Column(db.DateTime)
    # an user can have many docs
    documents = db.relationship("Memberships", backref="membership")

    def __repr__(self):
        return "<Name %r>" % self.name


class ExecutiveMembers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(70))
    bio = db.Column(db.String(500))
    email = db.Column(db.String(50), nullable=False)
    telephone = db.Column(db.String(20))
    english = db.Column(db.Boolean)
    french = db.Column(db.Boolean)
    preferable = db.Column(db.String(100))
    organization = db.Column(db.String(100))
    order = db.Column(db.Integer)
    executive_member_pic = db.Column(db.String(400), nullable=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError("Password is not readable attribute!")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<Name %r>" % self.name


# Database Model
class Surveys(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    start = db.Column(db.Date)
    end = db.Column(db.Date)
    responders = db.Column(db.Integer)
    file = db.Column(db.String(400), nullable=True)

    def __repr__(self):
        return "<Name %r>" % self.title


class Meetings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    minute = db.Column(db.String(200))
    attendees = db.Column(db.Integer)
    file = db.Column(db.String(400), nullable=True)

    def __repr__(self):
        return "<Name %r>" % self.date


class Memberships(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    start = db.Column(db.Date)
    end = db.Column(db.Date)
    remembered = db.Column(db.Date)
    member_id = db.Column(db.Integer, db.ForeignKey("members.id"))
    file = db.Column(db.String(400), nullable=True)

    def __repr__(self):
        return "<Name %r>" % self.name


class Activities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date)
    hour = db.Column(db.String(100))
    address = db.Column(db.String(200))
    file = db.Column(db.String(400))
    filename = db.Column(db.String(200))
    author = db.Column(db.String(100))

    def __repr__(self):
        return "<Name %r>" % self.title


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date)
    file = db.Column(db.String(400))
    author = db.Column(db.String(100))
    type = db.Column(db.String(100))

    def add_like(self):
        self.likes += 1
        return True

    def __repr__(self):
        return "<Name %r>" % self.title


class AnnualReports(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200))
    file = db.Column(db.String(400))
    visible = db.Column(db.Boolean)

    def __repr__(self):
        return "<Title %r>" % self.title


class TaskRepartitionFiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200))
    file = db.Column(db.String(400))
    author = db.Column(db.String(100))

    def __repr__(self):
        return "<Title %r>" % self.title


class TaskRepartitionTexts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    text = db.Column(db.Text)
    author = db.Column(db.String(100))

    def __repr__(self):
        return "<Title %r>" % self.title


class Banners(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200))
    file = db.Column(db.String(400))
    visible = db.Column(db.Boolean)

    def __repr__(self):
        return "<Title %r>" % self.title


class Quotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    text = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100))
    organization = db.Column(db.String(200))
    visible = db.Column(db.Boolean)
    fontSize = db.Column(db.Float)

    def __repr__(self):
        return "<Title %r>" % self.title


## ERROR -----------------------------------------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template("errors/500.html"), 500


def get_payment_status(last_membership):
    result = {}
    today = date.today()
    status = "Membership Not Found"
    expiration_date = ""
    warning_icon = False
    if last_membership:
        diff = today - last_membership.end
        expiration_date = last_membership.end
        if last_membership.end > today:
            status = "Paid"
            if diff > timedelta(days=-30):
                status = "Almost Expired"
        else:
            status = "Expired"

        if status == "Almost Expired":
            warning_icon = True
            if last_membership.remembered:
                warning_icon = False
            if not last_membership.remembered:
                warning_icon = True
    result["status"] = status
    result["warning_icon"] = warning_icon
    result["expiration_date"] = expiration_date
    if last_membership:
        result["remembered"] = last_membership.remembered
    else:
        result["remembered"] = 0
    return result


def save_file(file, folderName):
    # Save file name to database
    secure_filename_var = secure_filename(file.filename)
    unique_filename = str(uuid.uuid1()) + "_" + secure_filename_var

    filename_s3 = app.config["S3_BASE_FOLDER"] + folderName + unique_filename
    s3_client.upload_fileobj(file, "ccvmontreal", filename_s3)
    return unique_filename


def delete_file(object_key):
    try:
        bucket_name = "ccvmontreal"
        response = s3_client.delete_object(
            Bucket=bucket_name, Key=app.config["S3_BASE_FOLDER"] + object_key
        )
        print(
            f"Object '{object_key}' deleted successfully from bucket '{bucket_name}'."
        )
    except:
        print(f"Not possible to delete {object_key}")


class AddRegister:
    def __init__(
        self,
        request,
        form,
        register_type,
        s3_folder,
        form_fields,
        template_folder,
        file_field="file",
        member_id=None,
    ):
        self.request = request
        self.form = form
        self.register_type = register_type
        self.s3_folder = s3_folder
        self.form_fields = form_fields
        self.template_folder = template_folder
        self.file_field = file_field
        self.member_id = member_id

    def returnTemplate(self):
        if self.form.validate_on_submit():
            if not self.checkIfExists():
                self.saveInS3()
                self.createRegister()
                db.session.add(self.register)
                db.session.commit()

                for field in self.form_fields:
                    field.data = ""

                flash(f"{self.register_type} added successfully!")
            else:
                flash(
                    f"Error: Already exists a {self.register_type.lower()} with this title."
                )
        return render_template(
            f"{self.template_folder}/add_{self.register_type.lower().replace(" ", "_")}.html",
            form=self.form,
            member_id=self.member_id,
        )

    def checkIfExists(self):
        pass

    def saveInS3(self):
        # Save file in s3 and database
        self.unique_filename = ""
        if self.file_field:
            if self.request.files[self.file_field]:
                self.unique_filename = save_file(
                    self.request.files[self.file_field], self.s3_folder
                )

    def createRegister(self):
        pass


class UpdateRegister:
    def __init__(
        self,
        request,
        register,
        form,
        register_type,
        s3_folder,
        template_folder,
        file_field="file",
    ):
        self.request = request
        self.register = register
        self.form = form
        self.register_type = register_type
        self.s3_folder = s3_folder
        self.template_folder = template_folder
        self.file_field = file_field

    def returnTemplate(self):
        if self.request.method == "POST":
            self.unique_filename = ""
            if self.file_field:
                if self.request.files[self.file_field]:
                    if self.file_field == "file":
                        if self.register.file:
                            delete_file(self.s3_folder + self.register.file)
                    elif self.file_field == "member_pic":
                        if self.register.member_pic:
                            delete_file(self.s3_folder + self.register.member_pic)
                    elif self.file_field == "executive_member_pic":
                        if self.register.executive_member_pic:
                            delete_file(
                                self.s3_folder + self.register.executive_member_pic
                            )
                    self.unique_filename = save_file(
                        self.request.files[self.file_field], self.s3_folder
                    )
                    self.register.filename = self.request.files[
                        self.file_field
                    ].filename
                    self.register.file = self.unique_filename

            self.updateRegister()

            try:
                db.session.commit()

                flash(f"{self.register_type} updated successfully!")
            except:
                flash(f"Error: Not possible to update {self.register_type.lower()}.")
        deletable = False
        if app.config["IS_EXECUTIVE_MEMBER"]:
            deletable = True
        return render_template(
            f"{self.template_folder}/update_{self.register_type.lower().replace(" ", "_")}.html",
            form=self.form,
            register_to_update=self.register,
            s3_root=app.config["S3_ROOT"],
            deletable=deletable,
        )

    def updateRegister(self):
        pass


#
#
#
#
# def update_register(
#     request,
#     register,
#     form,
#     register_type,
#     s3_folder,
#     template_folder,
#     file_field="file",
# ):
#     if request.method == "POST":
#         unique_filename = ""
#         if request.files[file_field]:
#             if register.file:
#                 delete_file(s3_folder + register.file)
#             unique_filename = save_file(form.file.data, s3_folder)
#             register.file = unique_filename
#             register.filename = request.files[file_field].filename
#
#         # REDO THIS EVENTUALLY
#         if register_type == "News":
#             register.text = request.form.get("ckeditor")
#             register.date = form.date.data
#             register.author = form.author.data
#             register.title = form.title.data
#             register.type = form.type.data
#
#         # if register_type == "Task Repartition":
#
#         if register_type == "Member":
#             register.name = form.name.data
#             register.role = form.role.data
#             register.email = form.email.data
#             register.telephone = form.telephone.data
#             register.organization = form.organization.data
#             register.volunteers = form.volunteers.data
#             # register.english = form.english.data
#             # register.french = form.french.data
#             # register.preferable = form.preferable.data
#             if unique_filename:
#                 register.member_pic = unique_filename
#         if register_type == "Meeting":
#             register.date = form.date.data
#             register.attendees = form.attendees.data
#             register.file = unique_filename
#             if request.files["file"]:
#                 register.minute = request.files["file"].filename
#         try:
#             db.session.commit()
#
#             flash(f"{register_type} updated successfully!")
#             # return render_template(
#             #     "content/update_news.html", form=form, news_to_update=register_to_update
#             # )
#         except:
#             flash(f"Error: Not possible to update {register_type.lower()}.")
#             # return render_template(
#             #     "content/update_news.html", form=form, news_to_update=register_to_update
#             # )
#     # else:
#     return render_template(
#         f"{template_folder}/update_{register_type.lower().replace(" ", "_")}.html",
#         form=form,
#         register_to_update=register,
#         s3_root=app.config["S3_ROOT"],
#     )


class DeleteRegister:
    def __init__(
        self,
        register,
        form,
        register_type,
        s3_folder,
        template_folder,
        file_field="file",
    ):
        self.register = register
        self.form = form
        self.register_type = register_type
        self.s3_folder = s3_folder
        self.template_folder = template_folder
        self.file_field = file_field

    def returnTemplate(self):
        try:
            self.deleteDependencies()

            db.session.delete(self.register)
            db.session.commit()

            if self.file_field:
                if self.file_field == "file":
                    if self.register.file:
                        delete_file(self.s3_folder + self.register.file)
                elif self.file_field == "member_pic":
                    if self.register.member_pic:
                        delete_file(self.s3_folder + self.register.member_pic)
                elif self.file_field == "executive_member_pic":
                    if self.register.executive_member_pic:
                        delete_file(self.s3_folder + self.register.executive_member_pic)



            flash(f"{self.register_type} deleted successfully!")
            return render_template("content/empty.html")

        except:
            flash(f"Error: Not possible to delete {self.register_type.lower()}.")
        return render_template(
            f"{self.template_folder}/update_{self.register_type.lower().replace(" ", "_")}.html",
            form=self.form,
            register_to_update=self.register,
        )



    def deleteDependencies(self):
        pass


def get_background():
    backgrounds = [
        "background_01.jpg",
        "background_02.jpg",
        "background_03.jpg",
        "background_04.jpg",
        "background_05.jpg",
    ]
    return random.choice(backgrounds)


# import declared routes
import general, members, executive_members, memberships, meetings, surveys, api, activities, annualReports, banners, news, quotes, taskRepartition

if __name__ == "__main__":
    app.run()
