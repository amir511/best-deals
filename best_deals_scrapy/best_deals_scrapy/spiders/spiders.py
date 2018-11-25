import scrapy
import json
import os
import re
from logzero import logger

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class JumiaSpider(scrapy.Spider):
    name = "jumia"
    start_urls = ['https://www.jumia.com.eg/deal-of-the-day/?page=1']
    filename = os.path.join(PROJECT_DIR, 'output', 'jumia-{}.json')

    def parse(self, response):
        products = response.css('.-campaign').css('.sku.-gallery')
        products_list = []
        for product in products:
            old_price = product.css('.price-container').css('.price.-old span::attr(data-price)').extract_first()
            if old_price:
                try:
                    d = {
                        'product_id': product.css('::attr(data-sku)').extract_first(),
                        'description': product.css('::attr(data-name)').extract_first(),
                        'brand': product.css('::attr(data-brand)').extract_first(),
                        'link': product.css('a.link::attr(href)').extract_first(),
                        'old_price': float(old_price.replace(',', '')),
                        'new_price': float(
                            product.css('.price-container')
                            .css('.price span::attr(data-price)')
                            .extract_first()
                            .replace(',', '')
                        ),
                        'image': product.css('.image-wrapper.default-state img::attr(data-src)').extract_first(),
                        'platform': 'Jumia',
                    }
                    products_list.append(d)
                except Exception as e:
                    logger.error("Couldn't parse product data, the following error has occured:" + str(e))

        page_number = response.url.split('=')[-1]
        with open(self.filename.format(page_number), 'w') as f:
            f.write(json.dumps(products_list))

        next_page_url = response.css('a[title=Next]::attr(href)').extract_first()
        if next_page_url:
            yield response.follow(next_page_url, self.parse)


class SouqSpider(scrapy.Spider):
    name = "souq"
    start_urls = [
        'https://deals.souq.com/eg-en/search?campaign_id=10114&page=1&sort=best',
        'https://deals.souq.com/eg-en/search?campaign_id=10187&page=1&sort=best',
    ]
    filename = os.path.join(PROJECT_DIR, 'output', 'souq-{}-{}.json')

    def parse(self, response):
        products = json.loads(response.body_as_unicode())['data']
        products_list = []
        for product in products:
            if product['price_saving'] != False:
                try:
                    d = {
                        'product_id': str(product['item_id']),
                        'description': product['title'],
                        'brand': product['manufacturer_en'],
                        'link': product['item_url'],
                        'old_price': float(product['market_price']['price'].replace(',', '')),
                        'new_price': float(product['price']['price'].replace(',', '')),
                        'image': product['image_url'],
                        'platform': 'Souq',
                    }
                    products_list.append(d)
                except Exception as e:
                    logger.error("Couldn't parse product data, the following error has occured:" + str(e))

        page_number = int(re.search(r'page=[0-9]+', response.url).group().replace('page=', ''))
        campaign_id = re.search(r'campaign_id=[0-9]+', response.url).group().replace('campaign_id=', '')

        with open(self.filename.format(campaign_id, page_number), 'w') as f:
            f.write(json.dumps(products_list))

        total_pages = json.loads(response.body_as_unicode())['metadata']['total_pages']
        if page_number != total_pages:
            next_page_number = page_number + 1
            next_page_url = 'https://deals.souq.com/eg-en/search?campaign_id={}&page={}&sort=best'.format(
                campaign_id, next_page_number
            )
            yield response.follow(next_page_url, self.parse)

