import click, pytest, sys
from flask.cli import with_appcontext, AppGroup
from sqlalchemy.exc import IntegrityError

from App.database import db, get_migrate
from App.models import User, Student, Staff, ConfirmationRequest, Achievement
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    db.drop_all()
    db.create_all()
    bob = Student('111', 0, 'bob', 'bobpass')
    alice = Student('222', 0, 'alice', 'alicepass')
    trudy = Student('333', 0, 'trudy', 'trudypass')
    maisy = Staff('002', 'maisy', 'maisypass')
    trent = Staff('005', 'trent', 'trentpass')
    a1 = Achievement('Completed 10 hours')
    a2 = Achievement('Completed 25 hours!')
    a3 = Achievement('Completed 50 hours!')
    bob.confirmationRequests.append(ConfirmationRequest('23/09/2025', 'Beach Cleanup', 3))
    db.session.add_all([bob, alice, trudy, maisy, trent, a1, a2, a3])
    db.session.commit()
    print('database intialized')

# This command allows Staff to log hours for Student
@app.cli.command("log-hours", help="Allows a staff member to log a student's hours")
def log_hours():
    staff = Staff.query.all()
    print(staff)
    staff_id = input("Enter the staff id of the staff member performing the operation: ")
    staff_member = Staff.query.filter_by(staff_id=staff_id).first()
    if not staff_member:
        print(f'Staff member {staff_id} not found!')
        return
    students = Student.query.all()
    print(students)
    student_id = input("Enter the student id of the student whose hours you wish to log: ")
    student = Student.query.filter_by(student_id=student_id).first()
    if not student:
        print(f'Student {student_id} not found!')
        return
    hours = input("Enter the number of hours to be logged:")
    student.log_hours(hours)
    db.session.add(student)
    db.session.commit()
    print("Hours logged!")

# This command allows Student to make ConfirmationRequest
@app.cli.command("make-request", help="A student can request the confirmation of hours by a staff member")
def make_request():
    students = Student.query.all()
    print(students)
    student_id = input("Enter the student id of the student requesting confirmation: ")
    student = Student.query.filter_by(student_id=student_id).first()
    if not student:
        print(f'Student {student_id} not found!')
        return
    dateOfService = input("Please enter the date of the hours worked (format: DD/MM/YYYY): ")
    activity = input("Please enter the name of the community service/volunteering activity: ")
    hours = input("Please enter the number of hours worked: ")
    newConfirmationRequest = ConfirmationRequest(dateOfService, activity, hours)
    student.confirmationRequests.append(newConfirmationRequest)
    print("Request received!")
    db.session.add(student)
    db.session.commit()

# Staff approves confirmation request
@app.cli.command("confirm-hours", help="Allows a staff member to approve a student's confirmation request")
def confirm_hours():
    staff = Staff.query.all()
    print(staff)
    staff_id = input("Enter the staff id of the staff member performing the operation: ")
    staff_member = Staff.query.filter_by(staff_id=staff_id).first()
    if not staff_member:
        print(f'Staff member {staff_id} not found!')
        return
    status='Pending'
    confirmationRequests = ConfirmationRequest.query.filter_by(status=status).all()
    if not confirmationRequests:
        print(f'No pending requests')
        return
    print(confirmationRequests)
    request_id = input("Please enter the id of the request you want to approve or deny: ")
    confirmationRequest = ConfirmationRequest.query.get(request_id)
    if not confirmationRequest:
        print(f'Request {request_id} not found!')
        return
    approve = input("Approve request? (Y/N): ")
    if approve == 'Y' or 'y':
        confirmationRequest.status = 'Approved'
        student = Student.query.get(confirmationRequest.student_id)
        student.log_hours(confirmationRequest.hours)
        print("Request approved!")
    else:
        confirmationRequest.status = 'Rejected'
        print("Request denied!")
    db.session.add_all([confirmationRequest, student])
    db.session.commit()

# View Student leaderboard
@app.cli.command("view-leaderboard", help="Shows a student leadboard based on hours worked")
def view_leaderboard():
    students = Student.query.all()
    students.sort(key=lambda s: s.hours, reverse=True)
    i = 1
    for student in students:
        print(f'<Rank {i} - {student.username} (Student ID: {student.student_id}) (Hours: {student.hours})>')
        i = i + 1

# View Student Achievements
@app.cli.command("view-achievements", help="Shows the achievements for a particular user")
def view_achievements():
    students = Student.query.all()
    print(students)
    student_id = input("Please enter the id of the student whose achievements you'd like to view: ")
    student = Student.query.filter_by(student_id=student_id).first()
    if not student:
        print(f'Student {student_id} not found!')
        return
    print(student.achievements)

# Create new Student
@app.cli.command("create-student", help="Create a new student record")
def create_student():
    id = input("Please enter the student's id: ")
    username = input("Please enter the student's username: ")
    password = input("Please enter the student's password: ")
    hours = input("Please enter the hours worked by the student: ")
    new_student = Student(id, hours, username, password)
    try:
        db.session.add(new_student)
        db.session.commit()
        print(new_student)
    except IntegrityError as e:
        db.session.rollback()

# View all instances of Student
@app.cli.command("list-students", help="Lists all student records")
def list_students():
    students = Student.query.all()
    print(students)

#Create new Staff
@app.cli.command("create-staff", help="Create a new staff record")
def create_staff():
    id = input("Please enter the staff member's id: ")
    username = input("Please enter the staff member's username: ")
    password = input("Please enter the staff member's password: ")
    new_staff = Staff(id, username, password)
    try:
        db.session.add(new_staff)
        db.session.commit()
        print(new_staff)
    except IntegrityError as e:
        db.session.rollback()

# View all instances of Staff
@app.cli.command("list-staff", help="Lists all staff records")
def list_staff():
    staff = Staff.query.all()
    print(staff)