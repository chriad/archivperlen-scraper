import scrapy


class ArchivperlenSpider(scrapy.Spider):
    name = "archivperlen"
    base_url = 'https://www.srf.ch'

    def start_requests(self):
        urls = [
            'https://www.srf.ch/play/suche?query=&showAll=true&hideShowSearch=true&shows=urn%3Asrf%3Ashow%3Atv%3Aeb4f3b13-0362-4ea8-b7b3-325382c86ef2'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # page = response.url.split("/")[-2]
        item = response.css("ul li:first-of-type article div:first-of-type")
        anchor = item.css("a")[1]
        dl_url = anchor.attrib["href"]
        context_desc = anchor.attrib["aria-label"]
        vis_desc = item.css("a:nth-of-type(2)::text").get() # other way
        desc_long = item.css("div div:first-of-type::text").get()
        metadata = item.css("div div:nth-of-type(2)")
        datep = metadata.css("time::text").get()
        duration = metadata.css("span:nth-of-type(2)::text").get()
        # filename = f'quotes-{page}.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        self.log(f'Saved file {dl_url}')
