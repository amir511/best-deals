from scrapy.crawler import CrawlerProcess
from best_deals_scrapy.best_deals_scrapy.spiders.spiders import JumiaSpider, SouqSpider


def crawl_spiders():
    process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE; 7.0; Windows NT 5.1)'})
    process.crawl(JumiaSpider)
    process.crawl(SouqSpider)
    process.start()


def main():
    crawl_spiders()


if __name__ == "__main__":
    main()
