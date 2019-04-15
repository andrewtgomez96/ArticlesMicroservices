#tag
# 1 Add an article with a new tag# 4 Delete one or more of the tags from the article
# 5 List all articles with the new tag
# 6 Retrieve the tags for an individual URL


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
    engine = create_engine ('sqlite:///tagDB.db')
    connection = engine.connect()
    Session = sessionmaker(bind=engine)

#1
@app.route("/article/tag/<string:tag>", methods=['POST'])
def addArtTag(tag):
    session = Session()
    if (request.authorization):
        username = request.authorization.username
        password = request.authorization.password
        title = request.form.get('title')
        body = request.form.get('body')
    else:
        db.session.rollback()
        return jsonify('Unauthorized response'), 401

    a = Tag(username = username, title = title, body = body, tag = tag)
    db.session.add(a)
    db.session.commit()
    artId = Tag.query.with_entities(Tag.artId).first()
    db.session.close()
    return jsonify({'articleId' : artId, 'tag' : tag}), 201

#2 and 3
@app.route("/article/<int:articleId>/tag/<string:tag>", methods=['PUT'])
def addTag(articleId, tag):
    session = Session()
    if (request.authorization):
        username = request.authorization.username
        password = request.authorization.password
    else:
        db.session.rollback()
        return jsonify('Unauthorized response'), 401

    returnObject = Tag.query.filter_by(artId = articleId, tag = tag).first()
    if(returnObject):
        author = Tag.query.filter_by(artId = articleId).with_entities(Tag.username).first()
        if(author == username):
            t = Tag(tag = tag, artId = articleId)
            db.session.add(t)
            db.session.commit()
            db.session.close()
            return jsonify(articleId), 200
        else:
            db.session.rollback()
            return jsonify('You are not authorized to add this tag'), 409
    else:
        db.session.rollback()
        return jsonify('articleId was not found'), 404


#6
@app.route("/article/<int:articleId>/tags", methods=['GET'])
def getTags(articleId):
    session = Session()
    returnObject = Tag.query.filter_by(artId = articleId).all()
    if(returnObject):
        db.session.close()
        return jsonify(returnObject), 200
    else:
        db.session.rollback()
        return jsonify('articleId was not found'), 404

#4
@app.route("/article/<int:articleId>/tag", methods=['DELETE'])
def deleteTags(articleId):
    session = Session()
    if (request.authorization):
        username = request.authorization.username
        password = request.authorization.password
    else:
        db.session.rollback()
        return jsonify('Unauthorized response'), 401
    returnTags = {}
    #array holding one or more tags to delete
    tags = request.form.get('tags')
    tags = tags.split(",")
    #check if articleId exists in DB
    returnObject = Tag.query.filter_by(artId = articleId).first()
    if(returnObject):
        author = Tag.query.filter_by(artId = articleId).with_entities(Tag.username).first()
        cur.execute("SELECT userName FROM Article WHERE artId = ? ", (articleId,))
        if(author == username):
            for tag in tags:
                rmTag = (tag, articleId)
                print(rmTag)
                #Delete tags
                returnObject = Tag.query.filter_by(tag = tag, artId = articleId).first()
                if(returnObject):
                    db.session.delete(returnObject)
                    returnTags['{tag}'] = 'True'
                    db.session.commit()
                else:
                    returnTags['{tag}'] = 'false'
            db.session.close()
            return jsonify(returnTags), 200
        else:
            db.session.rollback()
            return jsonify('You are not authorized to delete this tag'), 409
    else:
        db.session.rollback()
        return jsonify('articleId was not found'), 404

#5
@app.route("/articles/tag/<string:tag>", methods=['GET'])
def getArticles(tag):
    session = Session()
    returnObject = Tag.query.filter_by(tag = tag).with_entities(Tag.artId).all()
    if(returnObject):
        db.session.close()
        return jsonify(returnObject), 200
    else:
        db.session.rollback()
        return jsonify({'tag was not found'}), 404




if(__name__ == '__main__'):
    app.run(debug=True)
