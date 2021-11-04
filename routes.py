import pymysql
from flask import render_template
from flask import jsonify
from flask import request

from app import app, auth
from config import mysql

from model.Employee import Employee
from model.Vacancy import Vacancy


SQL_DELETE_EMP = "DELETE FROM rest_emp WHERE id =%s"
SQL_UPDATE_EMP = "UPDATE rest_emp SET name=%s, email=%s, phone=%s, address=%s WHERE id=%s"
SQL_ADD_EMP = "INSERT INTO rest_emp(name, email, phone, address) VALUES(%s, %s, %s, %s)"
SQL_GET_EMPS = "SELECT id, name, email, phone, address FROM rest_emp"
SQL_GET_VACANCIES = "SELECT vacancy_id, title, url, body FROM vacancies"
SQL_ADD_VACANCIES_7ST = "INSERT INTO vacancies(vacancy_id, title, url, body) VALUES(%s, %s, %s, %s)"


@app.route('/')
@app.route('/index')
@auth.login_required
def index():
    user = {'username': auth.current_user()}
    posts = [
        {
            'author': {'username': 'C. S. Lewis'},
            'body': 'The Chronicles of Narnia'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/addvacancy', methods=['POST'])
@auth.login_required
def add_vacancy():
    try:
        app.config['MYSQL_DATABASE_DB'] = 'vacancies'
        required_fields = ("vacancy_id", "title", "url", "body")
        vacancy = Vacancy(**request.json)  # unpack json into Employee
        if vacancy.all_fields_filled(*required_fields) and request.method == 'POST':
            sqlQuery = (SQL_ADD_VACANCIES_7ST)
            bindData = tuple(getattr(vacancy, field) for field in required_fields)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            return return_success_vacancy()
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/getvacancies', methods=['GET'])
@auth.login_required
def get_vacancy():
    try:
        app.config['MYSQL_DATABASE_DB'] = 'vacancies'
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(SQL_GET_VACANCIES)
        vacancyRows = cursor.fetchall()
        response = jsonify(vacancyRows)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/addemp', methods=['POST'])
@auth.login_required
def add_emp():
    try:
        required_fields = ("name", "email", "phone", "address")
        employee = Employee(**request.json)  # unpack json into Employee
        if employee.all_fields_filled(*required_fields) and request.method == 'POST':
            sqlQuery = (SQL_ADD_EMP)
            bindData = tuple(getattr(employee, field) for field in required_fields)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            return return_success_emp()
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/getemp')
@auth.login_required
def emp():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(SQL_GET_EMPS)
        empRows = cursor.fetchall()
        response = jsonify(empRows)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/updateemp', methods=['PUT'])
@auth.login_required
def update_emp():
    try:
        _json = request.json
        required_fields = ("id", "name", "email", "phone", "address")
        employee = Employee(**request.json)  # unpack json into Employee
        if employee.all_fields_filled(*required_fields) and request.method == 'PUT':
            sqlQuery = (SQL_UPDATE_EMP)
            bindData = tuple(getattr(employee, field) for field in required_fields)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            return return_success_emp()
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


def return_success_emp():
    response = jsonify('Employee updated successfully!')
    response.status_code = 200
    return response


def return_success_vacancy():
    response = jsonify('Vacancy added successfully!')
    response.status_code = 200
    return response



@app.route('/deleteemp/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_emp(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute((SQL_DELETE_EMP), (id,))
        conn.commit()
        respone = jsonify('Employee deleted successfully!')
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.errorhandler(404)
@auth.login_required
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone
