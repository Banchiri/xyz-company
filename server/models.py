from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData


from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# ===================== DEPARTMENT =====================
class Department(db.Model, SerializerMixin):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    manager_ssn = db.Column(db.Integer, db.ForeignKey('employees.ssn'), nullable=True)
    start_date = db.Column(db.Date, nullable=True)

    locations = db.relationship('Location', back_populates='department', cascade='all, delete-orphan')
    projects = db.relationship('Project', back_populates='department', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "manager_ssn": self.manager_ssn,
            "start_date": self.start_date
        }

# ===================== LOCATION =====================
class Location(db.Model, SerializerMixin):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)

    department = db.relationship('Department', back_populates='locations')

    def to_dict(self):
        return {
            "id": self.id,
            "address": self.address,
            "department_id": self.department_id
        }

# ===================== PROJECT =====================
class Project(db.Model, SerializerMixin):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    number = db.Column(db.String, unique=True, nullable=False)
    location = db.Column(db.String, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)

    department = db.relationship('Department', back_populates='projects')
    assignments = db.relationship('WorksOn', back_populates='project', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "number": self.number,
            "location": self.location,
            "department_id": self.department_id
        }

# ===================== EMPLOYEE =====================
class Employee(db.Model, SerializerMixin):
    __tablename__ = 'employees'
    ssn = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    salary = db.Column(db.Float, nullable=False)
    gender = db.Column(db.String, nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    postal_address = db.Column(db.String, nullable=False)
    tel_no = db.Column(db.String, nullable=False)

    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    supervisor_ssn = db.Column(db.Integer, db.ForeignKey('employees.ssn'), nullable=True)

    department = db.relationship('Department', foreign_keys=[department_id])
    supervised_employees = db.relationship('Employee', backref=db.backref('supervisor', remote_side=[ssn]), lazy='select')
    assignments = db.relationship('WorksOn', back_populates='employee', cascade='all, delete-orphan')
    dependents = db.relationship('Dependent', back_populates='employee', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            "ssn": self.ssn,
            "name": self.name,
            "address": self.address,
            "salary": self.salary,
            "gender": self.gender,
            "birthdate": self.birthdate,
            "postal_address": self.postal_address,
            "tel_no": self.tel_no,
            "department_id": self.department_id,
            "supervisor_ssn": self.supervisor_ssn
        }

# ===================== WORKS_ON =====================
class WorksOn(db.Model, SerializerMixin):
    __tablename__ = 'works_on'
    id = db.Column(db.Integer, primary_key=True)
    employee_ssn = db.Column(db.Integer, db.ForeignKey('employees.ssn'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    hours_per_week = db.Column(db.Float, nullable=False)

    employee = db.relationship('Employee', back_populates='assignments')
    project = db.relationship('Project', back_populates='assignments')

    def to_dict(self):
        return {
            "id": self.id,
            "employee_ssn": self.employee_ssn,
            "project_id": self.project_id,
            "hours_per_week": self.hours_per_week
        }

# ===================== DEPENDENT =====================
class Dependent(db.Model, SerializerMixin):
    __tablename__ = 'dependents'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    relationship = db.Column(db.String, nullable=False)
    employee_ssn = db.Column(db.Integer, db.ForeignKey('employees.ssn'), nullable=False)

    employee = db.relationship('Employee', back_populates='dependents')

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "gender": self.gender,
            "birthdate": self.birthdate,
            "relationship": self.relationship,
            "employee_ssn": self.employee_ssn
        }
