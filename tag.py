#tag
# 1 Add an article with a new tag
# 2 Add another tag to the article and # 3 Add a tag to an article that doesn’t exist
# 4 Delete one or more of the tags from the article
# 5 List all articles with the new tag
# 6 Retrieve the tags for an individual URL


from flask import Flask, current_app, request, jsonify
from flask_sqlite3 import SQLite3
import click
from flask.cli import with_appcontext

app = Flask(__name__)
db = SQLite3(app)

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

#1
@app.route("/article/tag/<string:tag>", methods=['POST'])
def addArtTag(tag):
    cur = db.connection.cursor()
    userName = request.form.get('userName')
    title = request.form.get('title')
    body = request.form.get('body')
    insertArticle = (userName, title, body)

    cur.execute("INSERT INTO Article (userName, title, body, commentCount) VALUES (?, ?, ?, 0)", insertArticle)
    cur.execute("SELECT artId FROM Article WHERE title = ? ", (title,))
    artId = cur.fetchone()[0]
    insertTag = (tag, artId)
    cur.execute("INSERT INTO Tag (tag, artId) VALUES (?, ?)", insertTag)
    db.connection.commit()
    return jsonify(artId), 201

#2 and 3
@app.route("/article/<string:articleId>/tag/<string:tag>", methods=['PUT'])
def addTag(articleId, tag):
    cur = db.connection.cursor()
    cur.execute("""INSERT INTO User (username, password)
                VALUES ('Andrew', 'disme')""")
    db.connection.commit()
    if(articleId != "me"):
        return "http status code blah blah"
    return jsonify(cur.execute("select * from User").fetchall())

#6
@app.route("/article/<string:articleId>/tags", methods=['GET'])
def getTags(articleId):
    return f"grabbing all tags from {articleId} article"

#4  
@app.route("/article/<string:articleId>/tag/<int:n>", methods=['DELETE'])
def deleteTags(articleId, n):
    return f"we are deleting {n} tags from an article"

#5
@app.route("/articles/tag/<string:tag>", methods=['GET'])
def getArticles(tag):
    return "List all articles with the new tag"




if(__name__ == '__main__'):
    app.run(debug=True)