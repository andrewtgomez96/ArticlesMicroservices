#article
#1 posting a new article
#2 retrieve an existing article
#3 edit an existing article (update TIMESTAMP)
#4 delete an existing article
#5 retrieve contents of n most recent getArticles
#6 retrieve metadata for an article

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
    engine = create_engine ('sqlite:///articleDB.db')
    connection = engine.connect()
    Session = sessionmaker(bind=engine)

# 1 function for posting single article
@app.route("/article/new/<title>/<body>", methods=['POST'])
def newArticle(Atitle, Abody):
    session = Session()
    #reverse proxy
    if (request.authorization):
        username = request.authorization.username
        password = request.authorization.password
        user = username
    else:
        db.session.rollback()
        return jsonify('Unauthorized response'), 401

    #pass info into articles database
    a = Article(username = user, title = Atitle, body = Abody)
    db.session.add(a)
    db.session.commit()
    db.session.close()
    return jsonify('Successfully created article'), 201

#2 retrieve existing article
@app.route("/article/<int:articleId>/title", methods=['GET'])
def getArticle(articleId):
    session = Session()
    #check if articleId exists in DB
    returnObject = Article.query.filter_by(artId = articleId).first()
    if(returnObject):
        db.session.close()
        return jsonify(returnObject), 200
    else:
        db.session.rollback()
        return jsonify('Article Not found'), 404

#3 edit existing article
@app.route("/article/<int:articleId>/<title>/<body>", methods=['PATCH'])
def editArticle(articleId, Atitle, Abody):
    session = Session()
    if (request.authorization):
        username = request.authorization.username
        password = request.authorization.password
        user = username
    else:
        db.session.rollback()
        return jsonify('Unauthorized response'), 401

    returnObject = Article.query.filter_by(artId = articleId).first()
    if(returnObject):
        returnObject.userName = user
        returnObject.title = Atitle
        returnObject.body = Abody
        db.session.commit()
        db.session.close()
        return jsonify({'Successfully edited article' : articleId}), 200
    else:
        db.session.rollback()
        return jsonify('Not found'), 404

#4  delete and existing article
@app.route("/article/<int:articleId>", methods=['DELETE']) #allow both GET and POST requests
def deleteArticle(articleId):
    session = Session()
    if (request.authorization):
        username = request.authorization.username
        password = request.authorization.password
    else:
        db.session.rollback()
        return ('Unauthorized response'), 401

    #check if articleId exists in DB
    returnObject = Article.query.filter_by(artId = articleId).first()
    if(returnObject):
        #Delete article
        db.session.delete(returnObject)
        db.session.commit()
        db.session.close()
        return jsonify({'Successfully deleted article' : articleId}), 200
    else:
        db.session.rollback()
        return jsonify('Article Not found'), 404

#5 retrieve contents of n most recent articles
@app.route("/articles/<int:n>", methods=['GET'])
def getArticles(n):
    session = Session()
    #Retrieve n most recent articles
    returnObject = Article.query.with_entities(Article.title, Article.body).limit(n).first()
    if(returnObject):
        #return list of articles
        db.session.close()
        return jsonify(returnObject), 200
    else:
        db.session.rollback()
        return jsonify('Article Not found'), 404
#6 retrieve meta data of n most recent articles
@app.route("/articles/info/<int:n>", methods=['GET']) #allow both GET and POST requests
def getMetaArticles(n):
    session = Session()
    #Retrieve n most recent articles
    returnObject = Article.query.limit(n)
    if(returnObject):
        #return list of articles
        db.session.close()
        return jsonify(returnObject), 200
    else:
        db.session.rollback()
        return jsonify('Article Not found'), 404



if(__name__ == '__main__'):
    app.run(debug=True)
