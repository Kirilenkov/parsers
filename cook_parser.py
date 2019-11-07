import requests
from bs4 import BeautifulSoup as bs
import os
from time import time
PATH = 'C:/Users/Kirill/Desktop/Foods/'

pars_headers = {'accept': '*/*',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                         ' AppleWebKit/537.36 (KHTML, like Gecko)'
                         ' Chrome/77.0.3865.120 Safari/537.36'}


def time_it_decorator(func):
    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        print(time() - start)
        return result
    return wrapper


@time_it_decorator
def food_parser(url, headers):
    titles = []
    sess = requests.Session()
    request = sess.get(url, headers=headers)
    if request.status_code == 200:
        print('LOADED')
        soup = bs(request.content, 'html.parser')
        items = soup.find_all('h3', class_='horizontal-tile__item-title')
        for item in items:
            for tag in item.find_all('span'):
                recipe_title = tag.text.strip()
                titles.append(recipe_title)
    else:
        print('LOADING ERROR')
    return titles


@time_it_decorator
def main():
    os.chdir(PATH)
    common_titles = []
    for i in range(10):
        print(f'Загружается страница № {i + 1}')
        pars_url = f'https://eda.ru/recepty/osnovnye-blyuda/russkaya-kuhnya?page={i + 1}'
        common_titles.append(food_parser(pars_url, pars_headers))
    with open('recipe_list.txt', 'w', encoding='utf-8') as f:
        for titles in common_titles:
            f.writelines('\n'.join(titles))
            f.write('\n')


if __name__ == '__main__':
    main()

