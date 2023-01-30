from scrapy.selector import Selector
import undetected_chromedriver as uc
from datetime import datetime
import re

biddings = list(range(18))
years = [2021, 2022]
# Defining possible bidding dates
bidding_all = []
_date = datetime.today().strftime('%Y-%m-%d')


for year in years:
    for bidding in biddings:
        link_terracap = 'https://comprasonline.terracap.df.gov.br/bidding/external/index?utf8=%E2%9C%93&edict_year={}&edict_number={}&number_item=&commit=Consultar'.format(year, (bidding+1))
        print(link_terracap)
        temp = []
        # FIRST PAGE
        options = uc.ChromeOptions()
        options.headless = True
        options.add_argument('--headless')
        driver = uc.Chrome(options=options)
        driver.get(link_terracap)
        html = driver.page_source
        response_obj = Selector(text=html)
        item = response_obj.xpath('//div[contains(@class, "card")]')

        if len(item) >= 1:
            print('Edital {} do ano de {}'.format(bidding, year))
            for i in range(len(item)):
                link = item[i]
                titulo = link.xpath('.//div[contains(@class, "header")]/text()').get()
                features = link.xpath('.//div[contains(@class, "description")]/text()').getall()
                features.append(titulo)
                t=0
                for feat in features:
                    input_string = feat.split("\n")[1]
                    output_string = []
                    for index in range(len(input_string)):

                        if input_string[index] != ' ':
                            if space_flag == True:
                                if (input_string[index] == '.'
                                        or input_string[index] == '?'
                                        or input_string[index] == ','):
                                    pass
                                else:
                                    output_string.append(' ')
                                space_flag = False
                            output_string.append(input_string[index])
                        elif input_string[index - 1] != ' ':
                            space_flag = True
                    features[t] = output_string
                    t+=1
                    print(''.join(output_string))
                try:
                    endereco = ''.join(features[0]).split(': ')[1]
                except:
                    endereco = None

                try:
                    licitante = ''.join(features[1])
                    licitante = re.sub("[^0-9]", "", licitante)
                except:
                    licitante = None

                try:
                    valor = ''.join(features[2])
                    valor = valor.split(': ')[1].replace("R$", "")
                    valor = int(valor.split(',')[0].replace(".", ""))
                except:
                    valor = None

                try:
                    condicao = ''.join(features[3]).split(': ')[1]
                except:
                    condicao = None

                try:
                    meses = ''.join(features[4])
                    meses = int(re.sub("[^0-9]", "", meses))
                except:
                    meses = None

                try:
                    entrada = ''.join(features[5])
                    entrada = float(re.sub("[^0-9]", "", entrada))/100
                except:
                    entrada = None

                try:
                    edital = ''.join(features[6]).split(': ')[1]
                except:
                    edital = None
                try:
                    button = link.xpath('.//div[contains(@class, "button")]/text()').getall()[1]
                    button = int(re.sub("[^0-9]", "", button))
                except:
                    button = 'Desclassificado'

                'button'

                temp.append({
                    'edital': edital,
                    'colocacao': button,
                    'endereco': endereco,
                    'licitante': licitante,
                    'condicao': condicao,
                    'meses': meses,
                    'entrada': entrada,
                    'valor': valor,
                })
        else:
            print('Edital não disponível')

        temp = temp[1:len(temp)]
        bidding_all.extend(temp)


import pandas as pd
df = pd.DataFrame(bidding_all)