from cgitb import text
from imaplib import IMAP4_stream
import scrapy
from wrestlingterritories.items import WrestlingMatchItem


class MatchSpider(scrapy.Spider):
    name = 'match'
    start_urls = [
        'https://www.cagematch.net/en/?id=8&view=promotions&region=Amerika&status=&name=&location=&minRating=&maxRating=&minVotes=&maxVotes=']

    def parse(self, response):
        for promotion in response.css('tr.TRow1, tr.TRow2'):
            URL = promotion.css('td.TCol.TColSeparator a::attr(href)').get()
            yield response.follow(URL, callback=self.parse2)
            pageNumber = 0
            next_page_link = f'https://www.cagematch.net/en/?id=8&view=promotions&region=Amerika&s={pageNumber}'
            while pageNumber == 0:
                yield response.follow(next_page_link, callback=self.parse)
                pageNumber += 100

                next_page_link = f'https://www.cagematch.net/en/?id=8&view=promotions&region=Amerika&s={pageNumber}'

    def parse2(self, response):
        item = WrestlingMatchItem()
        promotionName = response.css('h1.TextHeader::text').get().split(' (')
        item['Promotion'] = promotionName[0]
        header = response.css('ul.ContentNavigator')
        eventsPage = ''
        for li in header.css('li'):

            if li.css('a::text').get() == 'Events':
                print('we in here boys')
                eventsPage = li.css('a::attr(href)').get()
        yield response.follow(eventsPage)
        # print(eventsPage)

    def parse3(self, response):
