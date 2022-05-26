from cgitb import text
from imaplib import IMAP4_stream
import scrapy
from wrestlingterritories.items import WrestlingMatchItem


class MatchSpider(scrapy.Spider):
    name = 'match'
    start_urls = [
        'https://www.cagematch.net/en/?id=8&view=promotions&region=Amerika&status=&name=&location=&minRating=&maxRating=&minVotes=&maxVotes=']

    def parse(self, response):
        # commented out lines 14 - 23 for testing purposes
        # for promotion in response.css('tr.TRow1, tr.TRow2'):
        #     URL = promotion.css('td.TCol.TColSeparator a::attr(href)').get()
        #     yield response.follow(URL, callback=self.parse2)
        #     pageNumber = 0
        #     next_page_link = f'https://www.cagematch.net/en/?id=8&view=promotions&region=Amerika&s={pageNumber}'
        # while pageNumber == 0:
        #     yield response.follow(next_page_link, callback=self.parse)
        #     pageNumber += 100

        #     next_page_link = f'https://www.cagematch.net/en/?id=8&view=promotions&region=Amerika&s={pageNumber}'
        yield response.follow('https://www.cagematch.net/en/?id=8&nr=1', callback=self.parse2)

    def parse2(self, response):
        # promotionName = response.css('h1.TextHeader::text').get().split(' (')
        # item['Promotion'] = promotionName[0]
        header = response.css('ul.ContentNavigator')
        eventsPage = ''
        for li in header.css('li'):
            if li.css('a::text').get() == 'Events':
                eventsPage = li.css('a::attr(href)').get()
        yield response.follow(eventsPage, callback=self.parse3)

    def parse3(self, response):
        table = response.css('table.TBase.TableBorderColor')
        rows = table.css('tr')
        rows = table.css('tr.TRow1, tr.TRow2')
        for row in rows:
            matchPage = row.css('td.TCol.TColSeparator a::attr(href)').getall()
            yield response.follow(matchPage[1], callback = self.parse4)

    def parse4(self, response):
        header = response.css('h1.TextHeader::text').get()
        print(header)
        item = WrestlingMatchItem()
        eventInfo = response.css('div.InformationBoxTable')
        matchInfo = response.css('div.Matches')
        for row in eventInfo.css('div.InformationBoxRow'):
            title = row.css(
                'div.InformationBoxTitle::text').get().replace(':', '')
            title2 = title.replace(' ', '')
            title3 = title2.replace('-', '')
            content = row.css('div.InformationBoxContents a::text, div.InformationBoxContents::text')
            if title3 == 'Nameoftheevent':
                title3 = 'EventName'
                print(title3)
                item[title3] = content.get()
                continue
            if title3 == 'TVstation/network':
                title3 = 'TVStation'
                item[title3] = content.get()
                continue
            if title3 == 'Commentaryby':
                title3 = 'Commentators'
                item[title3] = content.get()
                continue
            if content.get() is not None:
                item[title3] = content.get()
        for match in matchInfo:
            

        yield item


