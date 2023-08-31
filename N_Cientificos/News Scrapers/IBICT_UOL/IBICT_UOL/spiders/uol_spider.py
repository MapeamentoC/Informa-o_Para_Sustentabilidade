import scrapy
from scrapy import FormRequest
from scrapy.shell import inspect_response
from time import sleep
from selenium import webdriver


class UolSpiderSpider(scrapy.Spider):
    name = 'uol_spider'
    start_urls = ['https://www.google.com.br/']

    def __init__(self):
        self.driver = webdriver.Chrome()

    def parse(self, response):
        yield FormRequest.from_response(response,
                                        formdata={'q': '"sustentabilidade" "IstoÉ"',
                                                  'hl': 'pt-BR',
                                                  'tbm': 'nws',
                                                  },
                                        callback=self.result)

    def result(self, response):
        self.driver.get(response.url)
        self.driver.find_element('css selector', 'div#hdtb-tls').click()
        i = 0
        for item in self.driver.find_elements('css selector', '.KTBKoe'):
            if i == 1:
                item.click()
                break
            else:
                i += 1
        i = 0
        for item in self.driver.find_elements('css selector', 'g-menu-item'):
            if item.text == 'Intervalo personalizado...':
                item.click()
                break
        self.driver.find_element(
            'css selector', 'input#OouJcb').send_keys('01/01/2000')
        self.driver.find_element(
            'css selector', 'input#rzG2be').send_keys('19/09/2023')
        for item in self.driver.find_elements('css selector', 'g-button'):
            if item.text == 'Ir':
                item.click()
                break
        while True:
            for item in self.driver.find_elements('css selector', 'a'):
                try:
                    if item.get_attribute('href').find('istoe.com.br') > 0:
                        yield ({'link': item.get_attribute('href')})
                except:
                    0

            try:
                next_page = self.driver.find_element(
                    'css selector', 'a#pnnext')
                sleep(5)
                next_page.click()
            except:
                print('\n\n\n'+'NO MORE PAGES'+'\n\n\n')
                break
        self.driver.close()
