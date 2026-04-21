from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

DATA_FILE = "employees.json"

def load_employees():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_employees(employees):
    with open(DATA_FILE, "w") as f:
        json.dump(employees, f, indent=2)

@app.route("/")
def index():
    employees = load_employees()
    return render_template("index.html", employees=employees)

@app.route("/add", methods=["GET", "POST"])
def add_employee():
    if request.method == "POST":
        employees = load_employees()
        emp = {
            "id":         len(employees) + 1,
            "name":       request.form["name"],
            "email":      request.form["email"],
            "phone":      request.form["phone"],
            "department": request.form["department"],
            "position":   request.form["position"],
            "salary":     request.form["salary"],
            "joining":    request.form["joining"]
        }
        employees.append(emp)
        save_employees(employees)
        return redirect(url_for("index"))
    return render_template("add.html")

@app.route("/delete/<int:emp_id>")
def delete_employee(emp_id):
    employees = load_employees()
    employees = [e for e in employees if e["id"] != emp_id]
    save_employees(employees)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)