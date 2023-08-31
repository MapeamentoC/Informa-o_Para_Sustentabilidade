import json
from selenium import webdriver
import glob
from time import sleep

options = webdriver.ChromeOptions()
prefs = {"profile.default_content_settings.popups": 0,
         "download.default_directory": "/dev/null",
         "directory_upgrade": True}
options.add_experimental_option("prefs", prefs)
options.add_argument("--headless")

driver = webdriver.Chrome(options=options)

for file in glob.glob('./istoe\\*.json'):
    file_name = file.replace(
        './istoe\\', '')
    saida = './istoe\\final\\'+file_name
    dkits = []
    with open(file, 'r', encoding='utf8') as infile:
        links = json.load(infile)
        for entrada in links:
            driver.get(entrada['link'])
            texto = ''
            if entrada['link'].find('istoe.com.br') >= 0:
                try:
                    titulo = driver.title
                except:
                    titulo = ''
                try:
                    para = driver.find_elements('css selector', 'article p')
                    for item in para:
                        if item.text.find('Inscreva-se nas nossas newsletters') < 0 and len(item.text) > 30:
                            texto += (item.text+'\n')
                except:
                    texto = ''

            elif entrada['link'].find('motorshow.com.br') >= 0:
                try:
                    titulo = driver.title
                except:
                    titulo = ''
                try:
                    para = driver.find_elements('css selector', 'article p')
                    for item in para:
                        if len(item.text) > 0 and item.text[0] != '+':
                            texto += (item.text+'\n')
                except:
                    texto = ''

            else:
                try:
                    titulo = driver.title
                except:
                    titulo = ''
                try:
                    para = driver.find_elements('css selector', 'article p')
                    for item in para:
                        if len(item.text) > 30:
                            texto += (item.text+'\n')
                except:
                    texto = ''

            final = {'Título': titulo, 'Texto': texto,
                     'link': entrada['link']}

            dkits.append(final)
            sleep(5)

        with open(saida, 'w', encoding='utf8') as outfile:
            for dicionario in dkits:
                json.dump(dicionario, outfile)
                outfile.write('\n')

driver.close()
