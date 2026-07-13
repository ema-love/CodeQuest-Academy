
from flask import Flask,render_template,request,redirect,url_for
app=Flask(__name__)

missions=[
{"id":1,"title":"Task Manager","deadline":"Day 3","xp":100},
{"id":2,"title":"Quiz Game","deadline":"Day 5","xp":100},
{"id":3,"title":"Number Guessing Game","deadline":"Day 7","xp":100},
{"id":4,"title":"Restaurant Ordering System","deadline":"Day 10","xp":150},
{"id":5,"title":"Student Grade Calculator","deadline":"Day 14","xp":150},
{"id":6,"title":"Portfolio Website","deadline":"Day 21","xp":300},
]

submissions={}

@app.route("/")
def home():
    return render_template("index.html",missions=missions,subs=submissions)

@app.post("/submit/<int:mid>")
def submit(mid):
    submissions[mid]=request.form.get("github","")
    return redirect(url_for("home"))

if __name__=="__main__":
    app.run(debug=True)
