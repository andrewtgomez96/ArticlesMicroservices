#comments
# 1 Post a new comment on an article
# 2 Delete an individual comment
# 3 Retrieve the number of comments on a given article
# 4 Retrieve the n most recent comments on a URL



from flask import Flask, request
app = Flask(__name__)

#1 and 2
@app.route("/article/<string:articleId>/comment/<string:commentId>", methods=['POST', 'DELETE'])
def comments(articleId, commentId):
    if(request.method == 'POST'):
        return f"post a new comment to {articleId} with this comment id {commentId}"
    if(request.method == 'DELETE'):
        return f"we are deleting a comment with this id {commentId} from an article with this id {articleId}"

#3
@app.route("/article/<string:articleId>/comments", methods=['GET'])
def getNumOfComments(articleId):
    return f"Retrieve the number of comments on a given article: {articleId}"

#4
@app.route("/article/<string:articleId>/comments/<int:n>", methods=['GET'])
def getNComments(articleId, n):
    return f"Retrieve the {n} most recent comments on a URL"




if(__name__ == '__main__'):
    app.run(debug=True)