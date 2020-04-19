import requests
from bs4 import BeautifulSoup as bs
import lxml
from pprint import pprint
from fake_useragent import UserAgent
import pandas as pd

main_link = 'https://russia.superjob.ru/vacancy/search/?keywords=python'

response = requests.get(main_link, headers={'User-Agent': UserAgent().chrome}).text
soup = bs(response, 'lxml')

vacansys_result = []

next_button = soup.find('a', {'class': 'icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe'})
range_len = int(next_button.previous_element)

for i in range(0, range_len - 1):
    vacansy_block = soup.find('div', {'style': 'display:block'})
    vacansy_list = vacansy_block.find_all('div', {'class': 'iJCa5 _2gFpt _1znz6 _2nteL'}, recursive=False)

    for vacansy in vacansy_list:
        vacansy_data = {}
        data = vacansy.find('div', {'class': '_3mfro CuJz5 PlM3e _2JVkc _3LJqf'})
        data = data.findChild()
        vacansy_name = data.getText()
        vacansy_data['name'] = vacansy_name

        vacansy_link = data['href']
        vacansy_data['vacansy_link'] = 'https://russia.superjob.ru' + vacansy_link

        vacansy_from = vacansy_data['vacansy_link'].split('.')[1: 2]
        vacansy_data['vacansy_from'] = vacansy_from

        vacansy_salary = vacansy.find('span', {'class': '_3mfro _2Wp8I _31tpt f-test-text-company-item-salary'
                                                       ' PlM3e _2JVkc _2VHxz'}).getText()

        if vacansy_salary == 'По договорённости':
            vacansy_salary_money_type = None
            vacansy_salary_min = None
            vacansy_salary_max = None

        else:
            vacansy_salary = vacansy_salary.replace(u'\xa0', u' ')

            if vacansy_salary.split(' ')[0] == 'от':
                vacansy_salary_money_type = vacansy_salary[-4:].upper()
                vacansy_salary_min = int(vacansy_salary.split(' ')[1] + vacansy_salary.split(' ')[2])


            elif vacansy_salary.split(' ')[0] == 'до':
                vacansy_salary_money_type = vacansy_salary[-4:].upper()
                vacansy_salary_max = int(vacansy_salary.split(' ')[1] + vacansy_salary.split(' ')[2])

            #else vacansy_salary.split(' ')[1] == '—':
            else:
                vacansy_salary_money_type = vacansy_salary[-4:].upper()
                vacansy_salary_min = int(vacansy_salary.split(' ')[0] + vacansy_salary.split(' ')[1])
                vacansy_salary_max = int(vacansy_salary.split(' ')[3] + vacansy_salary.split(' ')[4])



        vacansy_data['salary_min'] = vacansy_salary_min
        vacansy_data['salary_max'] = vacansy_salary_max
        vacansy_data['money_type'] = vacansy_salary_money_type

        vacansys_result.append(vacansy_data)

next_page_link = soup.find('a', {'class': 'icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe'})['href']
response = requests.get(main_link + next_page_link, headers={'User-Agent': UserAgent().chrome}).text
soup = bs(response, 'lxml')

pprint(vacansys_result)
df_s_job = pd.DataFrame(vacansys_result)

pprint(df_s_job)

