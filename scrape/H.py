#//*[@id="notation_5501"]/div[24]


"""
from lxml import html
import requests


page = requests.get('http://www.chess.com/livechess/game?id=1090265781')
tree = html.fromstring(page.text)

buyers = tree.xpath('//*[@id="notation"]')


texts = [o.text for o in buyers]
print texts
print buyers
"""
"""
from scrapy import Spider
from scrapy.selector import Selector


class StackSpider(Spider):
    name = "stack"
    allowed_domains = ["chess.com"]
    start_urls = [
        "http://www.chess.com/livechess/game?id=1090265781",
    ]

    def parse(self, response):
	print "parsing"
        questions = Selector(response).xpath('//*[@id="notation"]')
	print questions
"""

import scrapy

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2]
        with open(filename, 'wb') as f:
            f.write(response.body)