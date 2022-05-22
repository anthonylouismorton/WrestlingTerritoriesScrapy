import scrapy


class WrestlerSpider(scrapy.Spider):
    name = 'promotion'
    start_urls = [
        'https://www.cagematch.net/en/?id=8&view=promotions&region=Amerika&status=&name=&location=&minRating=&maxRating=&minVotes=&maxVotes=']
    count = 1

    def parse(self, response):
        for promotion in response.css('tr.TRow1, tr.TRow2'):
            URL = promotion.css('td.TCol.TColSeparator a::attr(href)').get()
            yield response.follow(wrestlerURL, callback=self.parse2)

    def parse2(self, response):
        print(count)
        count += 1
