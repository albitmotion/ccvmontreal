from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    BooleanField,
    DateField,
    IntegerField,
    FloatField,
    FileField,
    TextAreaField,
    PasswordField,
    ValidationError,
    SelectField,
)
from wtforms.validators import DataRequired, EqualTo, Length
from flask_ckeditor import CKEditorField


class MemberForm(FlaskForm):
    name = StringField("Name*:", validators=[DataRequired()])
    email = StringField("Email*:", validators=[DataRequired()])
    role = StringField("Role*:", validators=[DataRequired()])
    telephone = StringField("Phone Number:")
    english = BooleanField("English")
    french = BooleanField("French")
    preferable = SelectField(
        "Preferable:",
        choices=[
            ("English", "English"),
            ("French", "French"),
        ],
    )
    organization = StringField("Organization:")
    volunteers = IntegerField("Number Voluntters I manage:")
    member_pic = FileField("Member Pic:")
    update_pw = BooleanField("Update Password:")
    password_hash = PasswordField(
        "Password:",
        validators=[
            DataRequired(),
            EqualTo("password_hash2", message="Passwords Must Match!"),
        ],
    )
    password_hash2 = PasswordField("Confirm Password:", validators=[DataRequired()])
    submit = SubmitField("Submit")


class ExecutiveMemberForm(FlaskForm):
    name = StringField("Name*:", validators=[DataRequired()])
    role = StringField("Role*:", validators=[DataRequired()])
    email = StringField("Email*:", validators=[DataRequired()])
    bio = StringField("Bio:")
    telephone = StringField("Telephone:")
    english = BooleanField("English:")
    french = BooleanField("French:")
    preferable = SelectField('Preferable:', choices=[
            ('English', 'English'),
            ('French', 'French'),
        ])
    organization = StringField("Organization:")
    order = IntegerField("Order:")
    executive_member_pic = FileField("Executive Member Pic:")
    # update_pw = BooleanField("Update Password")
    password_hash = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            EqualTo("password_hash2", message="Passwords Must Match!"),
        ],
    )
    password_hash2 = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class SurveyForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    start = DateField("Start")
    end = DateField("End")
    responders = IntegerField("Responders")
    file = FileField("File")
    submit = SubmitField("Submit")


class MeetingForm(FlaskForm):
    date = DateField("Date", validators=[DataRequired()])
    minute = StringField("Minute")
    attendees = IntegerField("Attendees")
    file = FileField("File")
    submit = SubmitField("Submit")


class MembershipForm(FlaskForm):
    start = DateField("Start")
    end = DateField("End")
    remembered = DateField("Reminded")
    file = FileField("File")
    submit = SubmitField("Submit")


class ActivityForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    # text = TextAreaField("Text", validators=[DataRequired()])
    text = CKEditorField("Text", validators=[DataRequired()])
    date = DateField("Date")
    hour = StringField("Hour")
    address = StringField("Address")
    file = FileField("File")
    filename = StringField("Filename")
    author = StringField("Author")
    submit = SubmitField("Submit")


class NewsForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    type = StringField("Type", validators=[DataRequired()])
    text = CKEditorField("Text", validators=[DataRequired()])
    date = DateField("Date")
    file = FileField("File")
    filename = StringField("Filename")
    author = StringField("Author")
    submit = SubmitField("Submit")


class AnnualReportForm(FlaskForm):
    filename = StringField("Filename")
    file = FileField("File")
    visible = BooleanField("Visible")
    submit = SubmitField("Submit")


class TaskRepartitionFileForm(FlaskForm):
    filename = StringField("Filename")
    file = FileField("File", validators=[DataRequired()])
    author = StringField("Author")
    submit = SubmitField("Submit")


class TaskRepartitionTextForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    # text = StringField("Text", validators=[DataRequired()])
    text = CKEditorField("Text", validators=[DataRequired()])
    author = StringField("Author")
    submit = SubmitField("Submit")


class BannerForm(FlaskForm):
    filename = StringField("Filename")
    file = FileField("File")
    visible = BooleanField("Visible")
    submit = SubmitField("Submit")


class QuoteForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    text = TextAreaField("Text", validators=[DataRequired()])
    author = StringField("Author")
    organization = StringField("Organization")
    visible = BooleanField("Visible")
    fontSize = FloatField("Font Size")
    submit = SubmitField("Submit")
