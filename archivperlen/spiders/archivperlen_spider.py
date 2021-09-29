import scrapy
from scrapy.item import Item, Field
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter


class Archivperle(Item):
    url = Field()
    title = Field()
    tooltip = Field()
    description = Field()



class ArchivperlenSpider(scrapy.Spider):
    name = "archivperlen"
    base_url = 'https://www.srf.ch'

    def start_requests(self):

        url = 'https://www.srf.ch/play/suche?query=&showAll=true&hideShowSearch=true&shows=urn%3Asrf%3Ashow%3Atv%3Aeb4f3b13-0362-4ea8-b7b3-325382c86ef2'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # item = response.css("ul li:first-of-type article div:first-of-type")
        articles = response.css("article")

        
        filename = f'/home/chriad/Desktop/archivperlen/data.csv'
        with open(filename, 'wb') as f:
            exporter = CsvItemExporter(file=f)
            exporter.start_exporting()
            for article in articles:
                item = article.css("div:first-of-type")
                anchor = item.css("a")[1]

                dl_url = anchor.attrib["href"]
                tooltip = anchor.attrib["aria-label"]
                title = item.css("a:nth-of-type(2)::text").get()  # other way
                description = item.css("div div:first-of-type::text").get()

                metadata = item.css("div div:nth-of-type(2)")
                published = metadata.css("time::text").get()
                duration = metadata.css("span:nth-of-type(2)::text").get()

                # self.log(
                #     f'\n{dl_url}\n{tooltip}\n{title}\n{description}\n{published}\n{duration}')

                perle = Archivperle(title=title, url=dl_url, tooltip=tooltip, description=description)
                exporter.export_item(perle)
            exporter.finish_exporting()
