#tag
# 1 Add an article with a new tag
# 2 Add another tag to the article
# 3 Add a tag to an article that doesn’t exist
# 4 Delete one or more of the tags from the article
# 5 List all articles with the new tag


from flask import Flask, current_app, request, jsonify
from flask_sqlite3 import SQLite3
import click
from flask.cli import with_appcontext

app = Flask(__name__)
db = SQLite3(app)

@app.cli.command()
@with_appcontext
def init_db_command():
    print("Clear the existing data and create new tables.")
    init_db()
    click.echo('Initialized the database.')

def init_db():
    
    with current_app.open_resource('schema.sql') as f:
        db.connection.executescript(f.read().decode('utf8'))

#1 and 2 and 3
@app.route("/article/<string:articleId>/tag/<string:tag>", methods=['POST', 'PATCH', 'DELETE'])
def addTags(articleId, tag):
    cur = db.connection.cursor()
    if(request.method == 'POST'):
        return jsonify(cur.execute("select * from User").fetchall())
    if(request.method == 'PATCH'):
        cur.execute("""INSERT INTO User (username, password)
                    VALUES ('Andrew', 'disme')""")
        db.connection.commit()
        if(articleId != "me"):
            return "http status code blah blah"
        return jsonify(cur.execute("select * from User").fetchall())

@app.route("/article/<string:articleId>/tags", methods=['GET'])
def getTags(articleId):
    return f"grabbing all tags from {articleId} article"
        
@app.route("/article/<string:articleId>/tag/<int:n>", methods=['DELETE'])
def deleteTags(articleId, n):
    return f"we are deleting {n} tags from an article"

#get all articles with tag
@app.route("/articles/tag/<string:tag>", methods=['GET'])
def getArticles(tag):
    return "List all articles with the new tag"




if(__name__ == '__main__'):
    app.run(debug=True)