from app import app
from models import db, Department, Location, Employee, Project, WorksOn, Dependent
from datetime import date

with app.app_context():
    # Drop and recreate tables for development
    db.drop_all()
    db.create_all()

    # Create departments (initially without manager_ssn)
    departments = [
        Department(name="HR", manager_ssn=None, start_date=date(2021, 1, 10)),
        Department(name="Engineering", manager_ssn=None, start_date=date(2020, 5, 20)),
        Department(name="Cooperatives", manager_ssn=None, start_date=date(2020, 5, 20)),
        Department(name="Science", manager_ssn=None, start_date=date(2020, 5, 20)),
        Department(name="Tech", manager_ssn=None, start_date=date(2020, 5, 20)),
        Department(name="Tourism", manager_ssn=None, start_date=date(2020, 5, 20)),
    ]
    db.session.add_all(departments)
    db.session.commit()

    # Add locations
    locations = [
        Location(address="Nairobi", department_id=departments[0].id),
        Location(address="Mombasa", department_id=departments[0].id),
        Location(address="Kisumu", department_id=departments[1].id),
        Location(address="Kisumu", department_id=departments[2].id),
        Location(address="Kisumu", department_id=departments[3].id),
        Location(address="Kisumu", department_id=departments[4].id),
        Location(address="Nairobi", department_id=departments[5].id),
    ]
    db.session.add_all(locations)
    db.session.commit()

    # Create employees
    employees = [
        Employee(ssn=111111111, name="Alice Johnson", address="123 Main St", salary=70000, gender="F",
                 birthdate=date(1990, 5, 20), postal_address="P.O Box 123", tel_no="0700123456", department_id=departments[0].id),
        Employee(ssn=222222222, name="Bob Smith", address="456 Banana Ave", salary=80000, gender="M",
                 birthdate=date(1985, 7, 10), postal_address="P.O Box 456", tel_no="0712345678", department_id=departments[1].id, supervisor_ssn=111111111),
        Employee(ssn=333333331, name="Sandra Banchiri", address="789 Eldoret", salary=60000, gender="F",
                 birthdate=date(2006, 1, 27), postal_address="P.O Box 789", tel_no="0723456789", department_id=departments[2].id, supervisor_ssn=111111111),
        Employee(ssn=333333332, name="Clara James", address="756 Turbo", salary=50000, gender="F",
                 birthdate=date(1993, 3, 30), postal_address="P.O Box 675", tel_no="0745656675", department_id=departments[3].id, supervisor_ssn=111111111),
        Employee(ssn=333333333, name="Beyonce", address="234 Redstone", salary=40000, gender="F",
                 birthdate=date(1993, 6, 9), postal_address="P.O Box 267", tel_no="0712356675", department_id=departments[4].id, supervisor_ssn=111111111),
        Employee(ssn=333333334, name="Johnie", address="452 Nairobi", salary=30000, gender="M",
                 birthdate=date(2001, 3, 13), postal_address="P.O Box 788", tel_no="0704556675", department_id=departments[0].id, supervisor_ssn=111111111),
    ]
    db.session.add_all(employees)
    db.session.commit()

    # Set managers now that employees exist
    departments[0].manager_ssn = employees[0].ssn
    departments[1].manager_ssn = employees[1].ssn
    departments[2].manager_ssn = employees[2].ssn
    departments[3].manager_ssn = employees[3].ssn
    departments[4].manager_ssn = employees[4].ssn
    departments[5].manager_ssn = employees[5].ssn
    db.session.commit()

    # Create projects
    projects = [
        Project(name="Payroll System", number="101", location="Nairobi", department_id=departments[0].id),
        Project(name="AI Analytics", number="102", location="Kisumu", department_id=departments[1].id),
    ]
    db.session.add_all(projects)
    db.session.commit()

    # Assignments (WorksOn)
    works = [
        WorksOn(employee_ssn=111111111, project_id=projects[0].id, hours_per_week=10),
        WorksOn(employee_ssn=222222222, project_id=projects[1].id, hours_per_week=15),
        WorksOn(employee_ssn=333333333, project_id=projects[0].id, hours_per_week=20),
    ]
    db.session.add_all(works)
    db.session.commit()

    # Dependents
    dependents = [
        Dependent(employee_ssn=111111111, first_name="Charlie", gender="M", birthdate=date(2012, 9, 5), relationship="Son"),
        Dependent(employee_ssn=222222222, first_name="Sophie", gender="F", birthdate=date(2010, 12, 22), relationship="Daughter"),
        Dependent(employee_ssn=333333333, first_name="David", gender="M", birthdate=date(2014, 8, 14), relationship="Brother"),
    ]
    db.session.add_all(dependents)
    db.session.commit()

    print("✅ Database seeded successfully.")
