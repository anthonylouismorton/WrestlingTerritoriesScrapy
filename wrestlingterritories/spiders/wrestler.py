import scrapy

class WrestlerSpider(scrapy.Spider):
    name = 'wrestler'
    start_urls = ['https://www.cagematch.net/?id=2&view=workers']

    def parse(self, response):
        for wrestler in response.css('tr.TRow1, tr.TRow2'):
            yield{
                'Wrestler': wrestler.css('a::text').get()
            }
            wrestlerURL = response.css('td.TCol.TColSeparator')
            wrestlerLink = wrestlerURL.css('a').attrib['href']
            yield response.follow(wrestlerLink)
            
        # page = response.css('div.NavigationPartPage.NavigationPartBorderRight')
        # next_page = page.css('a').attrib['href']
        pageNumber = 100
        next_page_link = f'https://www.cagematch.net/?id=2&view=workers&s={pageNumber}'
        # for item in range(253):
        #     pageNumber = pageNumber + 100
        #     print(pageNumber)
        #     yield response.follow(next_page_link, callback=self.parse)
        while pageNumber < 25400:
            yield response.follow(next_page_link, callback=self.parse)
            pageNumber +=100
            next_page_link = f'https://www.cagematch.net/?id=2&view=workers&s={pageNumber}'