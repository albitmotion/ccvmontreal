from flask import Flask, request
from app import (
    app,
    db,
    Meetings,
    AddRegister,
    UpdateRegister,
    DeleteRegister,
)
from webforms import MeetingForm


REGISTER_TYPE = "Meeting"
S3_FOLDER = "docs/meetings/"
TEMPLATE_FOLDER = "meetings"


class AddRegisterMeetings(AddRegister):
    def checkIfExists(self):
        self.register = Meetings.query.filter_by(date=self.request.form["date"]).first()
        return self.register

    def createRegister(self):
        self.register = Meetings()
        self.register.date = self.request.form["date"]
        self.register.minute = self.request.files["file"].filename
        self.register.attendees = self.request.form["attendees"]
        self.register.file = self.unique_filename


class UpdateRegisterMeetings(UpdateRegister):
    def updateRegister(self):
        self.register.date = self.form.date.data
        self.register.attendees = self.form.attendees.data
        self.register.file = self.unique_filename
        if self.request.files["file"]:
            self.register.minute = self.request.files["file"].filename


@app.route("/add_meeting", methods=["GET", "POST"])
def add_meeting():
    form = MeetingForm()
    form_fields = [form.date, form.minute, form.attendees, form.file]

    addRegister = AddRegisterMeetings(
        request, form, REGISTER_TYPE, S3_FOLDER, form_fields, TEMPLATE_FOLDER
    )
    return addRegister.returnTemplate()


@app.route("/update_meeting/<int:id>", methods=["GET", "POST"])
def update_meeting(id):
    form = MeetingForm()
    register = Meetings.query.get_or_404(id)

    updateRegister = UpdateRegisterMeetings(
        request, register, form, REGISTER_TYPE, S3_FOLDER, TEMPLATE_FOLDER
    )
    return updateRegister.returnTemplate()


@app.route("/delete_meeting/<int:id>", methods=["GET", "POST"])
def delete_meeting(id):
    register = Meetings.query.get_or_404(id)
    form = MeetingForm()

    deleteRegister = DeleteRegister(
        register, form, REGISTER_TYPE, S3_FOLDER, TEMPLATE_FOLDER
    )
    return deleteRegister.returnTemplate()
