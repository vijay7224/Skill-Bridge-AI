from flask import Blueprint, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

# ---------- Blueprint ----------
hr_bp = Blueprint("hr", __name__, url_prefix="/hr")

# ---------- MongoDB ----------
client = MongoClient("mongodb://localhost:27017/")
db = client["placement_db"]
students_col = db["students"]

# ---------- HR Dashboard ----------
@hr_bp.route("/dashboard")
def dashboard():
    query = {}

    search = request.args.get("search")
    min_cgpa = request.args.get("min_cgpa")
    skill = request.args.get("skill")
    decision = request.args.get("decision")

    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"email": {"$regex": search, "$options": "i"}},
            {"roll_no": {"$regex": search, "$options": "i"}}
        ]

    if min_cgpa:
        query["cgpa"] = {"$gte": float(min_cgpa)}

    if skill:
        query["skills"] = {"$regex": skill, "$options": "i"}

    if decision:
        query["hr_decision"] = decision

    students = list(students_col.find(query))

    total = students_col.count_documents({})
    shortlisted = students_col.count_documents({"hr_decision": "Shortlisted"})
    rejected = students_col.count_documents({"hr_decision": "Rejected"})
    pending = students_col.count_documents({
        "$or": [
            {"hr_decision": "Pending"},
            {"hr_decision": {"$exists": False}}
        ]
    })

    return render_template(
        "HR.html",
        students=students,
        total=total,
        shortlisted=shortlisted,
        rejected=rejected,
        pending=pending
    )

# ---------- Shortlist / Reject ----------
@hr_bp.route("/decision", methods=["POST"])
def decision():
    student_id = request.form.get("id")
    status = request.form.get("status")

    students_col.update_one(
        {"_id": ObjectId(student_id)},
        {"$set": {"hr_decision": status}}
    )

    return redirect(url_for("hr.dashboard"))

# ---------- View Student Profile ----------
@hr_bp.route("/student/<id>")
def view_student(id):
    student = students_col.find_one({"_id": ObjectId(id)})
    if not student:
        return "Student Not Found", 404

    return render_template("student_profile.html", student=student)
