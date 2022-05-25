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
        # while pageNumber == 0:
        #     yield response.follow(next_page_link, callback=self.parse)
        #     pageNumber += 100

        #     next_page_link = f'https://www.cagematch.net/en/?id=8&view=promotions&region=Amerika&s={pageNumber}'
        # yield response.follow('https://www.cagematch.net/en/?id=8&view=promotions&region=Amerika&s=0', callback=self.parse2)

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
        print(rows)
        # rows = table.css('tr.TRow1.TRowCard, tr.TRow2.TRowCard')
        for row in rows:
            matchPage = row.css('td.TCol.TColSeparator a::attr(href)').get()
            # print(matchPage)
            yield response.follow(matchPage, callback = self.parse4)

    def parse4(self, response):
        item = WrestlingMatchItem()
        eventInfo = response.css('div.InformationBoxTable')
        for row in eventInfo.css('div.InformationBoxRow'):
            title = row.css(
                'div.InformationBoxTitle::text').get().replace(':', '')
            title2 = title.replace(' ', '')
            title3 = title2.replace('-', '')
            print(title3)
            content = row.css('div.InformationBoxContents a::text, div.InformationBoxContents::text')
            if title3 == 'Nameoftheevent':
                title3 = 'EventName'
                item[title3] = content
                continue
            if title3 == 'TVstation/network':
                title3 = 'TVStation'
                item[title3] = content
                continue
            if title3 == 'Commentaryby':
                title3 = 'Commentators'
                item[title3] = content
                continue
            # else:
            #     item[title3] = content
        yield item


