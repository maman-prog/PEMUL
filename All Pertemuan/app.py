from flask import Flask,request
from markupsafe import escape
app=Flask(__name__)
@app.route("/")
def hello_word():
    return "<p>Hello, Kasepku!</p> <img src='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRqfWR_ndGrF8wiiQ_lXvaGf1VkOxyWiGyFSWpoXhZdiA&s' />"
@app.route("/about")
def about():
    return "About us"
@app.route("/user/<name>")
def profile(name):
    return f"Hello, {name}!"
@app.route("/post/<int:post_id>")
def post(post_id):
    return f"Post #{post_id}"