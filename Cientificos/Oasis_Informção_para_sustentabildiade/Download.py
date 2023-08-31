import io
import PyPDF2
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
from bs4 import BeautifulSoup
from time import sleep
import validators


def read_pdf_from_url(url):
    text = ''
    cont = 0
    while True:
        cont += 1
        response = requests.get(url, verify=False)
        if b'405 Not Allowed' in response.content:
            text = '405 Not Allowed'
            break
        pdf_file = io.BytesIO(response.content)
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            break
        except:
            soup = BeautifulSoup(pdf_file)
            href_list = soup.find_all(href=True)
            for item in href_list:
                if 'download' in item.get('href'):
                    url = item.get('href')
                    break
        if cont > 2:
            text = 'Não Capturado'
            break

    if text != '405 Not Allowed' and text != 'Não Capturado':
        num_pages = len(pdf_reader.pages)
        text = ""

        for page_number in range(num_pages):
            page = pdf_reader.pages[page_number]
            text += page.extract_text()

    return text

def get_all_elements(dictionary_set, key):
    elements = []
    num_dictionaries = len(dictionary_set)
    max_elements = max(len(dictionary.get(key, []))
                       for dictionary in dictionary_set)

    for i in range(max_elements):
        for j in range(num_dictionaries):
            dictionary = dictionary_set[j]
            dictionary_elements = dictionary.get(key, [])
            if i < len(dictionary_elements):
                elements.append(dictionary_elements[i])

    return elements

def organiza_texo(texto):
    referencias = ['Bibliografia\n', 'Referências bibliográficas\n',
                   'Bibliografia consultada\n', 'Referências consultadas\n',
                   'Fontes consultadas\n', 'Referências bibliográficas consultadas\n']
    
    for item in referencias:
        if texto.find(item) != -1:
            texto = texto[:texto.find(item)]
            break   
    texto = texto.replace(' - \n', '')
    texto = texto.replace('\t', ' ')
    texto = texto.replace(' -\n', '')
    texto = texto.replace('-\n', '')
    texto = texto.replace('.\n', '.⁜')
    texto = texto.replace('?\n', '?⁜')
    texto = texto.replace('!\n', '!⁜')
    texto = texto.replace('\n', ' ')
    texto = texto.replace('.⁜', '.\n')
    texto = texto.replace('?⁜', '?\n')
    texto = texto.replace('!⁜', '!\n')
    return texto


options = webdriver.ChromeOptions()
prefs = {"profile.default_content_settings.popups": 0,
         "download.default_directory": "/dev/null",
         "directory_upgrade": True}
options.add_experimental_option("prefs", prefs)
options.add_argument("--headless")


# Inicializa o navegador com as opções configuradas
driver = webdriver.Chrome(options=options)


 



