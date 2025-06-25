from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change-me'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assistant.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    client = db.relationship('Client', backref=db.backref('cases', lazy=True))

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('case.id'))
    case = db.relationship('Case', backref=db.backref('documents', lazy=True))
    filename = db.Column(db.String(255))
    text = db.Column(db.Text)

class Template(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    path = db.Column(db.String(255))

admin = Admin(app, name='Legal Assistant', template_mode='bootstrap3')
admin.add_view(ModelView(Client, db.session))
admin.add_view(ModelView(Case, db.session))
admin.add_view(ModelView(Document, db.session))
admin.add_view(ModelView(Template, db.session))

@app.before_first_request
def setup_db():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
