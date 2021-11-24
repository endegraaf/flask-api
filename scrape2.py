# https://github.com/h2non/jsonpath-ng
import json
import re

import jsonpath_ng
import requests
from bs4 import BeautifulSoup
from flask import render_template

import queries
from app import app, auth
from config import mysql

base_url = 'https://jobcatcher.nl/'
rest_path = 'api2/v1/requestsearch/search?currentpage=1&itemsperpage=100&search=test%20automation%20engineer&knowledgearea=78'
rest_url = base_url + rest_path
headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'}


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


@app.route('/scrape_jc')
@auth.login_required
def scrape_jc():
    response = requests.get(rest_url, headers=headers)
    data = response.json()
    if data:
        jsonpath_expr = jsonpath_ng.parse('$.Data.[0].List')
        list_val = [match.value for match in jsonpath_expr.find(data)]
        for vacancy in list_val:
            print('vacancy id: ' + str(vacancy[0]['requestid']))
            # try:
            #     conn = mysql.connect()
            #     cursor = conn.cursor()
            #     cursor.execute(queries.SQL_ADD_VACANCIES_JC, vacancy)
            #     conn.commit()
            # except Exception as e:
            #     print(e)
            # finally:
            #     cursor.close()
            #     conn.close()

    user = {'username': auth.current_user()}
    my_headers = {'Authorization': 'Basic ZGVtbzpkZW1v'}
    response = requests.get('http://127.0.0.1:5000/getvacancies', headers=my_headers)
    return render_template('viewscrape.html', title='Scrape', user=user,
                           datas=response)


@app.route('/viewscrape_jc')


@auth.login_required
def viewscrape_jc():
    user = {'username': auth.current_user()}
    my_headers = {'Authorization': 'Basic ZGVtbzpkZW1v'}
    response = requests.get('http://127.0.0.1:5000/getvacancies', headers=my_headers)
    print(json.loads(response.text))
    return render_template('viewscrape.html', title='Scrape', user=user,
                           data=json.loads(response.text))
