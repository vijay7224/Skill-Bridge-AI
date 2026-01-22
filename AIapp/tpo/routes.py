from flask import Blueprint, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

# ---------- Blueprint ----------
tpo_bp = Blueprint("tpo", __name__, url_prefix="/tpo")

# ---------- MongoDB ----------
client = MongoClient("mongodb://localhost:27017/")
db = client["placement_db"]
students_col = db["tpo_students"]

# ---------- Dashboard ----------
@tpo_bp.route("/dashboard")
def dashboard():
    search = request.args.get("search")
    branch = request.args.get("branch")
    batch = request.args.get("batch")
    status = request.args.get("status")
    recommendation = request.args.get("recommendation")

    query = {}
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"roll_no": {"$regex": search, "$options": "i"}}
        ]
    if branch:
        query["branch"] = branch
    if batch:
        query["batch"] = batch
    if status:
        query["status"] = status
    if recommendation:
        query["recommendation_tag"] = recommendation

    students = list(students_col.find(query))

    total = students_col.count_documents({})
    eligible = students_col.count_documents({"status": "Eligible"})
    placed = students_col.count_documents({"status": "Placed"})
    recommended = students_col.count_documents({"recommendation_tag": "Personally Recommended to HR"})

    return render_template(
        "TOP.html",
        students=students,
        total=total,
        eligible=eligible,
        placed=placed,
        recommended=recommended
    )

# ---------- Update Status ----------
@tpo_bp.route("/update_status", methods=["POST"])
def update_status():
    students_col.update_one(
        {"_id": ObjectId(request.form["id"])},
        {"$set": {"status": request.form["status"]}}
    )
    return redirect(url_for("tpo.dashboard"))

# ---------- Update Recommendation ----------
@tpo_bp.route("/update_recommendation", methods=["POST"])
def update_recommendation():
    students_col.update_one(
        {"_id": ObjectId(request.form["id"])},
        {"$set": {"recommendation_tag": request.form["recommendation"]}}
    )
    return redirect(url_for("tpo.dashboard"))

# ---------- View Student Profile ----------
@tpo_bp.route("/student/<id>")
def view_student(id):
    student = students_col.find_one({"_id": ObjectId(id)})
    if not student:
        return "Student Not Found", 404
    return render_template("student_profile.html", student=student)
