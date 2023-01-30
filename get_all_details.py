from scrapy.selector import Selector
import time
import undetected_chromedriver as uc
import re
import pandas as pd

biddings = list(range(1, 18))
num_imovel_list = list(range(1, 130))
year = 2022
bidding = 1
num_imovel = 1

# Defining possible bidding dates
bidding_all = []

for bidding in biddings:
    for num_imovel in num_imovel_list:
        link_terracap = 'https://comprasonline.terracap.df.gov.br/item/external/show?edict_number={}&edict_year={}&item={}'.format(bidding, year, num_imovel)
        print(link_terracap)
        time.sleep(15)
        temp = []
        # FIRST PAGE
        options = uc.ChromeOptions()
        options.headless = True
        options.add_argument('--headless')
        driver = uc.Chrome(options=options)
#        driver = Chrome()
#        driver.get(link_terracap)
        html = driver.page_source
        response_obj = Selector(text=html)

        try:
            item = response_obj.xpath('//div[contains(@class, "form-body")]')
            items = item.xpath('.//div[contains(@class, "form-control")]/text()').getall()

            try:
                edital = items[0]
            except:
                edital = None

            try:
                n_imovel_no_edital = int(items[1])
            except:
                n_imovel_no_edital = None

            try:
                valor_face = items[2]
                valor_face = valor_face.replace("R$", "")
                valor_face = int(valor_face.split(',')[0].replace(".", ""))
            except:
                valor_face = None

            try:
                valor_caucao = items[3]
                valor_caucao = valor_caucao.replace("R$", "")
                valor_caucao = int(valor_caucao.split(',')[0].replace(".", ""))
            except:
                valor_caucao = None

            try:
                cond_pgto = items[4]
            except:
                cond_pgto = None

            time.sleep(4)

            try:
                _next = driver.find_element_by_xpath("//a[contains(@class, 'fa fa-info')]")
                _next.click()
            except:
                print("--## FIM DA CAPTURA ##--")
            # Lista de atributos
            driver.switch_to.window(driver.window_handles[1])
            html = driver.page_source
            response = Selector(text=html)

            # Destinação de Uso do Lote:
            destinacao = response.xpath('//textarea[contains(@class, "form-control")]/text()').extract()[0]

            list_att = response.xpath('//div[contains(@class, "form-control")]/text()').extract()
            # Número de Identificação do Imóvel:
            id_terracap = list_att[0]

            # Endereço:
            end = list_att[1]

            # TESTES DE COERENCIA
            lista_teste_situacao = ["FIRME", "REGULAR", "IRREGULAR", "ISOLADO", "MEIO DA QUADRA", "ESQUINA"]
            lista_teste_tipo_solo = ["REGULAR", "IRREGULAR", "ISOLADO", "MEIO DA QUADRA", "ESQUINA"]
            lista_teste_forma = ["ISOLADO", "MEIO DA QUADRA", "ESQUINA"]

            # Número do Item:
            classificacao = list_att[2]
            if classificacao == 'PLANO':
                classificacao = str(10)
                relevo = list_att[2]
            else:
                relevo = list_att[3]

            if any(char.isdigit() for char in relevo) and any(char.isdigit() for char in classificacao):
                classificacao = None
                relevo = None
                area = list_att[2]
                area = area.split(".")[0]
                area_const_basica = list_att[3]
                area_const_basica = area_const_basica.split(".")[0]
                area_const_max = list_att[4]
                area_const_max = area_const_max.split(".")[0]
                try:
                    situacao = list_att[5]
                    if any(situacao == i for i in lista_teste_situacao):
                        situacao = None
                        tipo_de_solo = list_att[5]
                        if any(tipo_de_solo == i for i in
                         lista_teste_tipo_solo):
                            tipo_de_solo = None
                            forma =  list_att[5]
                            if any(forma == i for i in lista_teste_forma):
                                forma = None
                                posicao = list_att[5]
                            else:
                                try:
                                    posicao = list_att[6]
                                except:
                                    posicao = None
                        else:
                            try:
                                forma = list_att[6]
                                if any(forma == i for i in lista_teste_forma):
                                    forma = None
                                    posicao = list_att[6]
                                else:
                                    try:
                                        posicao = list_att[7]
                                    except:
                                        posicao = None
                            except:
                                forma = None
                                posicao = None
                    else:
                        try:
                            tipo_de_solo = list_att[6]
                            if any(tipo_de_solo == i for i in lista_teste_tipo_solo):
                                tipo_de_solo = None
                                forma =  list_att[6]
                                if any(forma == i for i in lista_teste_forma):
                                    forma = None
                                    posicao = list_att[6]
                                else:
                                    try:
                                        posicao = list_att[7]
                                    except:
                                        posicao = None
                            else:
                                try:
                                    forma = list_att[7]
                                    if any(forma == i for i in lista_teste_forma):
                                        forma = None
                                        posicao = list_att[7]
                                    else:
                                        try:
                                            posicao = list_att[8]
                                        except:
                                            posicao = None
                                except:
                                    forma = None
                                    posicao = None
                        except:
                            tipo_de_solo = None
                            forma = None
                            posicao = None
                except:
                    situacao = None
                    tipo_de_solo = None
                    forma = None
                    posicao = None

            elif any(char.isdigit() for char in relevo) or any(char.isdigit() for char in classificacao):
                if any(char.isdigit() for char in classificacao):
                    classificacao = None
                else:
                    classificacao = list_att[2]

                if any(char.isdigit() for char in relevo):
                    relevo = None
                else:
                    relevo = list_att[2]

                area = list_att[3]
                area = area.split(".")[0]
                area_const_basica = list_att[4]
                area_const_basica = area_const_basica.split(".")[0]
                area_const_max = list_att[5]
                area_const_max = area_const_max.split(".")[0]

                try:
                    situacao = list_att[6]
                    if any(situacao == i for i in lista_teste_situacao):
                        situacao = None
                        tipo_de_solo = list_att[6]
                        if any(tipo_de_solo == i for i in lista_teste_tipo_solo):
                            tipo_de_solo = None
                            forma =  list_att[6]
                            if any(forma == i for i in lista_teste_forma):
                                forma = None
                                posicao = list_att[6]
                            else:
                                try:
                                    posicao = list_att[7]
                                except:
                                    posicao = None
                        else:
                            try:
                                forma = list_att[7]
                                if any(forma == i for i in lista_teste_forma):
                                    forma = None
                                    posicao = list_att[7]
                                else:
                                    try:
                                        posicao = list_att[8]
                                    except:
                                        posicao = None
                            except:
                                forma = None
                                posicao = None
                    else:
                        try:
                            tipo_de_solo = list_att[7]
                            if any(tipo_de_solo == i for i in lista_teste_tipo_solo):
                                tipo_de_solo = None
                                forma =  list_att[7]
                                if any(forma == i for i in lista_teste_forma):
                                    forma = None
                                    posicao = list_att[7]
                                else:
                                    try:
                                        posicao = list_att[8]
                                    except:
                                        posicao = None
                            else:
                                try:
                                    forma = list_att[8]
                                    if any(forma == i for i in lista_teste_forma):
                                        forma = None
                                        posicao = list_att[8]
                                    else:
                                        try:
                                            posicao = list_att[9]
                                        except:
                                            posicao = None
                                except:
                                    forma = None
                                    posicao = None
                        except:
                            tipo_de_solo = None
                            forma = None
                            posicao = None
                except:
                    situacao = None
                    tipo_de_solo = None
                    forma = None
                    posicao = None

            else:
                area = list_att[4]
                area = area.split(".")[0]
                area_const_basica = list_att[5]
                area_const_basica = area_const_basica.split(".")[0]
                area_const_max = list_att[6]
                area_const_max = area_const_max.split(".")[0]

                try:
                    situacao = list_att[7]
                    if any(situacao == i for i in lista_teste_situacao):
                        situacao = None
                        tipo_de_solo = list_att[7]
                        if any(tipo_de_solo == i for i in lista_teste_tipo_solo):
                            tipo_de_solo = None
                            forma =  list_att[7]
                            if any(forma == i for i in lista_teste_forma):
                                forma = None
                                posicao = list_att[7]
                            else:
                                try:
                                    posicao = list_att[8]
                                except:
                                    posicao = None
                        else:
                            try:
                                forma = list_att[8]
                                if any(forma == i for i in lista_teste_forma):
                                    forma = None
                                    posicao = list_att[8]
                                else:
                                    try:
                                        posicao = list_att[9]
                                    except:
                                        posicao = None
                            except:
                                forma = None
                                posicao = None
                    else:
                        try:
                            tipo_de_solo = list_att[8]
                            if any(tipo_de_solo == i for i in lista_teste_tipo_solo):
                                tipo_de_solo = None
                                forma =  list_att[8]
                                if any(forma == i for i in lista_teste_forma):
                                    forma = None
                                    posicao = list_att[8]
                                else:
                                    try:
                                        posicao = list_att[9]
                                    except:
                                        posicao = None
                            else:
                                try:
                                    forma = list_att[9]
                                    if any(forma == i for i in lista_teste_forma):
                                        forma = None
                                        posicao = list_att[9]
                                    else:
                                        try:
                                            posicao = list_att[10]
                                        except:
                                            posicao = None
                                except:
                                    forma = None
                                    posicao = None
                        except:
                            tipo_de_solo = None
                            forma = None
                            posicao = None
                except:
                    situacao = None
                    tipo_de_solo = None
                    forma = None
                    posicao = None

            # Dimensões do Lote
            dimensions = response.xpath('//div[contains(@class, "description")]/text()').extract()

        # Frente
            try:
                frente = dimensions[0]
                frente = frente.split(",")[0]
                frente = re.sub("[^0-9]", "", frente)
                if len(frente) >= 4:
                    frente = None
                else:
                    frente = int(frente)
            except:
                frente = None

                # Fundo
            try:
                fundo = dimensions[1]
                fundo = fundo.split(",")[0]
                fundo = re.sub("[^0-9]", "", fundo)
                if len(fundo) >= 4:
                    fundo = None
                else:
                    fundo = int(fundo)
            except:
                fundo = None

            # Lado Direito
            try:
                lado_direito = dimensions[2]
                lado_direito = lado_direito.split(",")[0]
                lado_direito = re.sub("[^0-9]", "", lado_direito)
                if len(lado_direito) >= 4:
                    lado_direito = None
                else:
                    lado_direito = int(lado_direito)
            except:
                lado_direito = None

            # Lado Esquerdo
            try:
                lado_esquerdo = dimensions[3]
                lado_esquerdo = lado_esquerdo.split(",")[0]
                lado_esquerdo = re.sub("[^0-9]", "", lado_esquerdo)
                if len(lado_esquerdo) >= 4:
                    lado_esquerdo = None
                else:
                    lado_esquerdo = int(lado_esquerdo)
            except:
                lado_esquerdo = None

            temp.append({
                'edital': edital,
                'n_imovel_no_edital': n_imovel_no_edital,
                'destinacao': destinacao,
                'area': area,
                'area_const_basica': area_const_basica,
                'area_const_max': area_const_max,
                'valor_face': valor_face,
                'valor_caucao': valor_caucao,
                'cond_pgto': cond_pgto,
                'id_terracap': id_terracap,
                'end': end,
                'classficacao': classificacao,
                'relevo': relevo,
                'situacao': situacao,
                'tipo_de_solo': tipo_de_solo,
                'forma': forma,
                'posicao': posicao,
                'frente': frente,
                'fundo': fundo,
                'lado_direito': lado_direito,
                'lado_esquerdo': lado_esquerdo,
            })

        except:
            print('fim')
        bidding_all.extend(temp)






