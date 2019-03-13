#user
#1 create a new user
#2 delete an existing user
#3 update existing user's password

from flask import Flask, current_app, request, jsonify
from flask_sqlite3 import SQLite3
import click
from flask.cli import with_appcontext
from flask_bcrypt import Bcrypt
from flask_basicauth import BasicAuth

#Sfrom flask_basicauth import BasicAuth

app = Flask(__name__) #create the Flask app
bcrypt = Bcrypt(app) #bcrypt wrapper
db = SQLite3(app) #sqlite wrapper

# basic auth subclass checks database
def checkAuth(username, password):
    cur = db.connection.cursor()
    cur.execute("SELECT password FROM User WHERE userName = ?", username)
    pw_hash = cur.fetchone()
    if(bcrypt.check_password_hash(pw_hash, password)) == True:
        return True
    else:
        return False

#1 create a new user
@app.route("/user/new", methods=['POST'])
def newUser():
    cur = db.connection.cursor()
    username = request.form.get('username')
    password = request.form.get('password')
    #hash password
    pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    insertUser = (username, pw_hash)
    cur.execute("INSERT INTO User (userName, password) VALUES (?, ?)", insertUser)
    db.connection.commit()
    return jsonify({'Successfully created user' : username}), 201

#2 delete existing user
@app.route("/user", methods=['DELETE'])
def deleteUser():
    cur = db.connection.cursor()
    if (request.authorization):
        username = request.authorization.username
        password = request.authorization.password
        insertArticle = (username, title, body)
    else:
        return jsonify('Unauthorized response'), 401

    #authenticate
    if(checkAuth(username, password) == True):
        #delete user
        cur.execute("DELETE FROM User WHERE userName = ? ", username)
        return jsonify('Successfully deleted user'), 200
    #invalid credentials, return 409
    else:
        return jsonify('Credentials not found'), 409

#3 change existing user's password
@app.route("/user/edit", methods=['PATCH'])
def editUser():
    cur = db.connection.cursor()
    if (request.authorization):
        username = request.authorization.username
        password = request.authorization.password
        insertArticle = (username, title, body)
    else:
        return jsonify('Unauthorized response'), 401

    #authenticate
    if(checkAth(username, password) == True):
        #set new password
        newPassword = request.headers.get('Authorization')
        pw_hash = bcrypt.generate_password_hash(newPassword).decode('utf-8')
        cur.execute("UPDATE User SET (password) VALUES (?) WHERE username = ?", (pw_hash, username))
        db.connection.commit()
        return jsonify('Successfully updated user password'), 200
    else:
        return jsonify('Credentials not found'), 409


if(__name__ == '__main__'):
    app.run(debug=True)
