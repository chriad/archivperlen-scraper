import scrapy


class ArchivperlenSpider(scrapy.Spider):
    name = "archivperlen"

    def start_requests(self):
        urls = [
            'https://www.srf.ch/play/suche?query=&showAll=true&hideShowSearch=true&shows=urn%3Asrf%3Ashow%3Atv%3Aeb4f3b13-0362-4ea8-b7b3-325382c86ef2'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # page = response.url.split("/")[-2]
        href = response.css("ul li:first-of-type article div:first-of-type a:first-of-type").attrib["href"]
        # filename = f'quotes-{page}.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        self.log(f'Saved file {href}')
