from flask import Flask
from auth import auth_bp
from student import student_bp
from hr import hr_bp
from tpo import tpo_bp

app = Flask(__name__)
app.secret_key = "tpo_secret_key"

app.register_blueprint(auth_bp)
app.register_blueprint(student_bp)
app.register_blueprint(hr_bp)
app.register_blueprint(tpo_bp)

if __name__ == "__main__":
    app.run(debug=True)
