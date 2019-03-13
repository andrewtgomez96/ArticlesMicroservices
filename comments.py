#comments
# 1 Post a new comment on an article
# 2 Delete an individual comment
# 3 Retrieve the number of comments on a given article
# 4 Retrieve the n most recent comments on a URL



from flask import Flask, current_app, request, jsonify
from flask_sqlite3 import SQLite3
import click, json
from flask.cli import with_appcontext
from flask_bcrypt import Bcrypt #added
from flask_basicauth import BasicAuth #added

app = Flask(__name__)
db = SQLite3(app)
bcrypt = Bcrypt(app) #added
BasicAuth(app)

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

# basic auth subclass checks database
def checkAuth(username, password):
    return True
    #cur = db.connection.cursor()
    #cur.execute("SELECT password FROM User WHERE userName = ?", username)
    #pw_hash = cur.fetchone()
    #if(bcrypt.check_password_hash(pw_hash, password)) == True:
        #return True
    #else:
        #return False

#1
@app.route("/article/<int:articleId>/comment", methods=['POST'])
def comment(articleId):
    cur = db.connection.cursor()
    username = None
    comment = request.form.get('comment')
    if (request.authorization):
        username = request.authorization.username
        password = request.authorization.password
    cur.execute("SELECT artId FROM Article WHERE artId = ? ", (articleId,))
    returnObject = cur.fetchone()
    if(returnObject):
        if(username is not None):
            insertComment = (comment, articleId, username)
            if(checkAuth(username, password) == True):
                cur.execute("INSERT INTO Comment (comment, artId, author) VALUES (?, ?, ?)", insertComment)
                db.connection.commit()
                cur.execute("SELECT commentId FROM Comment where comment = ? AND artId = ?", (comment, articleId))
                commentId = cur.fetchone()[0]
                db.connection.commit()
                return jsonify({'articleId' : articleId, 'commentId' : commentId}), 201
            else:
                return jsonify('Credentials not found'), 409
        else:
            insertComment = (comment, articleId)
            cur.execute("INSERT INTO Comment (comment, artId) VALUES (?, ?)", insertComment)
            db.connection.commit()
            cur.execute("SELECT commentId FROM Comment where comment = ? AND artId = ?", (comment, articleId))
            commentId = cur.fetchone()[0]
            db.connection.commit()
            return jsonify({'articleId' : articleId, 'commentId' : commentId}), 201
    else:
        return jsonify('articleId was not found'), 404

#2
@app.route("/article/comment/<int:commentId>", methods=['DELETE'])
def deleteComment(commentId):
    cur = db.connection.cursor()
    if (request.authorization):
        username = request.authorization.username
        password = request.authorization.password
    else:
        return jsonify('Unauthorized request'), 401
    cur.execute("SELECT * FROM Comment WHERE commentId = ? ", (commentId,))
    returnObject = cur.fetchone()
    if(returnObject):
        if(checkAuth(username, password) == True):
            cur.execute("SELECT author FROM Comment WHERE commentId = ? ", (commentId,))
            author = cur.fetchone()[0]
            if(author == username):
                cur.execute("DELETE FROM Comment WHERE commentId = ?", (commentId,))
                db.connection.commit()
                return jsonify('comment deleted'), 200
            else:
                return jsonify('You are not authorized to delete this comment'), 409
        else:
            return jsonify('Credentials not found'), 409
    else:
        return jsonify('commentId was not found'), 404

#3
@app.route("/article/<string:articleId>/comments", methods=['GET'])
def getNumOfComments(articleId):
    cur = db.connection.cursor()
    cur.execute("SELECT artId FROM Article WHERE artId = ? ", (articleId,))
    returnObject = cur.fetchone()
    if(returnObject):
        cur.execute("SELECT * FROM Comment WHERE artId = ?", (articleId,))
        comments= cur.fetchall()
        return jsonify(len(comments)), 200
    else: 
        return jsonify('articleId was not found'), 404

#4 NEED TO ADD THE N PART TO THIS FUNCTION
@app.route("/article/<string:articleId>/comments/<int:n>", methods=['GET'])
def getNComments(articleId, n):
    cur = db.connection.cursor()
    nComments = (articleId, n)
    cur.execute("SELECT artId FROM Article WHERE artId = ? ", (articleId,))
    returnObject = cur.fetchone()
    if(returnObject):
        cur.execute("SELECT comment FROM Comment WHERE artId = ? ORDER BY created DESC LIMIT ?", nComments)
        comments = cur.fetchall()
        returnComments = {}
        for comment in comments:
            returnComments['comment'] = comment[0]
        return jsonify(returnComments), 200
    else: 
        return jsonify('articleId was not found'), 404




if(__name__ == '__main__'):
    app.run(debug=True)