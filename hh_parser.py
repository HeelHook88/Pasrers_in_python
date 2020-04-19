import requests
from bs4 import BeautifulSoup as bs
import lxml
from pprint import pprint
from fake_useragent import UserAgent
import pandas as pd

main_link = 'https://nevinnomyssk.hh.ru/search/vacancy?clusters=true' \
            '&enable_snippets=true&salary=&st=searchVacancy&text=python'

response = requests.get(main_link, headers={'User-Agent': UserAgent().chrome}).text
soup = bs(response, 'lxml')

vacansys_result = []

next_button = soup.find('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'})
range_len = int(next_button.find_previous_sibling().findChild('a', {'class': 'bloko-button HH-Pager-Control'}).getText())

for i in range(0, range_len-1):
    vacansy_block = soup.find('div', {'class': 'vacancy-serp'})
    vacansy_list = vacansy_block.findChildren('div', {'class': 'vacancy-serp-item'}, recursive=False)

    for vacansy in vacansy_list:
        vacansy_data = {}

        data = vacansy.find('span', {'class': 'g-user-content'})
        data = data.findChild()

        vacansy_name = data.getText()
        vacansy_data['name'] = vacansy_name

        vacansy_link = data['href']
        vacansy_data['vacansy_link'] = vacansy_link

        vacansy_from = vacansy_link.split('.')[1: 2]
        vacansy_data['vacansy_from'] = vacansy_from

        vacansy_salary = vacansy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})

        vacansy_salary_money_type = None
        vacansy_salary_min = None
        vacansy_salary_max = None

        if vacansy_salary is not None:
            vacansy_salary = vacansy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).getText().replace(u'\xa0', u'')


            if vacansy_salary.split(' ')[0] == 'от':
                vacansy_salary_money_type = vacansy_salary[-4:].upper()
                vacansy_salary_min = vacansy_salary.split(' ')[1]

            elif vacansy_salary.split(' ')[0] == 'до':
                vacansy_salary_money_type = vacansy_salary[-4:].upper()
                vacansy_salary_max = vacansy_salary.split(' ')[1]

            else:
                vacansy_salary_money_type = vacansy_salary[-4:].upper()
                vacansy_salary_min = vacansy_salary.split('-')[0]
                vacansy_salary_max = vacansy_salary.split('-')[1].split(' ')[0]

            vacansy_data['salary_min'] = vacansy_salary_min
            vacansy_data['salary_max'] = vacansy_salary_max
            vacansy_data['money_type'] = vacansy_salary_money_type
        else:
            vacansy_data['salary_min'] = vacansy_salary_min
            vacansy_data['salary_max'] = vacansy_salary_max
            vacansy_data['money_type'] = vacansy_salary_money_type

        vacansys_result.append(vacansy_data)

    next_page_block = soup.find('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'})
    if next_page_block is False:
        break
    else:
        next_page_link = next_page_block['href']
        response = response = requests.get(main_link, headers={'User-Agent': UserAgent().chrome}).text
        soup = bs(response, 'lxml')

df_hh = pd.DataFrame(vacansys_result)


pprint(df_hh)

