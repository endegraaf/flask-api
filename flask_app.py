import pymysql
from flask import jsonify, render_template
from flask import request
from werkzeug.security import check_password_hash
import re
import requests
from bs4 import BeautifulSoup

from app import app, auth
from config import mysql, users

base_url = 'https://sevenstars.nl/'
rest_path = 'professional/loadmore'
rest_url = base_url + rest_path
headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'}
myobj = {'type': '1', 'search': '', 'functiongroup': 'Tester', 'province': 'ALL', 'status': '0',
         'status': '1'}


def sanitize_string(in_text):
    return str(in_text.replace('\n', '')).strip()


def get_details_from_data(soup_data):
    all_the_divs = []
    for divs in soup_data.find_all("div", class_='site-container__inner'):
        for li in divs.find_all("div", recursive=False):
            span = li.find("span")
            if span:
                all_the_divs.append(sanitize_string(li.text))
    return all_the_divs


@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username


# API
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


@app.route('/scrape')
@auth.login_required
def scrape():
    global soup_data
    response = requests.post(rest_url, data=myobj, headers=headers)
    data = response.json()
    amount_of_vacancies = data['count']
    if amount_of_vacancies > 0:
        pattern = '.*/vacature/(.*)\" class'
        result = re.match(pattern, data['html'])
        if result:
            get_the_data(result)
        else:
            print("I did not find any vacancies! " + data['html'])
    user = {'username': auth.current_user()}
    return render_template('scrape.html', title='Scrape', user=user,
                           datas=get_details_from_data(soup_data))


def get_the_data(result):
    global soup_data
    detail_rest_url = base_url + 'partial/vacature/' + result.group(1)
    print('get the detail url ' + detail_rest_url)
    details_response = requests.get(detail_rest_url)
    details_data = details_response.json()
    details_data_html = details_data['html']
    soup_data = BeautifulSoup(details_data_html, 'html.parser')


@app.route('/add', methods=['POST'])
@auth.login_required
def add_emp():
    try:
        _json = request.json
        _name = _json['name']
        print(_name)
        _email = _json['email']
        print(_email)
        _phone = _json['phone']
        print(_phone)
        _address = _json['address']
        print(_address)
        if _name and _email and _phone and _address and request.method == 'POST':
            sqlQuery = "INSERT INTO rest_emp(name, email, phone, address) VALUES(%s, %s, %s, %s)"
            bindData = (_name, _email, _phone, _address)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify('Employee added successfully!')
            response.status_code = 200
            return response
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/emp')
@auth.login_required
def emp():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, name, email, phone, address FROM rest_emp")
        empRows = cursor.fetchall()
        respone = jsonify(empRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/update', methods=['PUT'])
@auth.login_required
def update_emp():
    try:
        _json = request.json
        _id = _json['id']
        _name = _json['name']
        _email = _json['email']
        _phone = _json['phone']
        _address = _json['address']
        if _name and _email and _phone and _address and _id and request.method == 'PUT':
            sqlQuery = "UPDATE rest_emp SET name=%s, email=%s, phone=%s, address=%s WHERE id=%s"
            bindData = (_name, _email, _phone, _address, _id,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Employee updated successfully!')
            respone.status_code = 200
            return respone
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/delete/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_emp(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM rest_emp WHERE id =%s", (id,))
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


if __name__ == "__main__":
    app.run(debug=True)
