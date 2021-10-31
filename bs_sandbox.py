from bs4 import BeautifulSoup

input_blob = """
"""

soup = BeautifulSoup(input_blob, 'html.parser')
#item = soup.find_all('a', class_='vacature-item')
links = [a['href'] for a in soup.find_all('a', href=True)]
titles = soup.find_all('h1')
body = soup.find_all('p')
collection = {}
collection = zip(titles, links, body)
for item in collection:
    print(item)