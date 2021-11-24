import json
import re

import flask
import requests
from bs4 import BeautifulSoup
from flask import render_template, request, jsonify, make_response
import queries
from app import app, auth
from config import mysql
from model.Vacancy import Vacancy

base_url = 'https://sevenstars.nl/'
rest_path = 'professional/loadmore'
rest_url = base_url + rest_path
headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'}
search_body = {'type': '1', 'search': '', 'functiongroup': 'Tester', 'province': 'ALL', 'status': '1'}


def get_the_vacancy_ids(link_path):
    idtext = []
    for text in link_path:
        pattern = 'vacature/(.*)/'
        result = re.search(pattern, text['href'])
        idtext.append(result.group(1))
    return idtext


def get_details_from_data(soup_data):
    soup = BeautifulSoup(soup_data, 'html.parser')
    item = soup.find_all('a', class_='vacature-item')
    links = [a['href'] for a in soup.find_all('a', href=True)]
    titles = soup.find_all('h1')
    body = soup.find_all('p')
    ids = get_the_vacancy_ids(item)
    return zip(ids, titles, links, body)


@app.route('/scrape')
@auth.login_required
def scrape():
    response = requests.post(rest_url, data=search_body, headers=headers)
    data = response.json()
    print('amount_of_vacancies: ' + str(data['count']))
    vacancies = get_details_from_data(data['html'])
    for vacancy in vacancies:
        print(vacancy)
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(queries.SQL_ADD_VACANCIES_7ST, vacancy)
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
    user = {'username': auth.current_user()}
    my_headers = {'Authorization': 'Basic ZGVtbzpkZW1v'}
    response = requests.get('http://127.0.0.1:5000/getvacancies', headers=my_headers)
    return render_template('viewscrape.html', title='Scrape', user=user,
                           datas=response)


@app.route('/viewscrape')
@auth.login_required
def viewscrape():
    user = {'username': auth.current_user()}
    my_headers  = {'Authorization' : 'Basic ZGVtbzpkZW1v'}
    response = requests.get('http://127.0.0.1:5000/getvacancies', headers=my_headers)
    print(json.loads(response.text))
    return render_template('viewscrape.html', title='Scrape', user=user,
                           data=json.loads(response.text))

# str(get_the_vacancy_id(item[1])).strip(), item[0], item[1], item[2]
