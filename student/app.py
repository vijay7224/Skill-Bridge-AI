from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# ---------- MongoDB Connection ----------
client = MongoClient("mongodb://localhost:27017/")
db = client["placement_db"]
students_col = db["students"]

# ---------- Home ----------
@app.route("/")
def home():
    return redirect(url_for("hr_dashboard"))

# ---------- HR Dashboard ----------
@app.route("/hr")
def hr_dashboard():
    students = list(students_col.find())

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
        "hr.html",
        students=students,
        total=total,
        shortlisted=shortlisted,
        rejected=rejected,
        pending=pending
    )

# ---------- Shortlist / Reject ----------
@app.route("/decision", methods=["POST"])
def decision():
    student_id = request.form.get("id")
    status = request.form.get("status")

    students_col.update_one(
        {"_id": ObjectId(student_id)},
        {"$set": {"hr_decision": status}}
    )

    return redirect(url_for("hr_dashboard"))
# ================= VIEW STUDENT PROFILE =================
@app.route("/student/<id>")
def view_student(id):
    student = students_col.find_one({"_id": ObjectId(id)})
    if not student:
        return "Student Not Found", 404
    return render_template("student_profile.html", student=student)


# ---------- Run ----------
if __name__ == "__main__":
    app.run(debug=True)
