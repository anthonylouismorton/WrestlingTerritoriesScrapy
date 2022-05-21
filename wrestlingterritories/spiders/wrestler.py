import scrapy
from wrestlingterritories.items import WrestlingterritoriesItem


class WrestlerSpider(scrapy.Spider):
    name = 'wrestler'
    start_urls = ['https://www.cagematch.net/?id=2&view=workers']

    def parse(self, response):
        for wrestler in response.css('tr.TRow1, tr.TRow2'):
            URL = wrestler.css('td.TCol.TColSeparator a::attr(href)').get()
            wrestlerURL = f'https://www.cagematch.net/{URL}'
            # item['WrestlerName'] = wrestler.css('a::text').get()
            # yield item
            yield response.follow(wrestlerURL, callback=self.parse2)

        pageNumber = 100
        next_page_link = f'https://www.cagematch.net/?id=2&view=workers&s={pageNumber}'
        while pageNumber < 200:
            yield response.follow(next_page_link, callback=self.parse)
            pageNumber += 100
            next_page_link = f'https://www.cagematch.net/?id=2&view=workers&s={pageNumber}'

    def parse2(self, response):
        item = WrestlingterritoriesItem()
        item['Wrestler'] = response.css('h1.TextHeader::text').get()
        aka = response.css('h2.TextSubHeader::text').get().replace(
            'Also known as ', '')
        akalist = aka.split(',')
        item['Alteregos'] = akalist
        for row in response.css('div.InformationBoxRow'):
            title = row.css(
                'div.InformationBoxTitle::text').get().replace(':', '')
            title2 = title.replace(' ', '')
            title3 = title2.replace('-', '')
            content = row.css('div.InformationBoxContents::text')
            if title3 == 'WWW':
                title3 = 'SocialMedia'
                accountList = []
                for account in response.css('ul.noList li'):
                    accountList.append(account.css('li a').attrib['href'])
                item[title3] = accountList
            if content.get() is not None:
                if title3 == 'Alteregos':
                    pass
                else:
                    item[title3] = content.get()
            else:
                # if title3 == 'WWW':
                #     title3 = 'SocialMedia'
                #     accountList = []
                #     for account in response.css('ul.noList li'):
                #         accountList.append(account.css('li a').attrib['href'])
                #     item[title3] = accountList
                # else:
                item[title3] = row.css(
                    'div.InformationBoxContents a::text').get()
        yield item
        # if content.get() is not None:
        #     yield{
        #         f'{title}': content.get()
        #     }
        # else:
        #     yield{
        #         f'{title}': row.css('div.InformationBoxContents a::text').get()
        #     }
        # wrestlerLink = wrestlerURL.css('a').attrib['href']
        # yield{
        #     'Wrestler': wrestler.css('a::text').get()
        # }
