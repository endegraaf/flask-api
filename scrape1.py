import re
import requests
from bs4 import BeautifulSoup

base_url = 'https://sevenstars.nl/'
rest_path = 'professional/loadmore'
rest_url = base_url + rest_path
headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'}
myobj = {'type': '1', 'search': '', 'functiongroup': 'Tester', 'province': 'ALL', 'status': '1'}

response = requests.post(rest_url, data=myobj, headers=headers)
data = response.json()
amount_of_vacancies = data['count']

print('Found ' + str(amount_of_vacancies) + ' vacancies')


def get_the_vacancy_id(link_path):
    pattern = '.*/vacature/(.*)/'
    result = re.findall(pattern, link_path)
    return int(result[0])


def get_details_from_data(soup_data):
    soup = BeautifulSoup(soup_data, 'html.parser')
    # item = soup.find_all('a', class_='vacature-item')
    links = [a['href'] for a in soup.find_all('a', href=True)]
    titles = soup.find_all('h1')
    body = soup.find_all('p')
    collection = zip(titles, links, body)
    for item in collection:
        print(item[0], str(get_the_vacancy_id(item[1])), item[1], item[2])


get_details_from_data(data['html'])

