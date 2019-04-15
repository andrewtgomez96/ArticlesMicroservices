#user
#1 create a new user
#2 delete an existing user
#3 update existing user's password

from flask import Flask, request, jsonify
import click, json
from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext
from dbConfig import db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_bcrypt import Bcrypt
from flask_basicauth import BasicAuth

app = Flask(__name__) #create the Flask app
db = SQLAlchemy(app)

'''
if you run 'flask init-db-command' it will create the articles database from the dbconfig file
'''
@app.cli.command()
@with_appcontext
def init_db_command():
    print("Clear the existing data and create new tables.")
    init_db()
    click.echo('Initialized the database.')

def init_db():
    db.create_all(bind='articles')
    engine = create_engine ('sqlite:///userDB.db')
    connection = engine.connect()
    Session = sessionmaker(bind=engine)

# basic auth subclass checks database
def checkAuth(username, password):
    session = Session()
    pw_hash = User.query.filter_by(username = username).first()
    if(bcrypt.check_password_hash(pw_hash[0], password) == True):
        return True
    else:
        return False

#1 create a new user
@app.route("/user/new", methods=['POST'])
def newUser():
    session = Session()
    username = request.form.get('username')
    password = request.form.get('password')
    #hash password
    pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    insertUser = User(username = username, password = pw_hash)
    db.session.add(insertUser)
    db.session.commit()
    db.session.close()
    return jsonify({'Successfully created user' : username}), 201

#2 delete existing user
@app.route("/user", methods=['DELETE'])
def deleteUser():
    session = Session()
    if (request.authorization):
        username = request.authorization.username
        password = request.authorization.password
    else:
        db.session.rollback()
        return jsonify('Unauthorized response'), 401

    #authenticate
    if(checkAuth(username, password) == True):
        #delete user
        u = User.query.filter_by(username = username).first()
        db.session.delete(u)
        db.session.commit()
        db.session.close()
        return jsonify('Successfully deleted user'), 200
    #invalid credentials, return 409
    else:
        db.session.rollback()
        return jsonify('Credentials not found'), 409

#3 change existing user's password
@app.route("/user/edit", methods=['PATCH'])
def editUser():
    session = Session()
    newPassword = request.form.get('password')
    if (request.authorization):
        username = request.authorization.username
        password = request.authorization.password
    else:
        db.session.rollback()
        return jsonify('Unauthorized response'), 401

    #authenticate
    if(checkAuth(username, password) == True):
        #set new password
        pw_hash = bcrypt.generate_password_hash(newPassword).decode('utf-8')
        u = User.query.filter_by(username = username).first()
        u.password = pw_hash
        db.session.commit()
        db.session.close()
        return jsonify('Successfully updated user password'), 200
    else:
        db.session.rollback()
        return jsonify('Credentials not found'), 409


if(__name__ == '__main__'):
    app.run(debug=True)
