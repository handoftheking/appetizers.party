import scrapy
from a8s.items import A8SItem


class SkSpider(scrapy.Spider):
    name = "sk"
    allowed_domains = ["smittenkitchen.com"]
    start_urls = [
        'http://smittenkitchen.com/recipes/'
    ]

    def parse(self, response):
        items = response.xpath('//a[@name="Appetizers"]/following::ul[1]/li')
        for sel in items:
            item = A8SItem()
            item['title'] = sel.xpath('a/text()').extract()[0]
            item['link'] = sel.xpath('a/@href').extract()[0]
            print item['link']
            slug = item['link'].split(
                'http://smittenkitchen.com/blog/')[1].replace('/', '-')
            item['slug'] = '%s01-%s' % (slug[:8], slug[8:])

            yield item
