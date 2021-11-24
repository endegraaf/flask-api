import pymysql
from flask import render_template
from flask import jsonify
from flask import request

import queries
from app import app, auth
from config import mysql

from model.Vacancy import Vacancy


@app.route('/')
@app.route('/index')
@auth.login_required
def index():
    user = {'username': auth.current_user()}
    posts = [
        {
            'author': {'username': 'C. S. Lewis'},
            'body': 'The Chronicles of Narnia'
        },
        {
            'author': {'username': 'Tolkien'},
            'body': 'LOTR'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/addvacancy', methods=['POST'])
@auth.login_required
def add_vacancy():
    try:
        required_fields = ("vacancy_id", "title", "url", "body")
        vacancy = Vacancy(**request.json)  # unpack json into Employee
        if vacancy.all_fields_filled(*required_fields) and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(queries.SQL_ADD_VACANCIES_7ST,
                           tuple(getattr(vacancy, field) for field in required_fields))
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
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(queries.SQL_GET_VACANCIES)
        vacancyRows = cursor.fetchall()
        response = jsonify(vacancyRows)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


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
        cursor.execute((queries.SQL_DELETE_EMP), (id,))
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
