import os
import django
import json
from logzero import logger
from scrapy.crawler import CrawlerProcess
from best_deals_scrapy.best_deals_scrapy.spiders.spiders import JumiaSpider, SouqSpider

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'best_deals_django.settings')
django.setup()
from best_deals_django.base.models import Product

JSON_FILES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'best_deals_scrapy', 'best_deals_scrapy', 'output')


def crawl_spiders():
    process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE; 7.0; Windows NT 5.1)'})
    process.crawl(JumiaSpider)
    process.crawl(SouqSpider)
    process.start()

def read_json_file(file_path):
    with open(file_path,'r') as f:
        file_data = json.loads(f.read())
    
    return file_data

def update_or_create_product(product_dict):
    product_id = product_dict['product_id']
    platform = product_dict['platform']
    product, status = Product.objects.get_or_create(product_id=product_id, platform=platform)
    product.description = product_dict['description']
    product.brand = product_dict['brand']
    product.link = product_dict['link']
    product.old_price = product_dict['old_price']
    product.new_price = product_dict['new_price']
    product.image = product_dict['image']
    product.save()
    message = 'Created product: {}' if status else 'Updated product: {}'
    logger.info(message.format(str(product)))

def crawl_and_update_db():
    logger.info('Started Scrapping data and updating Database')
    crawl_spiders()
    for file in os.listdir(JSON_FILES_DIR):
        file_path = os.path.join(JSON_FILES_DIR, file)
        for d in read_json_file(file_path):
            update_or_create_product(d)
    logger.info('Finished Scrapping data and updating Database')

if __name__ == "__main__":
    crawl_and_update_db()
