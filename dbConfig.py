from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from app import db
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///usersDB.sqlite'
app.config['SQLALCHEMY_BINDS'] = {'articles' : 'sqlite://///articleDB.sqlite',
                                    'tags' : 'sqlite://///tagDB.sqlite',
                                    'comments' : 'sqlite:////commentDB.sqlite'}

db = SQLAlchemy(app)
class User(db.Model):
    userId = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25))
    password = db.Column(db.String(25))

class Article(db.Model):
    __bind_key__ = "articles"
    username = db.Column(db.String(25))
    artId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40))
    body = db.Column(db.String(240))
    created = db.Column(db.DateTime)
    modified = db.Column(db.DateTime)

class Tag(db.Model):
    __bind_key__ = "tags"
    tagId = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25))
    title = db.Column(db.String(40))
    body = db.Column(db.String(240))
    tag = db.Column(db.String(20))
    artId = db.Column(db.Integer)
    created = db.Column(db.DateTime)

class Comment(db.Model):
    __bind_key__ = "comments"
    username = db.Column(db.String(25), default="anonymous coward")
    commendId = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(180))
    artId = db.Column(db.Integer)
    created = db.Column(db.DateTime)

if __name__ == '__main__':
    app.run(debug=True)
