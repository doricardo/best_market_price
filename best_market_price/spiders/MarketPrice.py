# -*- coding: utf-8 -*-
import scrapy


class MarketpriceSpider(scrapy.Spider):
    name = 'MarketPrice'
    allowed_domains = ['www.supermercadosmundial.com.br']
    start_urls = ['https://www.supermercadosmundial.com.br/ofertas/']

    def parse(self, response):

        links = response.css('div.item-filtro a::attr(href)').getall()

        for link in links:
            i=1
            while i <= 10:
                yield scrapy.Request(
                    link  + "?page=" + str(i),
                    callback=self.parse_product
                )

                i+=1
            # next_page = response.css('#bnt-carregar')


    def parse_product(self, response):

        category = response.url.split('?')[0].split('/')[-1]
        products = response.css('span.link-offers')

        for product in products:
    
            #image = product.css('img ::attr(src)').get()
            name = product.css('span.name-product ::text').get()
            price = product.css('span.price-product strong::text').get() + response.css('span.price-product sup::text').get()
            price = price.replace(',','.')
            yield { 'category' : category, 
                    'name' : name,
                    'price' : price } 