with open('C:\\Users\\isc_j\\OneDrive\\Documentos\\Py Projects\\Artigo_Lana\\Oasis\\textos_0.json', 'a', encoding='utf8') as outfile:
    with open('C:\\Users\\isc_j\\OneDrive\\Documentos\\Py Projects\\Artigo_Lana\\Oasis\\lista_final.json', 'r', encoding='utf8') as infile:
        for linha in infile:
            dict_base = json.loads(linha)
            link = dict_base['link']
            titulo = dict_base['titulo']
            fonts_to_ignore = ['bdjur.stj.jus.br', 'https://revistas.ufpr.br']
            font_valid = 0
            for item in fonts_to_ignore:
                if item in link:
                    font_valid = 1
            if font_valid == 0:
                try:
                    if link.find('||') > 0:
                        link = link.split('||')[0]
                    
                    driver.get(link)

                    sleep(2)
                    if driver.current_url.endswith('.com.br') or driver.current_url.endswith('.com.br/'):
                        print(('aqui'))
                        json.dump({'Título': titulo,
                                   'Link' : link,
                                   'Texto' : 'Página não encontrada'},
                                   outfile)
                        outfile.write('\n')
                        pass
                    elif ('<h1>400' in driver.page_source) or ('<h1>403' in driver.page_source) or ('<h1>404' in driver.page_source) or ('<h1>401' in driver.page_source):
                        json.dump({'Título': titulo,
                                   'Link' : link,
                                   'Texto' : 'Url quebrado, 400 ou 401, ou 403'},
                                   outfile)
                        outfile.write('\n')
                        pass
                    elif 'Página não encontrada' in driver.page_source:
                        json.dump ({'Título' : titulo,
                                    'Link' : link,
                                    'Texto' : 'Página não encontrada'},
                                    outfile)
                        outfile.write('\n')
                        pass
                    elif 'Não existem arquivos associados a este item' in driver.page_source:
                        json.dump ({'Título' : titulo,
                                    'Link' : link,
                                    'Texto' : 'Página não encontrada'},
                                    outfile)
                        outfile.write('\n')
                    else:
                        memo = ''
                        valid = 0
                        try:
                            try:
                                url = driver.find_element('partial link text','.pdf')
                                if 'article' in url.get_attribute('href') or 'bitstream' in url.get_attribute('href'):
                                    memo = url.get_attribute('href')
                                    valid = 1
                            except:
                                0
                            try:
                                if valid == 0:
                                    url = driver.find_element('partial link text','pdf')
                                    if 'article' in url.get_attribute('href') or 'bitstream' in url.get_attribute('href'):
                                        memo = url.get_attribute('href')
                                        valid = 1
                            except:
                                0
                            try:
                                if valid == 0:
                                    url = driver.find_element('partial link text','.PDF')
                                    if 'article' in url.get_attribute('href') or 'bitstream' in url.get_attribute('href'):
                                        memo = url.get_attribute('href')
                                        valid = 1
                            except:
                                0
                            try:
                                if valid == 0:
                                    url = driver.find_element('partial link text','PDF')
                                    if 'article' in url.get_attribute('href') or 'bitstream' in url.get_attribute('href'):
                                        memo = url.get_attribute('href')
                                        valid = 1
                            except:
                                0
                            try:
                                if valid == 0:
                                    lista = [item.get_attribute('href') for item in driver.find_elements('xpath', '//*[contains(a,href)]') if (item.get_attribute('href')) is not None]
                                    for item in lista:
                                        if '.pdf' in item:
                                            memo = item
                                            break
                                    if memo != '':
                                        valid = 1
                            except:
                                0
                            try:
                                if valid == 0:
                                    if memo == '':
                                        lista = [item.get_attribute('href') for item in driver.find_elements('xpath', '//*[contains(a,href)]') if (item.get_attribute('href')) is not None]
                                        for item in lista:
                                            if ('pdf' in item) and ('pt' in item):
                                                memo = item
                                                break
                                    if memo != '':
                                        valid = 1
                            except:
                                0
                            try:
                                if valid == 0:
                                    if memo == '':
                                        lista = [item.get_attribute('content') for item in driver.find_elements('css selector', 'meta') if validators.url(item.get_attribute('content'))]
                                        for item in lista:
                                            if 'pdf' in item:
                                                memo = item
                                                break
                                    if memo != '':
                                        valid = 1
                            except:
                                0
                        
                            try:
                                if valid == 0:
                                    if memo == '':
                                        lista = [item.get_attribute('content') for item in driver.find_elements('css selector', 'meta') if validators.url(item.get_attribute('content'))]
                                        for item in lista:
                                            if 'download' in item:
                                                memo = item
                                                break
                                    if memo != '':
                                        valid = 1
                            except:
                                0


                            curent = (driver.current_url)
                            try:
                                url_pdf = driver.get(memo)
                            except:
                                0
                            new = (driver.current_url)

                            if curent != new:
                                texto = read_pdf_from_url(driver.current_url)
                                memo = ''
                            if curent == new:
                                texto = read_pdf_from_url(memo)
                                memo = ''
                            texto = organiza_texo(texto)

                            json.dump({'Título' : titulo,
                                       'Link' : link,
                                       'Texto': texto},
                                       outfile)
                            outfile.write('\n')
                        except:
                            json.dump({'Título' : titulo,
                                       'Link' : link,
                                       'Texto': 'Não Capturado'},
                                       outfile)
                            outfile.write('\n')
                            pass
                except:
                    json.dump({'Título' : titulo,
                               'Link' : link,
                               'Texto' : 'Url quebrado'},
                               outfile)
                    outfile.write('\n')
                    pass
            else:
                pass
            

    


driver.close()
