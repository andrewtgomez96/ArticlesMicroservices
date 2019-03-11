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
@app.route("/user/new/<username>/<password>", methods=['POST'])
def newUser(username, password):
    cur = db.connection.cursor()
    #hash password
    pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    insertUser = (username, pw_hash)
    cur.execute("INSERT INTO User (userName, password) VALUES (?, ?)", insertUser)
    db.connection.commit()
    return jsonify({'Successfully created user' : username}), 201

#2 delete existing user
@app.route("/user/<username>/<password>", methods=['DELETE'])
def deleteUser(username, password):
    cur = db.connection.cursor()

    #check if user exists in DB
    if(cur.execute("SELECT password FROM User WHERE userName = ?", username)) == 0:
        return jsonify({'User Not found'}), 404
    #authenticate
    elif(check_auth(username, password) == True):
        #delete user
        cur.execute("DELETE FROM User WHERE userName = ? ", username)
        return jsonify({'Successfully deleted user'}), 200
    #invalid credentials, return 409
    else:
        return jsonify({'Credentials not found'}), 409

#3 change existing user's password
@app.route("/user/edit/<username>/<oldPassword>/<newPassword>", methods=['PATCH'])
def editUser(username, oldPassword, newPassword):
    cur = db.connection.cursor()

    #check if user exists
    if(cur.execute("SELECT password FROM User WHERE userName = ? ", username)) == 0:
        return jsonify({'User Not found'}), 404
    #authenticate
    elif(check_auth(username, oldPassword) == True):
        #set new password
        pw_hash = bcrypt.generate_password_hash(newPassword).decode('utf-8')
        cur.execute("UPDATE User SET (password) VALUES (?) WHERE username = ?", (pw_hash, username))
        db.connection.commit()
        return jsonify({'Successfully updated user password'}), 200
    else:
        return jsonify({'Credentials not found'}), 409


if(__name__ == '__main__'):
    app.run(debug=True)