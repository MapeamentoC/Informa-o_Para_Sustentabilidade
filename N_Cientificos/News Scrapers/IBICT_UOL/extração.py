import json
from selenium import webdriver
import glob
from time import sleep

driver = webdriver.Firefox()

for file in glob.glob('C:\\Users\\isc_j\\OneDrive\\Documentos\\Py Projects\\Artigo_Lana\\IBICT_UOL\\IBICT_UOL\\*.json'):
    file_name = file.replace(
        'C:\\Users\\isc_j\\OneDrive\\Documentos\\Py Projects\\Artigo_Lana\\IBICT_UOL\\IBICT_UOL\\', '')
    saida = 'C:\\Users\\isc_j\\OneDrive\\Documentos\\Py Projects\\Artigo_Lana\\IBICT_UOL\\IBICT_UOL\\final\\'+file_name
    dkits = []
    with open(file, 'r', encoding='utf8') as infile:
        links = json.load(infile)
        for entrada in links:
            driver.get(entrada['link'])
            try:
                titulo = driver.find_element(
                    'css selector', 'i.custom-title').text
            except:
                titulo = ''

            try:
                texto = driver.find_element('css selector', 'div.text').text
                texto = texto.replace('\nPUBLICIDADE', '').replace(
                    '\nRELACIONADAS', '')
            except:
                texto = ''
            try:
                autor = driver.find_element(
                    'css selector', 'p.p-author-local').text
            except:
                autor = ''

            try:
                time = driver.find_element('css selector', 'p.p-author').text
                time = time.replace('Atua', ' Atua')
            except:
                time = ''

            final = {'Título': titulo, 'Texto': texto,
                     'Autor': autor, 'Data': time}

            dkits.append(final)
            sleep(5)
        with open(saida, 'w', encoding='utf8') as outfile:
            for dicionario in dkits:
                json.dump(dicionario, outfile)

        driver.close()
