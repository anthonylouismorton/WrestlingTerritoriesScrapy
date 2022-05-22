import scrapy
from wrestlingterritories.items import WrestlingterritoriesItem


class WrestlerSpider(scrapy.Spider):
    name = 'wrestler'
    start_urls = ['https://www.cagematch.net/?id=2&view=workers']

    def parse(self, response):
        for wrestler in response.css('tr.TRow1, tr.TRow2'):

            URL = wrestler.css('td.TCol.TColSeparator a::attr(href)').get()
            wrestlerURL = f'https://www.cagematch.net/{URL}'
            yield response.follow(wrestlerURL, callback=self.parse2)

        # pageNumber = 100
        # next_page_link = f'https://www.cagematch.net/?id=2&view=workers&s={pageNumber}'
        # while pageNumber < 200:
        #     yield response.follow(next_page_link, callback=self.parse)
        #     pageNumber += 100
        #     next_page_link = f'https://www.cagematch.net/?id=2&view=workers&s={pageNumber}'

    def parse2(self, response):
        item = WrestlingterritoriesItem()
        item['Wrestler'] = response.css('h1.TextHeader::text').get()
        try:
            aka = response.css('h2.TextSubHeader::text').get().replace(
                'Also known as ', '')
            akalist = aka.split(',')
            item['Alteregos'] = akalist
        except:
            item['Alteregos'] = None
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
            if title3 == 'ActiveRoles':
                continue
            if title3 == 'Roles':
                rolesList = []
                for role in content:
                    rolesList.append(role.get())
                item['Roles'] = rolesList
                continue
            if title3 == 'Nicknames':
                nickNameList = []
                for nickName in content:
                    nickNameList.append(nickName.get())
                item[title3] = nickNameList
                continue
            if title3 == 'Signaturemoves':
                moveList = []
                for move in content:
                    moveList.append(move.get())
                item[title3] = moveList
                continue
            if title3 == 'Trainer':
                if row.css('div.InformationBoxContents a::text') is not None:
                    trainers = row.css(
                        'div.InformationBoxContents a::text').getall()
                    item[title3] = trainers
                    continue
                elif content is not None:
                    item[title3] = content
                    continue
                # elif row.css('div.InformationBoxContents') is not None:
                #     item[title3] = row.css('div.InformationBoxContents')
                #     continue
            if content.get() is not None:
                if title3 == 'Alteregos':
                    pass
                else:
                    item[title3] = content.get()
            else:
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
