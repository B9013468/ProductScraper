import scrapy
from scrapy.crawler import CrawlerProcess
import json
import re
from operator import itemgetter

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

# sort json file
class SortJson():

    # Open JSON file to read
    input_file = open('items.json', "r", encoding='utf8')
    json_array = json.load(input_file)


    # for each item in json array convert prices from strings to floats (if subscription is monthly, multiply by 12 to get the annual price)

    for item in json_array:
        if(item.get("optionTitle").split()[-1] == "Months"):
            newPrice = re.findall("\d+\.\d+",item.get("price"))
            item["price"] = float(newPrice[0])*12
        else:
            newPrice = re.findall("\d+\.\d+", item.get("price"))
            item["price"] = float(newPrice[0])


    # sort array by annual price
    json_array = sorted(json_array, key=itemgetter('price'), reverse=True)

    # convert prices from float back to string (divide by 12 to get the original prices for monthly subs and round up to 2 decimals)
    for item in json_array:
        if(item.get("optionTitle").split()[-1] == "Months"):
            item["price"] = "£" + str("%.2f" % round(item.get("price")/12, 2))
        else:
            item["price"] = "£" + str(item.get("price"))

    # print new json in terminal
    for item in json_array:
        print(item)

    #close json file and reopen it to write
    input_file.close()
    input_file = open('items.json', "w", encoding='utf8')
    # dump new json array and close json file
    json.dump(json_array, input_file, indent=4, separators=(',', ': '), ensure_ascii=False)
    input_file.close()