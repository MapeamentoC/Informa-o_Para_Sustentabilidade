import scrapy


class FolhaSpySpider(scrapy.Spider):
    name = 'folha_spy'
    allowed_domains = ['xxx.com']
    start_urls = ['http://xxx.com/']

    def parse(self, response):
        pass
