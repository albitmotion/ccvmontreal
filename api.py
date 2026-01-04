from flask import request

from app import (
    app,
    db,
    Members,
    Meetings,
    Memberships,
    News,
    attendance,
    TaskRepartitionTexts,
    s3_client,
)
from flask import jsonify
import json
import csv
from datetime import date


from werkzeug.security import generate_password_hash, check_password_hash


## API------------------------------------------------------


@app.route("/check_login/", methods=["GET", "POST"])
def check_login():
    result = json.loads(request.data)
    user = Members.query.filter_by(email=result["email"]).first()
    print("USER", user)
    if user.category == "Executive Member":
        is_executive_member = True
    else:
        is_executive_member = False

    userDict = {}
    if user:
        if user.verify_password(result["pass"]):
            userDict["id"] = user.id
            userDict["name"] = user.name
            userDict["email"] = user.email
            userDict["is_executive_member"] = is_executive_member
            userDict["s3_root"] = app.config["S3_ROOT"]
            userDict["member_pic"] = user.member_pic
            app.config["CURRENT_USER_ID"] = user.id
            app.config["IS_EXECUTIVE_MEMBER"] = is_executive_member

        else:
            userDict["error"] = "Invalid password"
    else:
        userDict["error"] = "Email not found"
    return userDict, 200


@app.route("/get_member/", methods=["GET", "POST"])
def get_member():
    result = json.loads(request.data)
    member = Members.query.filter_by(email=result["email"]).first()
    memberDict = {}
    if member:
        if member.verify_password(result["pass"]):
            memberDict["id"] = member.id
            memberDict["name"] = member.name
            memberDict["email"] = member.email
            memberDict["role"] = member.role
            memberDict["telephone"] = member.telephone
            memberDict["english"] = member.english
            memberDict["french"] = member.french
            memberDict["preferable"] = member.preferable
            memberDict["organization"] = member.organization
            memberDict["volunteers"] = member.volunteers
            memberDict["member_pic"] = member.member_pic
        else:
            memberDict["error"] = "Invalid password"
    else:
        memberDict["error"] = "Email not found"
    return memberDict, 200


@app.route("/get_member_id/<id>")
def get_member_id(id):
    user = Members.query.filter_by(id=id).first()
    userDict = {}
    userDict["id"] = user.id
    userDict["name"] = user.name
    userDict["email"] = user.email
    userDict["role"] = user.role
    userDict["telephone"] = user.telephone
    userDict["english"] = user.english
    userDict["french"] = user.french
    userDict["preferable"] = user.preferable
    userDict["organization"] = user.organization
    userDict["volunteers"] = user.volunteers
    userDict["member_pic"] = user.member_pic
    return userDict, 200


@app.route("/get_executive_member/", methods=["GET", "POST"])
def get_executive_member():
    result = json.loads(request.data)
    executiveMember = Members.query.filter_by(email=result["email"]).first()
    executiveMemberDict = {}
    if executiveMember:
        if executiveMember.verify_password(result["pass"]):
            executiveMemberDict["id"] = executiveMember.id
            executiveMemberDict["name"] = executiveMember.name
            executiveMemberDict["email"] = executiveMember.email
            executiveMemberDict["role"] = executiveMember.role
            executiveMemberDict["telephone"] = executiveMember.telephone
            executiveMemberDict["english"] = executiveMember.english
            executiveMemberDict["french"] = executiveMember.french
            executiveMemberDict["preferable"] = executiveMember.preferable
            executiveMemberDict["organization"] = executiveMember.organization
            executiveMemberDict["executive_member_pic"] = (
                executiveMember.executive_member_pic
            )
        else:
            executiveMemberDict["error"] = "Invalid password"
    else:
        executiveMemberDict["error"] = "Email not found"
    return executiveMemberDict, 200


@app.route("/get_executive_member_id/<id>")
def get_executive_user_id(id):
    user = Members.query.filter_by(id=id).first()
    userDict = {}
    userDict["id"] = user.id
    userDict["name"] = user.name
    userDict["email"] = user.email
    userDict["role"] = user.role
    userDict["telephone"] = user.telephone
    userDict["english"] = user.english
    userDict["french"] = user.french
    userDict["preferable"] = user.preferable
    userDict["organizationEN"] = user.organizationEN
    userDict["organizationFR"] = user.organizationFR
    userDict["member_pic"] = user.member_pic
    return userDict, 200


@app.route("/get_users")
def get_users():
    app.config["USER"] = user
    return jsonify(user_data), 200


@app.route("/add_likes_news/", methods=["GET", "POST"])
def add_likes_news():
    result = json.loads(request.data)
    news = News.query.filter_by(id=result["id"]).first()
    news.add_like()
    db.session.commit()
    returnVar = {"likes": news.likes}
    return returnVar, 200


@app.route("/change_attendance/", methods=["GET", "POST"])
def change_attendance():
    result = json.loads(request.data)
    meeting = Meetings.query.filter_by(id=result["meeting"]).first()
    member = Members.query.filter_by(id=result["member"]).first()

    returnVar = {}
    if result["checked"]:
        if not member in meeting.member_attendance:
            member.meetings_attendance.append(meeting)
            try:
                db.session.commit()
            except:
                returnVar["error"] = "Not possible to save Meeting Attendance"
    else:
        if member in meeting.member_attendance:
            member.meetings_attendance.remove(meeting)
            try:
                db.session.commit()
            except:
                returnVar["error"] = "Not possible to save Meeting Attendance"
    if not "error" in returnVar:
        returnVar["result"] = "Attendance saved successfully."
    return returnVar, 200


