#1 posting a new article
#2 retrieve an existing article
#3 edit an existing article (update TIMESTAMP)
#4 retrieve contents of n most recent getArticles
#5 retrieve metadata for an article

from flask import Flask, current_app, request, jsonify
from flask_sqlite3 import SQLite3
import click
from flask.cli import with_appcontext

app = Flask(__name__)
db = SQLite3(app)
#Sfrom flask_basicauth import BasicAuth

app = Flask(__name__) #create the Flask app

#function for posting and editing a single article
@app.route("/article/<int:articleId>/<title>/<body>", methods=['POST', 'PATCH']) #allow both GET and POST requests
def editArticle(articleId, title, body):
    cur = db.connection.cursor()
    userName = request.form.get('userName')

    if request.method == 'POST':
        insertArticle = (userName, title, body)
        cur.execute("INSERT INTO Article (userName, title, body, created) VALUES (?, ?, ?, 0)", insertArticle)
        db.connection.commit()
        return jsonify(artId), 201

    elif request.method == 'PATCH':
        insertArticle = (userName, title, body)

        #check if article exists
        if(cur.execute("SELECT (title, body) FROM Article WHERE artID = ? ", articleId)) == 0:
            return jsonify({'Not found'}), 404
        else:
            cur.execute("UPDATE Article SET (userName, title, body, modified) VALUES (?, ?, ?, 0) WHERE artID = ?", (insertArticle, articleId))
            db.connection.commit()
            return jsonify(artId), 201

#2 & 3
@app.route("/article/<int:articleId>/title", methods=['GET', 'DELETE']) #allow both GET and POST requests
def getArticle(articleId):
    cur = db.connection.cursor()
    #check if articleId exists in DB
    if(cur.execute("SELECT (title, body) FROM Article WHERE artId = ? ", articleId)) == 0:
        return jsonify({'Article Not found'}), 404
    else:
        #Retrieve article of article id
        if request.method == 'GET':
            cur.execute("SELECT (title, body) FROM Article WHERE artID = ? ", articleId)
            article = cur.fetchone()[0]
            return jsonify(article), 200

        elif request.method == 'DELETE':
            cur.execute("DELETE FROM article WHERE artID = ?", articleId)
            return jsonify({'Successfully deleted article' : articleId}), 200




if(__name__ == '__main__'):
    app.run(debug=True)
