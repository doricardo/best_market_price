# -*- coding: utf-8 -*-
import scrapy

class MundialSpider(scrapy.Spider):
    name = 'Mundial'
    allowed_domains = ['www.supermercadosmundial.com.br']
    start_urls = ['https://www.supermercadosmundial.com.br/ofertas/']

    def parse(self, response):

        for link in response.css('div.item-filtro'):
            i=1
            while i <= 10:
                yield scrapy.Request(
                    link.css('a::attr(href)').extract_first()  + "?page=" + str(i),
                    callback=self.parse_product
                )

                i+=1
            # next_page = response.css('#bnt-carregar')


    def parse_product(self, response):
        initial = response.css('span.data-oferta ::text').extract_first()[1]
        final = response.css('span.data-oferta ::text').extract_first()[3]
        category = response.url.split('?')[0].split('/')[-1]
        products = response.css('span.link-offers')

        for product in products:
    
            image = product.css('img ::attr(src)').extract_first()
            description = product.css('span.name-product ::text').extract_first()
            price = product.css('span.price-product strong::text').extract_first() + response.css('span.price-product sup::text').extract_first()
            price = price.replace(',','.')

            price = BestMarketPriceItem(market='mundial', initial=initial, final=final, category=category, name=description, price=price)
            yield price
            #yield { 'market' : name, 'initial' : initial, 'final' : final, 'category' : category, 'name' : description, 'price' : price } 
