import scrapy
from scrapy.crawler import CrawlerProcess


class Playbook(scrapy.Spider):
    name = "PostcodesSpider"

    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'Data.csv',
    }


    def start_requests(self):
        yield scrapy.Request(url="https://www.olx.com.pk/livestock_c1960?filter=type_eq_cows",
                             callback=self.parse, dont_filter=True,
                             headers={
                                 'USER-AGENT': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
                             },
                             )

    def parse(self, response):
        dates = response.css("li.EIR5N > a::attr(href)").extract()
        for d in dates:
            yield scrapy.Request("https://www.olx.com.pk" + d,
                                 callback=self.parse2, dont_filter=True,
                                 headers={
                                     'USER-AGENT': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
                                 },
                                 )

    def parse2(self, response):
        name = response.css("div._3oOe9::text").extract_first()

        data = response.text

        i = data.find("+92")

        phone = data[i: i + 13] + " "

        yield {
            "Name": name,
            "Phone": phone,
        }


process = CrawlerProcess()
process.crawl(Playbook)
process.start()
