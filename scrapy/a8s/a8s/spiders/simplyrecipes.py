import scrapy
from a8s.items import A8SItem


SOURCE = 'www.simplyrecipes.com'


class SimplyrecipesSpider(scrapy.Spider):
    name = "simplyrecipes"
    allowed_domains = [SOURCE]
    start_urls = [
        'http://%s/recipes/course/appetizer/' % SOURCE
    ]

    rules = (Rule (LinkExtractor(
             allow=('http://%s/recipes/course/appetizer/page/3/' % SOURCE),
             restrict_xpaths=('//p[@class="next page-numbers"]',))
        , callback="parse_items", follow= True),
    )

    def parse(self, response):
        items = response.xpath('//a[@name="Appetizers"]/following::ul[1]/li')
        for sel in items:
            item = A8SItem()
            item['title'] = sel.xpath('a/text()').extract()[0]
            item['link'] = sel.xpath('a/@href').extract()[0]
            print item['link']
            slug = item['link'].split(
                'http://%s/blog/' % SOURCE)[1].replace('/', '-').strip('-')
            item['slug'] = '%s01-%s' % (slug[:8], slug[8:])
            item['source'] = SOURCE
            yield item
