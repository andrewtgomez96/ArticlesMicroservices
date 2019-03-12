#tag
# 1 Add an article with a new tag
# 2 Add another tag to the article and # 3 Add a tag to an article that doesn’t exist
# 4 Delete one or more of the tags from the article
# 5 List all articles with the new tag
# 6 Retrieve the tags for an individual URL


from flask import Flask, current_app, request, jsonify
from flask_sqlite3 import SQLite3
import click, json
from flask.cli import with_appcontext
from flask_bcrypt import Bcrypt #added
from flask_basicauth import BasicAuth #added

app = Flask(__name__)
db = SQLite3(app)
bcrypt = Bcrypt(app) #added

'''
if you run 'flask init-db-command' it will drop the current database and reinitialize it from
the scheme.sql file which resets the db, inserting 3 rows in each table
'''
@app.cli.command()
@with_appcontext
def init_db_command():
    print("Clear the existing data and create new tables.")
    init_db()
    click.echo('Initialized the database.')

def init_db():
    with current_app.open_resource('schema.sql') as f:
        db.connection.executescript(f.read().decode('utf8'))

#--added code here--
# basic auth subclass checks database
def checkAuth(username, password):
    cur = db.connection.cursor()
    cur.execute("SELECT password FROM User WHERE userName = ?", username)
    pw_hash = cur.fetchone()
    if(bcrypt.check_password_hash(pw_hash, password)) == True:
        return True
    else:
        return False
#-- end code here --

#1
@app.route("/article/tag/<string:tag>", methods=['POST'])
def addArtTag(tag):
    cur = db.connection.cursor()
    userName = request.form.get('userName')
    title = request.form.get('title')
    body = request.form.get('body')
    password = request.headers.get('Authorization')
    insertArticle = (userName, title, body)

    if(checkAuth(userName, password) == True):
        cur.execute("INSERT INTO Article (userName, title, body, commentCount) VALUES (?, ?, ?, 0)", insertArticle)
        cur.execute("SELECT artId FROM Article WHERE title = ? ", (title,))
        artId = cur.fetchone()[0]
        insertTag = (tag, artId)
        cur.execute("INSERT INTO Tag (tag, artId) VALUES (?, ?)", insertTag)
        db.connection.commit()
        return jsonify({'articleId' : artId, 'tag' : tag}), 201
    else: 
        return jsonify({'Credentials not found'}), 409

#2 and 3
@app.route("/article/<int:articleId>/tag/<string:tag>", methods=['PUT'])
def addTag(articleId, tag):
    cur = db.connection.cursor()
    password = request.headers.get('Authorization')
    userName = request.form.get('userName')

    if(checkAuth(userName, password) == True):
        if(cur.execute("SELECT artId FROM Article WHERE artId = ? ", (articleId,)) == 0):
            return jsonify({'articleId was not found'}), 404
        else:
            insertTag = (tag, articleId)
            cur.execute("INSERT INTO TAG (tag, artId) VALUES (?, ?)", insertTag)
            db.connection.commit()
            return jsonify(articleId), 200
    else:
        return jsonify({'Credentials not found'}), 409

#6
@app.route("/article/<int:articleId>/tags", methods=['GET'])
def getTags(articleId):
    cur = db.connection.cursor()
    if(cur.execute("SELECT artId FROM Article WHERE artId = ? ", (articleId,)) == 0):
        return jsonify({'articleId was not found'}), 404
    else: 
        cur.execute("SELECT (tag) FROM Tag WHERE artId = ?", (articleId,))
        tags= cur.fetchall()
        return jsonify(tags), 200

#4  
@app.route("/article/<int:articleId>/tag", methods=['DELETE'])
def deleteTags(articleId):
    cur = db.connection.cursor()
    password = request.headers.get('Authorization')
    userName = request.form.get('userName')
    returnTags = {}
    #array holding one or more tags to delete
    tags = request.form.get('tags')
    #check if articleId exists in DB
    if(cur.execute("SELECT artId FROM Article WHERE artId = ? ", (articleId,)) == 0):
        return jsonify({'articleId was not found'}), 404
    #authenticate
    if(checkAuth(userName, password) == True):
        for tag in tags:
            rmTag = (tag, articleId)
            #Delete tags
            if(cur.execute("DELETE FROM Tag WHERE tag = ? AND articleId = ?", rmTag) == 0):
                returnTags[f'{tag}'] = 'false'
            else:
                returnTags[f'{tag}'] = 'True'
    else:
        return jsonify({'Credentials not found'}), 409
    return jsonify(returnTags), 200

#5
@app.route("/articles/tag/<string:tag>", methods=['GET'])
def getArticles(tag):
    cur = db.connection.cursor()
    if(cur.execute("SELECT tag FROM Tag WHERE tag = ? ", (tag,)) == 0):
        return jsonify({'tag was not found'}), 404
    else: 
        cur.execute("SELECT artId FROM Tag where tag = ?", (tag,))
        artIds= cur.fetchall()
        return jsonify(artIds), 200




if(__name__ == '__main__'):
    app.run(debug=True)