import os
from flask import Flask
from flask import render_template
from flask import request,redirect
from flask_sqlalchemy import SQLAlchemy

#---------------------------------------------------------------------------------------------#
current_dir= os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"+ os.path.join(current_dir,"database.sqlite3")


db= SQLAlchemy()
db.init_app(app)
app.app_context().push()
#---------------------------------------------------------------------------------------------#
class Student(db.Model):
    __tablename__='student'
    student_id = db.Column(db.Integer, primary_key=True, autoincrement= True)
    roll_number = db.Column(db.String, unique= True, nullable= False)
    first_name = db.Column(db.String, nullable= False)
    last_name = db.Column(db.String)
    courses=db.relationship("Course",secondary="enrollments")

class Course(db.Model):
    __tablename__='course'
    course_id = db.Column(db.Integer, primary_key=True, autoincrement= True)
    course_code = db.Column(db.String, unique= True, nullable= False)
    course_name = db.Column(db.String, nullable= False)
    course_description = db.Column(db.String)

class Enrollments(db.Model):
    __tablename__='enrollments'
    enrollment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    estudent_id= db.Column(db.Integer, db.ForeignKey("student.student_id"), nullable=False)
    ecourse_id= db.Column(db.Integer, db.ForeignKey("course.course_id"), nullable=False)
#--------------------------------ALL STUDENT DETAILS-------------------------------------------#
@app.route('/', methods=["GET","POST"])
def index():
    if request.method=="GET":
        students = Student.query.all()
        return render_template("index.html",students=students)
#------------------------------CREATE NEW STUDENT----------------------------------------------#
@app.route('/student/create', methods=["GET","POST"])
def create_student():
    if request.method=="GET":
        return render_template("form.html")
    else:
        roll_no= request.form.get('roll')
        f_name= request.form.get('f_name')
        l_name= request.form.get('l_name')
        course=request.form.getlist('courses')
        student_record=Student(roll_number=roll_no,first_name=f_name,last_name=l_name)
        for c in course:
            if c=='course_1':
                student_enroll=Enrollments(estudent_id=roll_no,ecourse_id="CSE01")
                db.session.add(student_enroll)
            if c=='course_2':
                student_enroll=Enrollments(estudent_id=roll_no,ecourse_id="CSE02")
                db.session.add(student_enroll)
            if c=='course_3':
                student_enroll=Enrollments(estudent_id=roll_no,ecourse_id="CSE03")
                db.session.add(student_enroll)
            if c=='course_4':
                student_enroll=Enrollments(estudent_id=roll_no,ecourse_id="BST13")
                db.session.add(student_enroll)
        try:
            db.session.add(student_record)
            db.session.commit()
            return redirect('/')
        except:
            return render_template("error.html")
#--------------------------------------DISPLAY STUDENT DETAILS-----------------------------------#
@app.route('/student/<roll_no>', methods=["GET","POST"])
def display(roll_no):
    student_details = db.session.query(Student).filter(Student.roll_number==roll_no).one()
    enroll_details = db.session.query(Enrollments).filter(Enrollments.estudent_id==roll_no).all()
    l=[]  #l stores all courses taken by a student in enrollments table.
    for enroll in enroll_details:
        l.append(enroll.ecourse_id)
    course_details = db.session.query(Course).filter(Course.course_code.in_(l)).all()

    return render_template("display.html",student=student_details,enroll=course_details)
#----------------------------------------UPDATE STUDENT DETAILS----------------------------------#

@app.route('/student/<roll>/update', methods=["GET","POST"])
def update(roll):
    if request.method=="GET":
        student_details= db.session.query(Student).filter(Student.roll_number==roll).one()
        enroll_details = db.session.query(Enrollments).where(Enrollments.estudent_id==roll).all()
        l=[]
        for enroll in enroll_details:
            l.append(enroll.ecourse_id)
        course_details = db.session.query(Course).filter(Course.course_code.in_(l)).all()
        return render_template("update.html",student=student_details,course=course_details)
    else:
        f_name=request.form.get('f_name')
        l_name=request.form.get('l_name')
        course=request.form.getlist('courses')
        student= db.session.query(Student).filter(Student.roll_number==roll).one()
        student.first_name=f_name
        student.last_name=l_name
        enroll_details = db.session.query(Enrollments).where(Enrollments.estudent_id==roll).all()
        for enroll in enroll_details:
            db.session.delete(enroll)
        db.session.commit()
        for c in course:
            if c=='course_1':
                student_enroll=Enrollments(estudent_id=roll,ecourse_id="CSE01")
                db.session.add(student_enroll)
            if c=='course_2':
                student_enroll=Enrollments(estudent_id=roll,ecourse_id="CSE02")
                db.session.add(student_enroll)
            if c=='course_3':
                student_enroll=Enrollments(estudent_id=roll,ecourse_id="CSE03")
                db.session.add(student_enroll)
            if c=='course_4':
                student_enroll=Enrollments(estudent_id=roll,ecourse_id="BST13")
                db.session.add(student_enroll)
        db.session.commit()

        return redirect('/')

#----------------------------------------DELETE STUDENT DETAILS----------------------------------#

@app.route('/student/<roll>/delete', methods=["GET","POST"])
def delete(roll):
    student_details=db.session.query(Student).filter(Student.roll_number==roll).one()
    enroll_details = db.session.query(Enrollments).where(Enrollments.estudent_id==roll).all()
    for enroll in enroll_details:
        db.session.delete(enroll)
    db.session.delete(student_details)
    db.session.commit()
    return redirect('/')


#---------------------------------------------------------------------------------------------#
if __name__=='__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)    
