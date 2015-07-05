from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from a8s.items import A8SItem


SOURCE = 'www.simplyrecipes.com'


class SimplyrecipesSpider(CrawlSpider):
    name = "simplyrecipes"
    allowed_domains = [SOURCE]
    start_urls = [
        'http://%s/recipes/course/appetizer/' % SOURCE  # http://ww.simplyrecipes.com/recipes/course/appetizer/
    ]

    rules = (Rule(LinkExtractor(
             allow=(r'http://%s/recipes/course/appetizer/.*' % SOURCE),
             restrict_xpaths=(r'//p[@class="next page-numbers"]', )),
        callback="parse_items", follow= True),
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
