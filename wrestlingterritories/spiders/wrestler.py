import scrapy

class WrestlerSpider(scrapy.Spider):
    name = 'wrestler'
    start_urls = ['https://www.cagematch.net/?id=2&view=workers']

    def parse(self, response):
        for wrestler in response.css('tr.TRow1, tr.TRow2'):
            URL = wrestler.css('td.TCol.TColSeparator a::attr(href)').get()
            wrestlerURL = f'https://www.cagematch.net/{URL}'
            yield response.follow(wrestlerURL, callback=self.parse2)
        pageNumber = 100
        next_page_link = f'https://www.cagematch.net/?id=2&view=workers&s={pageNumber}'
        while pageNumber < 200:
            yield response.follow(next_page_link, callback=self.parse)
            pageNumber +=100
            next_page_link = f'https://www.cagematch.net/?id=2&view=workers&s={pageNumber}'
    def parse2(self, response):
        for row in response.css('div.InformationBoxRow'):
            title = row.css('div.InformationBoxTitle::text').get()
            content = row.css('div.InformationBoxContents::text')

            if content.get() is not None:
                yield{
                    f'{title}': content.get()
                }
            else:
                yield{
                    f'{title}': row.css('div.InformationBoxContents a::text').get()
                }
            # wrestlerLink = wrestlerURL.css('a').attrib['href']
            # yield{
            #     'Wrestler': wrestler.css('a::text').get()
            # }