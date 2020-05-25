from flask import Flask , render_template, request , redirect, jsonify 
from flask_sqlalchemy import SQLAlchemy, Model 
from sqlalchemy import Column , ForeignKey, Integer, String, Boolean,Table
import sys
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1@localhost:5432/ray2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app,db)

# define the relationship in any of the 2 classes it dosn't matter
# backref is the name of the current Class Table that the other one will have
# easy acess through Studnt.courses and Course.students
# deal with it as a normal python list

# secondry table to connect the tables directly to each other
# Study = db.Table("study",db.Column("student_id",Integer,ForeignKey("student.id"),primary_key=True),
#                         db.Column("course_id",Integer,ForeignKey("course.id"),primary_key=True),
#                         db.Column("teacher_id",Integer,ForeignKey("teacher.id"),primary_key=True),
#                         )

class Study(db.Model):
    __tablename__ = "study"
    student_id = db.Column(Integer,ForeignKey("student.id"),primary_key=True)
    course_id = db.Column(Integer,ForeignKey("course.id"),primary_key=True)
    teacher_id = db.Column(Integer,ForeignKey("teacher.id"),primary_key=True)
    
class Student(db.Model):
    id = Column(Integer,primary_key = True)
    name = Column(String(),nullable = False)
    courses = db.relationship("Course",secondary="study"  )
    teachers = db.relationship("Teacher",secondary="study")

    def __repr__(self):
        return '(' + str(self.id) +',' + self.name +')'

class Course(db.Model):
    id = Column(Integer,primary_key = True)
    name = Column(String(),nullable = False)

    students = db.relationship("Student",secondary= "study")
    teachers = db.relationship("Teacher",secondary= "study")

    def __repr__(self):
        return '(' + str(self.id) +',' + self.name +')'

class Teacher (db.Model):
    id = Column(Integer,primary_key = True)
    name = Column(String(),nullable = False)

    students = db.relationship("Student",secondary= "study")
    courses = db.relationship("Course",secondary  = "study")

    def __repr__(self):
        return '(' + str(self.id) +',' + self.name +')'


s1 = Student.query.get(1)
s2 = Student.query.get(2)
t1 = Teacher.query.get(1)
t2 = Teacher.query.get(2)
c1 = Course.query.get(1)
c2 = Course.query.get(2)

newStudy = Study(student_id=s1.id ,course_id = c1.id ,teacher_id= t1.id)
db.session.add(newStudy)
newStudy = Study(student_id=s1.id ,course_id = c2.id ,teacher_id= t1.id)
db.session.add(newStudy)
newStudy = Study(student_id=s2.id ,course_id = c1.id ,teacher_id= t1.id)
db.session.add(newStudy)


print("student1:",s1.courses,s1.teachers)
print("student2:",s2.courses,s2.teachers)
print("course1:",c1.students,c1.teachers)
print("teacher1:",t1.students,t1.courses)

db.session.commit()









# s =  Student.query.get(1)
# s2 =  Student.query.get(2)

# c1 = Course.query.get(1)
# c2 = Course.query.get(2)
# c3 = Course.query.get(3)

# s.courses.append(c1)
# s.courses.append(c2)
# print(s.courses)
# print(s2.courses)
# print(c1.students)
# print(c2.students)
# print(c3.students)

# when you use db.session.add() to add Parent or child , the other is added automatically
# c4 = Course(id = 5, name = 'Game Development')
# s3 = Student(id=33,name='mohaned')
# c4.students.append(s3)
# db.session.add(c4)
