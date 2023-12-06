from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
db = SQLAlchemy(app)
api = Api(app)


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    designation = db.Column(db.String(255))
    company = db.Column(db.String(255))
    date_of_joining = db.Column(db.Date)
    contact = db.Column(db.String(20))
    email = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_edit_at = db.Column(db.DateTime)


with app.app_context():
    db.create_all()


class EmployeeResource(Resource):
    def get(self, employee_id):
        employee = Employee.query.get_or_404(employee_id)
        return {
            'id': employee.id,
            'name': employee.name,
            'dob': str(employee.dob),
            'designation': employee.designation,
            'company': employee.company,
            'date_of_joining': str(employee.date_of_joining),
            'contact': employee.contact,
            'email': employee.email,
            'created_at': str(employee.created_at),
            'last_edit_at': str(employee.last_edit_at)
        }

    def put(self, employee_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('dob', type=str, required=True)
        parser.add_argument('designation', type=str)
        parser.add_argument('company', type=str)
        parser.add_argument('date_of_joining', type=str)
        parser.add_argument('contact', type=str)
        parser.add_argument('email', type=str, required=True)
        args = parser.parse_args()

        employee = Employee.query.get_or_404(employee_id)

        employee.name = args['name']
        employee.dob = datetime.strptime(args['dob'], '%Y-%m-%d')
        employee.designation = args['designation']
        employee.company = args['company']
        employee.date_of_joining = datetime.strptime(args['date_of_joining'], '%Y-%m-%d') if args[
            'date_of_joining'] else None
        employee.contact = args['contact']
        employee.email = args['email']
        employee.last_edit_at = datetime.utcnow()

        db.session.commit()

        return {'message': 'Employee updated successfully'}

    def delete(self, employee_id):
        employee = Employee.query.get_or_404(employee_id)

        db.session.delete(employee)
        db.session.commit()

        return {'message': 'Employee deleted successfully'}


class EmployeeListResource(Resource):
    def get(self):
        employees = Employee.query.all()
        employee_list = [{
            'id': employee.id,
            'name': employee.name,
            'dob': str(employee.dob),
            'designation': employee.designation,
            'company': employee.company,
            'date_of_joining': str(employee.date_of_joining),
            'contact': employee.contact,
            'email': employee.email,
            'created_at': str(employee.created_at),
            'last_edit_at': str(employee.last_edit_at)
        } for employee in employees]

        return {'employees': employee_list}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('dob', type=str, required=True)
        parser.add_argument('designation', type=str)
        parser.add_argument('company', type=str)
        parser.add_argument('date_of_joining', type=str)
        parser.add_argument('contact', type=str)
        parser.add_argument('email', type=str, required=True)
        args = parser.parse_args()

        new_employee = Employee(
            name=args['name'],
            dob=datetime.strptime(args['dob'], '%Y-%m-%d'),
            designation=args['designation'],
            company=args['company'],
            date_of_joining=datetime.strptime(args['date_of_joining'], '%Y-%m-%d') if args['date_of_joining'] else None,
            contact=args['contact'],
            email=args['email']
        )

        db.session.add(new_employee)
        db.session.commit()

        return {'message': 'Employee added successfully'}, 201


api.add_resource(EmployeeResource, '/employee/<int:employee_id>')
api.add_resource(EmployeeListResource, '/employees')

if __name__ == '__main__':
    app.run(debug=True)
