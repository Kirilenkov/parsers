import requests
import xlsxwriter as excel
import datetime as dt
from bs4 import BeautifulSoup as bs
import os
from time import time
PATH = '/Users/kirill/results'
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


'''def link_input():
    return input('Paste the link to the product page: \n')'''


def dns_parser(url, headers):
    useful_content = []
    sess = requests.Session()
    request = sess.get(url, headers=headers)
    if request.status_code == 200:
        print('{:s} [LOADED]'.format(url))
        soup = bs(request.content, 'html.parser')
        table = soup.find('table', class_='table-params table-no-bordered')
        raws = table.find_all('tr')
        for raw in raws:
            line = ''
            for column in raw.find_all('td'):
                line += column.text.strip() + '\t'
            print(line)
            useful_content.append(line)
    else:
        print('{:s} [LOADING ERROR]'.format(url))
    return useful_content


def write_to_txt(snippet):
    with open('specification.txt', 'w', encoding='utf-8') as f:
        for titles in snippet:
            f.writelines(titles)
            f.write('\n')


def write_to_excel(file):
    workbook = excel.Workbook("spec.xlsx")
    worksheet = workbook.add_worksheet()
    merge_format = workbook.add_format({
        'bold': 1,
        # 'valign': 'vcenter',
        'align': 'center'})
    row = 0
    column = 0
    f = open(file, 'r', encoding='utf-8')
    for line in f:
        items = line.split('\t')
        for item in items:
            try:
                worksheet.write(row, column, item)
            except:
                item = 'N/A'
                worksheet.write(row, column, item)
                print('Не удалось записать значение в файл excel \n'
                      'в позиции строка {0:d} столбец {1:d}'.format(row + 1, column))
            finally:
                column += 1
                if items.__len__() == 2:
                    worksheet.merge_range('A{0:d}:B{0:d}'.format(row + 1), items[0], merge_format)
        column = 0
        row += 1
    worksheet.set_column('A:B', 40)
    workbook.close()


def core(pars_url):
    write_to_txt(dns_parser(pars_url, pars_headers))
    write_to_excel('specification.txt')


@time_it_decorator
def main():
    os.chdir(PATH)
    core('https://www.dns-shop.ru/product/8bf0324586723332/65-164-sm-televizor-led-lg-65sm8200pla-cernyj/characteristics/')


if __name__ == '__main__':
    main()

