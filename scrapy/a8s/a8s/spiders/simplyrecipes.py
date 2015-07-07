import os

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

    rules = (
        Rule(LinkExtractor(
            allow=(r'http://%s/recipes/course/appetizer/page/.*' % SOURCE,),
        ), follow=True),
        Rule(LinkExtractor(
            allow=(r'http://www.simplyrecipes.com/recipes/.*'),
            deny=(r'http://www.simplyrecipes.com/recipes/type',
                  r'http://www.simplyrecipes.com/recipes/.*/.*/'),
            restrict_xpaths='//ul[@class="entry-list"]'
        ), callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        item = A8SItem()
        item['title'] = response.xpath('//h1/text()').extract()[0]
        item['link'] = response.url
        item['source'] = SOURCE
        date = response.xpath('//time/@content').extract()[0]
        item['slug'] = '%s-%s' % (date,
                                  os.path.basename(response.url.strip('/')))
        item['ingredients'] = response.xpath('string(//li[@class="ingredient"])').extract()
        yield item
