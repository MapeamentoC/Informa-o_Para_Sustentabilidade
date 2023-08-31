import scrapy
from scrapy import FormRequest
from scrapy.shell import inspect_response


class G1SpiderSpider(scrapy.Spider):
    name = 'g1_spider'
    start_urls = ['https://g1.globo.com/busca/']

    def parse(self, response):
        yield FormRequest.from_response(response,
                                        formdata={
                                            'q': 'sustentavel',
                                            'page': '1',
                                            'order': 'recent',
                                            'species': 'notícias',
                                            'ajax': '1'},
                                        callback=self.results)

    def results(self, response):
        for materia in response.css('.widget--info'):
            yield {
                'titulo': materia.css('.widget--info div.widget--info__title::text').get(),
                'link': materia.css('.widget--info div.widget--info__text-container a::attr(href)').get()}
        try:
            next_page_part = response.css('div.pagination a::attr(href)').get()
            next_page = response.urljoin(next_page_part)
            yield scrapy.Request(next_page, callback=self.results)
        except:
            0
            print('\nSEM MAIS PAGINAS\n')
