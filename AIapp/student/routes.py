from flask import Blueprint, render_template, session, redirect, url_for
from extensions import users
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["tpo_portal"]
users = db["users"]

student_bp = Blueprint("student", __name__, url_prefix="/student")

@student_bp.route("/dashboard", methods=["GET"])
def dashboard():
    if "user_email" not in session:
        return redirect(url_for("auth.index"))

    user = users.find_one({"email": session["user_email"]})

    return render_template(
        "STUDENT.html",
         name=user.get("fullname"),
        branch=user.get("branch", "B.Tech AI"),
        enrollment=user.get("enrollment"),
        points=user.get("points", 0)
    )

