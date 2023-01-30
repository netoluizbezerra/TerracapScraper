# This is a sample Python script.
from scrapy.selector import Selector
import time
import json as json
import undetected_chromedriver as uc
from datetime import datetime
import pandas as pd

def get_imoveis_terracap():
    _date = datetime.today().strftime('%Y-%m-%d')
    link = 'https://comprasonline.terracap.df.gov.br/?edict_number=4&edict_year=2021&page=1&item=&ra=&destination=&min=&max=&area_min=&area_max='
    options = uc.ChromeOptions()
    options.headless = True
    #options.add_argument('--headless')
    driver = uc.Chrome()#options=options)
    driver.get(link)
    temp = []
    go = True
    html = driver.page_source
    response_obj = Selector(text=html)
    #Número de Páginas
    n_pages = response_obj.xpath('//font[contains(@id, "titulo-paginacao")]/text()').getall()[0]
    n_pages = int(n_pages.split('de')[1].split('\n')[0])
    time.sleep(3)
    for j in range(n_pages):
        num_page = 2+j
        time.sleep(5)

        #GETING everything
        item = response_obj.xpath('//div[contains(@class, "card mb-3 sombreado")]')
        for i in range(len(item)):
            link = item[i]
            titulo = link.xpath('.//h3[contains(@class, "card-title")]/text()').get()
            _all = link.xpath('.//p[contains(@class, "card-text")]/text()').getall()
            endereco = _all[0].split(': ')[1]
            bairro = _all[1].split(': ')[1]
            n_imoveis = int(_all[2].split(': ')[1])
            try:
                area = int(_all[3].split(': ')[1].replace("m²", ""))
            except:
                area = _all[3].split(': ')[1].replace("m²", "")
                area = int(area.split('.')[0])
            valor_compra_temp = _all[4].split(': ')[1].replace("R$", "")
            valor_compra = int(valor_compra_temp.split(',')[0].replace(".", ""))
            valor_caucao_temp = _all[4].split(': ')[1].replace("R$", "")
            valor_caucao = int(valor_caucao_temp.split(',')[0].replace(".", ""))
            uso = link.xpath('.//small[contains(@class, "text-muted")]/text()').getall()[0]
            coord_name = link.xpath('.//input[contains(@type, "hidden")]/@name').getall()[0]
            coords = link.xpath('.//input[contains(@type, "hidden")]/@value').getall()[0]

            temp.append({
                        'titulo': titulo,
                        'endereco': endereco,
                        'bairro': bairro,
                        'n_imoveis': n_imoveis,
                        'area': area,
                        'valor_compra': valor_compra,
                        'valor_caucao': valor_caucao,
                        'uso': uso,
                        'coord_name': coord_name,
                        'coords': coords
                        })

        try:
            _next = driver.find_element_by_xpath(
                '//a[contains(text(),{})]'.format(num_page)
            )
            _next.click()
        except:
            print("--## FIM DA CAPTURA ##--")

    with open('terracap_{}.json'.format(_date), 'w') as f:
        json.dump(temp, f)
    return temp

imoveis = get_imoveis_terracap()


df = pd.DataFrame(imoveis)
df.to_csv('edital_05_2021.csv')