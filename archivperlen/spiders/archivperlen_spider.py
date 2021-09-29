import scrapy
from scrapy.item import Item, Field
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter


class Archivperle(Item):
    vis_desc = Field()
    url = Field()
    vis_desc = Field()
    vis_desc = Field()
    vis_desc = Field()
    vis_desc = Field()
    vis_desc = Field()
    vis_desc = Field()


class ArchivperlenSpider(scrapy.Spider):
    name = "archivperlen"
    base_url = 'https://www.srf.ch'

    def start_requests(self):

        url = 'https://www.srf.ch/play/suche?query=&showAll=true&hideShowSearch=true&shows=urn%3Asrf%3Ashow%3Atv%3Aeb4f3b13-0362-4ea8-b7b3-325382c86ef2'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # page = response.url.split("/")[-2]
        item = response.css("ul li:first-of-type article div:first-of-type")
        anchor = item.css("a")[1]

        dl_url = anchor.attrib["href"]
        description = anchor.attrib["aria-label"]
        title = item.css("a:nth-of-type(2)::text").get()  # other way
        desc_long = item.css("div div:first-of-type::text").get()

        metadata = item.css("div div:nth-of-type(2)")
        published = metadata.css("time::text").get()
        duration = metadata.css("span:nth-of-type(2)::text").get()

        self.log(
            f'\n{dl_url}\n{description}\n{title}\n{desc_long}\n{published}\n{duration}')
        perle = Archivperle(vis_desc=title, url=dl_url)
        filename = f'/home/chriad/Desktop/archivperlen/data.csv'
        with open(filename, 'wb') as f:
            exporter = CsvItemExporter(file=f)
            exporter.start_exporting()
            exporter.export_item(perle)
            exporter.finish_exporting()
