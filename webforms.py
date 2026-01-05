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
from wtforms.validators import DataRequired, NumberRange, EqualTo, Length
from flask_ckeditor import CKEditorField


class MemberForm(FlaskForm):
    name = StringField("Name*:", validators=[DataRequired()])
    email = StringField("Email*:", validators=[DataRequired()])
    role = StringField("Role EN:")
    roleFR = StringField("Role FR:")
    bioEN = StringField("BioEN:")
    bioFR = StringField("BioFR:")
    order = IntegerField("Order:")
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
    organizationEN = StringField("OrganizationEN:")
    organizationFR = StringField("OrganizationFR:")
    volunteers = IntegerField("Number Volunteers I manage:", validators=[NumberRange(min=0, message="Number must be non-negative.")])
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
    member_pic = FileField("Executive Member Pic:")
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
    titleEN = StringField("Title EN", validators=[DataRequired()])
    titleFR = StringField("Title FR", validators=[DataRequired()])
    textEN = CKEditorField("Text EN", validators=[DataRequired()])
    textFR = CKEditorField("Text FR", validators=[DataRequired()])
    date = DateField("Date")
    hourEN = StringField("Hour EN")
    hourFR = StringField("Hour FR")
    addressEN = StringField("Address EN")
    addressFR = StringField("Address FR")
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

class PageForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    url = StringField("url", validators=[DataRequired()])
    textEN = StringField("Text EN")
    textFR = StringField("Text FR")
    submit = SubmitField("Submit")
