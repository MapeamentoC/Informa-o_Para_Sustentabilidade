from selenium import webdriver
from time import sleep
import json


query = 'sustentáveis'
date = '24/06/2023'

driver = webdriver.Chrome()

# initial page
driver.get('https://login.folha.com.br/login?done=https%3A%2F%2Fpaywall.folha.uol.com.br%2Ffolha%2Fretorno%3Fdone%3Dhttps%253A%252F%252Fwww.folha.uol.com.br%252F&service=portal')

# user data
email = 'mitelles@gmail.com'
senha = 'folha@123'

# login
email_form = driver.find_element('css selector', '#registerEmail')
email_form.send_keys(email)
senha_form = driver.find_element('css selector', '#registerPassword')
senha_form.send_keys(senha)
botao = driver.find_element('xpath', "//*[text()='Entrar']")
botao.click()

# search
buscar = driver.find_element('xpath', "//*[text()='Buscar']")
buscar.click()
search_box = driver.find_element('css selector', '#query')
search_box.send_keys(query)
botao = driver.find_element('css selector', '.c-search__search-btn')
botao.click()

# refine
botao = driver.find_element('css selector', '.banner-lgpd-consent__accept')
botao.click()
botao = driver.find_elements('css selector', '.c-form__default')
for item in botao:
    if item.text == 'PERSONALIZADO':
        item.click()
botao = driver.find_elements('css selector', '.c-form__radio')
for item in botao:
    if item.text == 'PERSONALIZADO':
        item.click()
caixa_ini = driver.find_element('css selector', '#sd')
caixa_ini.send_keys('01/01/2000')
caixa_fin = driver.find_element('css selector', '#ed')
caixa_fin.send_keys(date)
botao = driver.find_elements('css selector', '.c-button--full')
for i in range(len(botao)):
    if i == 1:
        botao[i].click()

# capture
next_cont = 0
with open('./'+query+'.json', 'a', encoding='utf8') as outfile:
    while True:
        sleep(5)
        source = driver.current_url
        news = driver.find_elements('css selector', '.c-headline__title')
        total_news = len(news)
        for i in range(total_news):
            try:
                sleep(5)
                news = driver.find_elements(
                    'css selector', '.c-headline__title')
                news[i].click()
                titulo = driver.find_element(
                    'css selector', '.c-content-head__title').text
                texto = driver.find_element(
                    'css selector', '.c-content-head__subtitle').text+'\n'
                corpo = driver.find_elements('css selector', '.c-news__body p')

                for item in corpo:
                    if len(item.text) > 2 and 'Receba no seu email o que de mais' not in item.text and 'Carregando...' not in item.text and 'PUBLICIDADE' not in item.text:
                        texto += item.text+'\n'

                json.dump({'Título': titulo,
                           'Texto': texto,
                           'Link' : driver.current_url}, outfile)
                outfile.write('\n')
            except:
                json.dump({'Título': 'Não capturado',
                          'Texto': 'Não capturado',
                          'Link' : driver.current_url}, outfile)
                outfile.write('\n')
            driver.get(source)

        # next_page
        try:
            next_p = driver.find_elements(
                'css selector', '.c-pagination__arrow')
            if next_cont == 0:
                next_p[0].click()
            if next_cont > 0:
                next_p[1].click()
            next_cont += 1
        except:
            break
