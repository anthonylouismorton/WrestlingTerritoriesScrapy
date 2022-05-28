from cgitb import text
from imaplib import IMAP4_stream
import scrapy
from wrestlingterritories.items import WrestlingEventItem
from wrestlingterritories.items import WrestlingMatchItem

class MatchSpider(scrapy.Spider):
    name = 'match'
    start_urls = [
        'https://www.cagematch.net/en/?id=8&view=promotions&region=Amerika&status=&name=&location=&minRating=&maxRating=&minVotes=&maxVotes=']

    def parse(self, response):
        # commented out lines 14 - 23 for testing purposes
        for promotion in response.css('tr.TRow1, tr.TRow2'):
            URL = promotion.css('td.TCol.TColSeparator a::attr(href)').get()
            yield response.follow(URL, callback=self.parse2)
        pageNumber = 0
        next_page_link = f'https://www.cagematch.net/en/?id=8&view=promotions&region=Amerika&s={pageNumber}'
        while pageNumber < 2400:
            yield response.follow(next_page_link, callback=self.parse)
            pageNumber += 100

            next_page_link = f'https://www.cagematch.net/en/?id=8&view=promotions&region=Amerika&s={pageNumber}'
        # yield response.follow('https://www.cagematch.net/en/?id=8&nr=1', callback=self.parse2)

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
        promoID = response.css('div.TextHeaderLogo a::text').get()
        for row in rows:
            matchPage = row.css('td.TCol.TColSeparator a::attr(href)').getall()
            # print(f'this is the match page {matchPage[1]}')
            # if matchPage[1] is None:
            #     continue
            yield response.follow(matchPage[1], callback = self.parse4)
        eventPage = 100
        next_page_link = f'https://www.cagematch.net/en/{promoID}&page=4&s={eventPage}'
        while eventPage < 24000:
            yield response.follow(next_page_link, callback=self.parse3)
            eventPage += 100
            next_page_link = f'https://www.cagematch.net/en/?id=8&nr=1&page=4&s={eventPage}'

    def parse4(self, response):
        item = WrestlingEventItem()
        eventInfo = response.css('div.InformationBoxTable')
        matchInfo = response.css('div.Matches')
        itemList = ['Promotion','EventName','Date','Type','Location','Arena','Broadcasttype','Broadcastdate','TVStation','Commentators','Attendance','Theme','Wrestlers','OfficialVideo','Officialvideo','Currentname','Currentabbreviation','Status','ActiveTime','WWW','Names','Abbreviations','Owners']
        for row in eventInfo.css('div.InformationBoxRow'):
            title = row.css(
                'div.InformationBoxTitle::text').get().replace(':', '')
            title2 = title.replace(' ', '')
            title3 = title2.replace('-', '')
            content = row.css('div.InformationBoxContents a::text, div.InformationBoxContents::text')
            if title3 == 'Nameoftheevent':
                title3 = 'EventName'
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
            if title3 == 'Date':
                eventDate = content.get()
            if title3 not in itemList:
                continue
            if content.get() is not None:
                item[title3] = content.get()
        allWrestlers = response.css('div.Comments.Font9 a::text, div.Comments.Font9::text').getall()
        newAllWrestlers = []
        for wrestler in allWrestlers:
            if wrestler == ', ':
                continue
            newAllWrestlers.append(wrestler)
        if len(newAllWrestlers) > 0:
            item['Wrestlers'] = newAllWrestlers
        yield item


