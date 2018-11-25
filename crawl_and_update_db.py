import os
import django
import json
from logzero import logger
from scrapy.crawler import CrawlerProcess
from best_deals_scrapy.best_deals_scrapy.spiders.spiders import JumiaSpider, SouqSpider

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'best_deals_django.settings')
django.setup()
from best_deals_django.base.models import Product

JSON_FILES_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'best_deals_scrapy', 'best_deals_scrapy', 'output'
)


def _list_json_files():
    files = os.listdir(JSON_FILES_DIR)
    files.remove('empty_file.txt')
    return files


def remove_old_files():
    logger.info('Removing old json files')
    files = _list_json_files()
    os.chdir(JSON_FILES_DIR)
    for file in files:
        try:
            os.remove(file)
        except FileNotFoundError:
            logger.error("Couldn't remove {}, it might be already removed".format(file))
    logger.info('Finished Removing old files')


def crawl_spiders():
    logger.info('Started the scraping process')
    process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE; 7.0; Windows NT 5.1)'})
    process.crawl(JumiaSpider)
    process.crawl(SouqSpider)
    process.start()
    logger.info('Finished Scraping data')


def delete_old_products():
    """
    This is necessary to prevent obselete data in db.
    Jumia updates its offers almost every couple of hours.
    """
    logger.info('Removing old products from db')
    Product.objects.all().delete()
    logger.info('db is now empty!')


def _read_json_file(file_path):
    with open(file_path, 'r') as f:
        file_data = json.loads(f.read())

    return file_data


def _create_product(product_dict):
    try:
        product = Product(**product_dict)
        product.save()
        logger.info('Created product: {}'.format(str(product)))
    except Exception as e:
        logger.error("Couldn't create product, because of: {}".format(e))


def create_products_from_files():
    logger.info('Started creating products from json files')
    files = _list_json_files()
    for file in files:
        file_path = os.path.join(JSON_FILES_DIR, file)
        for d in _read_json_file(file_path):
            _create_product(d)
    logger.info('Finished creating new products')


if __name__ == "__main__":
    logger.info('Started Scrapping data and updating Database')
    remove_old_files()
    crawl_spiders()
    delete_old_products()
    create_products_from_files()
    logger.info('Finished Scrapping data and updating Database')
