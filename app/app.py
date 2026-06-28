from flask import Flask, render_template, request, redirect, jsonify
from datetime import datetime

from database import db
from models import Task

app = Flask(__name__)

# SQLite Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()


# -------------------------
# Dashboard + Search
# -------------------------
@app.route("/")
def index():

    search = request.args.get("search")

    if search:
        tasks = Task.query.filter(
            Task.title.contains(search)
        ).all()
    else:
        tasks = Task.query.all()

    total = Task.query.count()

    completed = Task.query.filter_by(status="Completed").count()

    pending = Task.query.filter_by(status="Pending").count()

    return render_template(
        "index.html",
        tasks=tasks,
        total=total,
        completed=completed,
        pending=pending
    )


# -------------------------
# Add Task
# -------------------------
@app.route("/add", methods=["POST"])
def add_task():

    task = Task(
        title=request.form["title"],
        description=request.form["description"],
        priority=request.form["priority"],
        due_date=datetime.strptime(
            request.form["due_date"],
            "%Y-%m-%d"
        )
    )

    db.session.add(task)
    db.session.commit()

    return redirect("/")


# -------------------------
# Mark Task as Completed
# -------------------------
@app.route("/complete/<int:id>")
def complete_task(id):

    task = Task.query.get(id)

    if task:
        task.status = "Completed"
        db.session.commit()

    return redirect("/")


# -------------------------
# Delete Task
# -------------------------
@app.route("/delete/<int:id>")
def delete_task(id):

    task = Task.query.get(id)

    if task:
        db.session.delete(task)
        db.session.commit()

    return redirect("/")


# -------------------------
# Health Check (for DevOps)
# -------------------------
@app.route("/health")
def health():

    return jsonify({
        "status": "UP",
        "application": "CloudTask Pro",
        "version": "1.0"
    })


# -------------------------
# Run App
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)