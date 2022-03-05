import scrapy
from scrapy.crawler import CrawlerProcess
import json

# SETTINGS
process = CrawlerProcess(settings= {
    'FEED_URI': 'items.json',
    'FEED_FORMAT': 'json',
    'FEED_EXPORT_ENCODING': 'utf-8',
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7',
    'ROBOTSTXT_OBEY': False,
    'DOWNLOAD_DELAY': 4,


})

# Spider class
class ProductSpider(scrapy.Spider):
    # name of spider
    name = 'products'

    # link of website to scrape
    def start_requests(self):
        yield scrapy.Request('https://wltest.dns-systems.net/')

    # callback to process downloaded responses
    def parse(self, response):
        # set of div containing all the items I want except the titles of the products
        items = response.css('.package-features')

        # for each item create proper fields
        for item in items:
            yield {
                'optionTitle': item.xpath(
                    'preceding-sibling::div[1]/h3/text()').get(),  # get h3 text from previous sibling
                'description': item.css('.package-name ::text').get() + item.css('.package-description ::text').get(),
                'price': item.css('.price-big ::text').get(),
                'discount': item.css('.package-price p::text').get()
            }

            yield (scrapy.Request(f'https://wltest.dns-systems.net/', callback=self.parse))

# start crawling
process.crawl(ProductSpider)
process.start()