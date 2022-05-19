import scrapy


class WrestlerSpider(scrapy.Spider):
    name = 'wrestler'
    start_urls = ['https://www.cagematch.net/?id=2&view=workers']

    def parse(self, response):
        for wrestler in response.css('tr.TRow1, tr.TRow2'):
            yield{
                'Wrestler': wrestler.css('a::text').get()
            }
        page = response.css('div.NavigationPartPage.NavigationPartBorderRight')
        next_page = page.css('a').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