@app.route("/clear_attendance/", methods=["GET", "POST"])
def clear_attendance():
    meetings = Meetings.query.order_by(Meetings.id)
    member = Members.query.filter_by(id=Members.id).first()
    for meeting in meetings:
        #     for member in members:
        if member in meeting.member_attendance:
            member.meetings_attendance = []
            db.session.commit()
    returnVar = {}
    return returnVar, 200


@app.route("/create_initial_user/")
def create_initial_user():
    hashed_pw = generate_password_hash("123", method="pbkdf2:sha256")
    result = []
    executive_member = Members.query.filter_by(
        name="Initial Executive Member"
    ).first()
    if not executive_member:
        executiveMember = Members(
            id=1,
            name="Initial Executive Member",
            email="exec@mail.com",
            role="Initial Executive Member",
            order=1,
            organizationEN="System",
            organizationFR="System",
            password_hash=hashed_pw,
            category="Executive Member",
        )
        db.session.add(executiveMember)
        db.session.commit()
        result.append("Initial Executive Member added successfully.")
    member = Members.query.filter_by(name="Initial Member").first()
    hashed_pw = generate_password_hash("123", method="pbkdf2:sha256")
    if not member:
        member = Members(
            id=2,
            name="Initial Member",
            email="member@mail.com",
            role="Initial Member",
            organizationEN="System",
            organizationFR="System",
            password_hash=hashed_pw,
            category="Member",
        )
        db.session.add(member)
        db.session.commit()
        result.append("Initial Member added successfully.")
    task_repartitionText = TaskRepartitionTexts.query.filter_by(id=1).first()
    if not task_repartitionText:
        task_repartitionText = TaskRepartitionTexts(
            id=1,
            title="Initial Title",
            text="Initial Text",
        )
        db.session.add(task_repartitionText)
        db.session.commit()
        result.append("Initial Task Repartition added successfully.")
    return result, 200


@app.route("/mark_reminded/", methods=["GET", "POST"])
def mark_reminded():
    data = json.loads(request.data)
    print('Mark Reminded', data)
    membership = Memberships.query.filter_by(id=data["membership_id"]).first()
    print("membership", membership)
    membership.remembered = date.today()
    db.session.commit()

    return {'result': 'tudo bem'}

@app.route("/enforce_active_user/", methods=["GET", "POST"])
def enforce_active_user():
    data = json.loads(request.data)
    result = []
    if "userId" in data:
        app.config["CURRENT_USER_ID"] = data["userId"]
        app.config["IS_EXECUTIVE_MEMBER"] = data["isExecutiveMember"]
    else:
        result.append("Not possible to enforce active user")
    return result, 200


@app.route("/download_payment/", methods=["GET", "POST"])
def download_payment():
    data = json.loads(request.data)
    # Data to write to the CSV file
    headers = [
        "Name",
        "Role",
        "Organization",
        "Status",
        "Member Since",
        "Expiration Date",
        "Reminded",
    ]
    rowList = []
    for row in data["csvData"]:
        reminded = ""
        print("row[6]", row[6])
        if "<button class" in row[6]:
            reminded = "Need to remind"
        elif "-" in row[6]:
            print('tem -, quer dizer que precisa limpar')
            reminded = row[6].replace(" ", "").replace("\n", "")
            print("reminded", reminded)
        rowList.append(
            [row[0], row[1], row[2], row[3].split(">")[1][:-3], row[4], row[5], reminded]
        )


    csvfilePath = app.config["DOWNLOAD"] + "payments.csv"
    with open(csvfilePath, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        # Write the header row
        writer.writerow(headers)

        # Write the data rows
        writer.writerows(rowList)
    with open(csvfilePath, "rb") as f:
        s3_client.upload_fileobj(f, "ccvmontreal", "download/payments.csv")

    return {
        "result": "CSV file 'people.csv' created successfully.",
        "url": "https://s3.us-east-2.amazonaws.com/ccvmontreal/download/payments.csv",
    }

@app.route("/download_attendance/", methods=["GET", "POST"])
def download_attendance():
    print('DOWNLOAD ATTENDANCE')
    data = json.loads(request.data)
    print('data', data)
    rowList = []
    for row in data["csvData"]:
        name = ""
        name_split = row[0].split(">")
        if len(name_split) > 1:
            name = name_split[1].split("<")[0]
        colList = []
        for col in row:
            col_clean = ""
            col_split = col.split(">")
            if len(col_split) > 1:
                col_clean = col_split[1].split("<")[0].split("<")[0]
            if "checked" in col:
                col_clean = "Present"
            elif "value" in col:
                col_clean = "Absent"
            if col_clean:
                colList.append(col_clean)
            else:
                colList.append(col)
             # [name, row[1], row[2], row[3]]
        rowList.append(colList)


    csvfilePath = app.config["DOWNLOAD"] + "attendance.csv"
    with open(csvfilePath, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        writer.writerows(rowList)
    with open(csvfilePath, "rb") as f:
        s3_client.upload_fileobj(f, "ccvmontreal", "download/attendance.csv")

    return {
        "result": "CSV file 'people.csv' created successfully.",
        "url": "https://s3.us-east-2.amazonaws.com/ccvmontreal/download/attendance.csv",
    }
