from flask import Flask
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1@localhost:5432/ray2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String())

    def __repr__(self):
        return f'(Student ID: {self.id}, name: {self.name})'

class Course(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String())
    sid = db.Column(db.Integer,db.ForeignKey('student.id'))
    def __repr__(self):
        return f'(Course ID: {self.id}, name: {self.name})'

print('....',Course.query.count() )
print('....',Student.query.count() )
print('....',Student.query.get(33) )

query = Student.query.filter(Student.id == 65)
if(query.count()):
    query.delete()
    print('deleted')

print('....',Course.query.count() )
print('....',Student.query.count() )

print('******* Join *********')
# it puts the join condition from itself , to see that: print the query print(joined)
joined = db.session.query(Course).join(Student)
print('joined: ',joined.all())
db.session.commit()


# Edit
print(".............")
s = Student.query.filter(Student.id == 3).first()
s.name = 'editedName'


# db.session.commit()
# db.create_all()
if __name__ == "__main__":
    app.run()
