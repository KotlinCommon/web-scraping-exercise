import json

import requests
from bs4 import BeautifulSoup

# Initialize an empty list to store the information
base_url = 'https://www.metacritic.com'
# Define the URL of the first page
# url_template = 'https://www.metacritic.com/browse/games/score/metascore/all/pc/filtered?view=condensed&page={page}'
url_template = 'https://www.metacritic.com/browse/games/score/metascore/all/pc/filtered?view=detailed&page={page}'

# Define the number of pages to scrape
num_pages = 53
count = 0
# Iterate through the pages
for page in range(num_pages):
    url = url_template.format(page=page)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.82 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    games = []
    first = True
    for item in soup.find_all('tr'):
        count += 1
        print(count)
        # print(item)
        if item.find('h3', text=True) is None:
            continue
        if item.find('div', class_='metascore_w') is None:
            continue
        if item.find('a', class_='title').get('href') is None:
            continue
        if item.findAll('span', class_=not "title numbered")[0].text.strip('[]') is None:
            continue

        game = {'title': ''.join(item.find('h3').findAll(text=True)),
                'meta_score': ''.join(item.find('div', class_='metascore_w').findAll(text=True)),
                'img': item.findAll('img')[0]['src'],
                'link': base_url + item.find('a', class_='title').get('href'),
                'release_date': item.findAll('span', class_=not "title numbered")[0].text.strip('[]')}

        games.append(game)
    name = 'games_'
    name += str(page)
    with open(name + '.json', 'w') as json_file:
        json.dump(games, json_file, indent=2)
print('finished')
