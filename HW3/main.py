import os
from flask import Flask, render_template, session, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField, IntegerField, TextField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY']='oursecretkey'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRAC_MODIFICATIONS']=False

db=SQLAlchemy(app)

class student(db.Model):
    __tablename__="students"

    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.Text)
    grade= db.Column(db.Integer)

    def __init__(self,name,grade):
        self.name=name
        self.grade=grade
    def __repr__(self):
        return f"Student {self.name} has an {self.grade}"

class MyForm(FlaskForm):
    name=TextField('Enter name:')
    grade=IntegerField('Enter grade:')
    submit=SubmitField('Add')
db.create_all()
@app.route('/', methods=['GET','POST'])
def index():
    form= MyForm()
    if form.validate_on_submit():
        lname = form.name.data
        lgrade = form.grade.data
        new = print(student(lname,lgrade))
        db.session.add(new)
        db.session.commit()
    return render_template('home.html', form=form,)
@app.route('/report')
def report():
    return render_template('results.html')

if __name__ == '__main__':
    app.run(debug=True)