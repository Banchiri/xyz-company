from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import db, Department, Employee, Project, WorksOn, Dependent

# Initialize Flask app
app = Flask(__name__)

# Set up the SQLAlchemy configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///company.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Initialize the database
db.init_app(app)

@app.route('/')
def home():
    return "Welcome to XYZ Company!"

# ===================== EMPLOYEE ROUTES =====================

# Route to get all employees
@app.route('/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    return jsonify([emp.to_dict() for emp in employees])

# Route to get a specific employee by SSN
@app.route('/employees/<int:ssn>', methods=['GET'])
def get_employee(ssn):
    employee = Employee.query.get(ssn)
    if employee:
        emp_dict = employee.to_dict()
        emp_dict["projects"] = [wo.project.to_dict() for wo in employee.assignments]  
        return jsonify(emp_dict)
    else:
        return jsonify({"message": "Employee not found"}), 404

# Route to add a new employee
@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.get_json()
    new_employee = Employee(
        ssn=data['ssn'],
        name=data['name'],
        address=data['address'],
        salary=data['salary'],
        gender=data['gender'],
        birthdate=data['birthdate'],
        postal_address=data['postal_address'],
        tel_no=data['tel_no'],
        department_id=data['department_id'],
        supervisor_ssn=data.get('supervisor_ssn')
    )
    db.session.add(new_employee)
    db.session.commit()
    return jsonify(new_employee.to_dict()), 201

# ===================== DEPARTMENT ROUTES =====================

# Route to get all departments
@app.route('/departments', methods=['GET'])
def get_departments():
    departments = Department.query.all()
    return jsonify([dep.to_dict() for dep in departments])

# Route to get a specific department by ID
@app.route('/departments/<int:id>', methods=['GET'])
def get_department(id):
    department = Department.query.get(id)
    if department:
        dep_dict = department.to_dict()
        dep_dict["locations"] = [loc.to_dict() for loc in department.locations]
        dep_dict["projects"] = [proj.to_dict() for proj in department.projects]
        return jsonify(dep_dict)
    else:
        return jsonify({"message": "Department not found"}), 404

# Route to add a new department
@app.route('/departments', methods=['POST'])
def add_department():
    data = request.get_json()
    new_department = Department(
        name=data['name'],
        manager_ssn=data['manager_ssn'],
        start_date=data['startdate']
    )
    db.session.add(new_department)
    db.session.commit()
    return jsonify(new_department.to_dict()), 201

# ===================== PROJECT ROUTES =====================

# Route to get all projects
@app.route('/projects', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    return jsonify([proj.to_dict() for proj in projects])

# Route to get a specific project by project number
@app.route('/projects/<int:project_number>', methods=['GET'])
def get_project(project_number):
    project = Project.query.filter_by(number=project_number).first()
    if project:
        proj_dict = project.to_dict()
        proj_dict["assignments"] = [wo.to_dict() for wo in project.assignments]
        return jsonify(proj_dict)
    else:
        return jsonify({"message": "Project not found"}), 404

# Route to add a new project
@app.route('/projects', methods=['POST'])
def add_project():
    data = request.get_json()
    new_project = Project(
        name=data['name'],
        number=data['number'],
        location=data['location'],
        department_id=data['department_id']
    )
    db.session.add(new_project)
    db.session.commit()
    return jsonify(new_project.to_dict()), 201

# ===================== WORKS_ON ROUTES =====================

# Route to get all assignments (WorksOn) for employees
@app.route('/works_on', methods=['GET'])
def get_works_on():
    works_on = WorksOn.query.all()
    return jsonify([wo.to_dict() for wo in works_on])

# Route to get a specific assignment by WorksOn ID
@app.route('/works_on/<int:id>', methods=['GET'])
def get_work_on(id):
    work_on = WorksOn.query.get(id)
    if work_on:
        return jsonify(work_on.to_dict())
    else:
        return jsonify({"message": "Assignment not found"}), 404

# Route to add a new works_on (assignment)
@app.route('/works_on', methods=['POST'])
def add_works_on():
    data = request.get_json()
    new_works_on = WorksOn(
        employee_ssn=data['employee_ssn'],
        project_id=data['project_id'],
        hours_per_week=data['hours_per_week']
    )
    db.session.add(new_works_on)
    db.session.commit()
    return jsonify(new_works_on.to_dict()), 201

# ===================== DEPENDENT ROUTES =====================

# Route to get all dependents of employees
@app.route('/dependents', methods=['GET'])
def get_dependents():
    dependents = Dependent.query.all()
    return jsonify([dep.to_dict() for dep in dependents])

# Route to get dependents for a specific employee by SSN
@app.route('/dependents/<int:ssn>', methods=['GET'])
def get_dependents_by_employee(ssn):
    employee = Employee.query.get(ssn)
    if employee:
        dependents = employee.dependents
        return jsonify([dep.to_dict() for dep in dependents])
    else:
        return jsonify({"message": "Employee not found"}), 404

# Route to add a new dependent
@app.route('/dependents', methods=['POST'])
def add_dependent():
    data = request.get_json()
    new_dependent = Dependent(
        first_name=data['first_name'],
        gender=data['gender'],
        birthdate=data['birthdate'],
        relationship=data['relationship'],
        employee_ssn=data['employee_ssn']
    )
    db.session.add(new_dependent)
    db.session.commit()
    return jsonify(new_dependent.to_dict()), 201


if __name__ == '__main__':
    app.run(debug=True)
