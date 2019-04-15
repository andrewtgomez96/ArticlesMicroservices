#comments
# 1 Post a new comment on an article
# 2 Delete an individual comment
# 3 Retrieve the number of comments on a given article
# 4 Retrieve the n most recent comments on a URL

from flask import Flask, request, jsonify
import click, json
from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext
from dbConfig import db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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
    engine = create_engine ('sqlite:///commentDB.db')
    connection = engine.connect()
    Session = sessionmaker(bind=engine)

#1
@app.route("/article/<int:articleId>/comment", methods=['POST'])
def comment(articleId):
    session = Session()
    username = None
    newComment = request.form.get('comment')
    if (request.authorization):
        username = request.authorization.username
        password = request.authorization.password

    if(username is not None):
        insertComment = Comment(comment = newComment, artId = articleId, username = username)
        db.session.add(insertComment)
        db.session.commit()
        commentId = Comment.query.with_entities(Comment.commentId).first()
        db.session.commit()
        db.session.close()
        return jsonify({'articleId' : articleId, 'commentId' : commentId}), 201

    else:
        insertComment = Comment(comment = newComment, artId = articleId)
        db.session.add(insertComment)
        db.session.commit()
        commentId = Comment.query.with_entities(Comment.commentId).first()
        db.session.commit()
        db.session.close()
        return jsonify({'articleId' : articleId, 'commentId' : commentId}), 201

#2
@app.route("/article/comment/<int:commentId>", methods=['DELETE'])
def deleteComment(commentId):
    session = Session()
    if (request.authorization):
        username = request.authorization.username
        password = request.authorization.password
    else:
        db.session.rollback()
        return jsonify('Unauthorized request'), 401

    returnObject = Comment.query.filter_by(commentId = commentId).first()
    if(returnObject):
        author = Comment.query.filter_by(commentId = commentId).with_entities(Comment.username).first()
        if(author == username):
            db.session.delete(returnObject)
            db.session.commit()
            db.session.close()
            return jsonify('comment deleted'), 200
        else:
            return jsonify('You are not authorized to delete this comment'), 409
    else:
        return jsonify('commentId was not found'), 404

#3
@app.route("/article/<string:articleId>/comments", methods=['GET'])
def getNumOfComments(articleId):
    session = Session()
    returnObject = Comment.query.filter_by(artId = articleId).all()
    if(returnObject):
        db.session.close()
        return jsonify(len(returnObject)), 200
    else:
        db.session.rollback()
        return jsonify('articleId was not found'), 404

#4 NEED TO ADD THE N PART TO THIS FUNCTION
@app.route("/article/<string:articleId>/comments/<int:n>", methods=['GET'])
def getNComments(articleId, n):
    session = Session()
    #Retrieve n most recent articles
    returnObject = Article.query.filter_by(artId = articleId).limit(n).first()
    if(returnObject):
        #return list of articles
        db.session.close()
        return jsonify(returnObject), 200
    else:
        db.session.rollback()
        return jsonify('Article Not found'), 404



if(__name__ == '__main__'):
    app.run(debug=True)
