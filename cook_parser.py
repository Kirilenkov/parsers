import requests
from bs4 import BeautifulSoup as bs
import os
from multiprocessing import Pool
from time import time
PATH = 'C:/Users/Kirill/Desktop/Food/'
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


def food_parser(url, headers):
    titles = []
    sess = requests.Session()
    request = sess.get(url, headers=headers)
    if request.status_code == 200:
        print('{:s} [LOADED]'.format(url))
        soup = bs(request.content, 'html.parser')
        items = soup.find_all('h3', class_='horizontal-tile__item-title')
        for item in items:
            for tag in item.find_all('span'):
                recipe_title = tag.text.strip()
                titles.append(recipe_title)
    else:
        print('{:s} [LOADING ERROR]'.format(url))
    return titles


def write_to_txt(snippet):
    with open('desserts.txt', 'a', encoding='utf-8') as f:
        for titles in snippet:
            f.writelines(titles)
            f.write('\n')


def core(pars_url):
    write_to_txt(food_parser(pars_url, pars_headers))


@time_it_decorator
def main():
    os.chdir(PATH)
    queue = [f'https://eda.ru/recepty/vypechka-deserty?page={n}' for n in range(1, 715, 1)]
    with Pool(40) as p:
        p.map(core, queue)


if __name__ == '__main__':
    main()

