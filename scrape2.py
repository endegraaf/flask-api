# https://github.com/h2non/jsonpath-ng
import jsonpath_ng
import requests

base_url = 'https://jobcatcher.nl/'
rest_path = 'api2/v1/requestsearch/search?currentpage=1&itemsperpage=100&search=test%20automation%20engineer&knowledgearea=78'
rest_url = base_url + rest_path
headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'}


response = requests.get(rest_url, headers=headers)
data = response.json()
if data:
        jsonpath_expr = jsonpath_ng.parse('$.Data.[0].List')
        list_val = [match.value for match in jsonpath_expr.find(data)]
        for val in list_val:
            print('vacancy id: ' + str(val[0]['requestid']))