#article
#1 posting a new article
#2 retrieve an existing article
#3 edit an existing article (update TIMESTAMP)
#4 delete an existing article
#5 retrieve contents of n most recent getArticles
#6 retrieve metadata for an article

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

# 1 function for posting single article
@app.route("/article/new/<title>/<body>", methods=['POST'])
def newArticle(title, body):
    cur = db.connection.cursor()
    if (request.authorization):
        username = request.authorization.username
        password = request.authorization.password
        insertArticle = (username, title, body)
    else:
        return jsonify('Unauthorized response'), 401
    #authenticate
    if(checkAuth(username, password) == True):
        #add article
        cur.execute("INSERT INTO Article (userName, title, body, created) VALUES (?, ?, ?,?)", (insertArticle, CURRENT_TIMESTAMP))
        db.connection.commit()
        return jsonify({'Successfully created article' : articleId}), 201
    else:
        return jsonify('Credentials not found'), 409

#2 retrieve existing article
@app.route("/article/<int:articleId>/title", methods=['GET']) #allow both GET and POST requests
def getArticle(articleId):
    cur = db.connection.cursor()

    #check if articleId exists in DB
    cur.execute("SELECT (title, body) FROM Article WHERE artId = ? ", articleId)
    returnObject = cur.fetchone()
    if(returnObject):
        cur.execute("SELECT (title, body) FROM Article WHERE artID = ? ", articleId)
        article = cur.fetchone()[0]
        return jsonify(article), 200
    else:
        return jsonify('Article Not found'), 404

#3 edit existing article
@app.route("/article/<int:articleId>/<title>/<body>", methods=['PATCH'])
def editArticle(articleId, title, body):
    cur = db.connection.cursor()
    if (request.authorization):
        username = request.authorization.username
        password = request.authorization.password
        insertArticle = (username, title, body)
    else:
        return jsonify('Unauthorized response'), 401

    #check if article exists
    #authenticate
    if(checkAuth(username, password) == True):
        cur.execute("SELECT (title, body) FROM Article WHERE artID = ? ", articleId)
        returnObject = cur.fetchone()
        if(returnObject):
            cur.execute("UPDATE Article SET (userName, title, body, modified) VALUES (?, ?, ?, ?) WHERE artID = ?", (insertArticle, CURRENT_TIMESTAMP, articleId))
            db.connection.commit()
            return jsonify({'Successfully edited article' : articleId}), 200
        else:
            return jsonify('Not found'), 404
    else:
        return jsonify('Credentials not found'), 409

#4  delete and existing article
@app.route("/article/<int:articleId>", methods=['DELETE']) #allow both GET and POST requests
def deleteArticle(articleId):
    cur = db.connection.cursor()
    if (request.authorization):
        username = request.authorization.username
        password = request.authorization.password
        insertArticle = (username, title, body)
    else:
        return ('Unauthorized response'), 401
    #check if articleId exists in DB
    #authenticate
    if(checkAuth(username, password) == True):
        cur.execute("SELECT (title, body) FROM Article WHERE artId = ? ", articleId)
        returnObject = cur.fetchone()
        if(returnObject):
            #Delete article
            cur.execute("DELETE FROM article WHERE artID = ?", articleId)
            db.connection.commit()
            return jsonify({'Successfully deleted article' : articleId}), 200
        else:
            jsonify('Article Not found'), 404
    else:
        return jsonify('Credentials not found'), 409

#5 retrieve contents of n most recent articles
@app.route("/articles/<int:n>", methods=['GET']) #allow both GET and POST requests
def getArticles(n):
    cur = db.connection.cursor()

    #Retrieve n most recent articles
    cur.execute("SELECT (title, body) FROM Article ORDER BY created DESC LIMIT ? ", n)
    artciles = fetchone()
    return jsonify(articles), 200

#6 retrieve meta data of n most recent articles
@app.route("/articles/info/<int:n>", methods=['GET']) #allow both GET and POST requests
def getMetaArticles(n):
    cur = db.connection.cursor()

    #Retrieve n most recent articles
    cur.execute("SELECT (userName, title, body, created, url) FROM Article ORDER BY created DESC LIMIT ? ", n)
    artciles = fetchone()
    return jsonify(articles), 200



if(__name__ == '__main__'):
    app.run(debug=True)
