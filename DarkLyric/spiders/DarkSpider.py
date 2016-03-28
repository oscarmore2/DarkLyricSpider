import re, json
from scrapy.selector import Selector
try:
        from scrapy.spider import Spider
except:
        from scrapy.spider import BaseSpider as Spider
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle

from DarkLyric.items import *
from DarkLyric.misc.log import *

class DarkLyricSpider(CrawlSpider):
        name = "DarkLyric"
        allowed_domains = ["darklyrics.com"]
        chrStart = 97
        i = chrStart
        start_urls = ["http://www.darklyrics.com/a.html"]
        
        
        rules = [Rule(sle(allow=("a.html")), follow=True, callback='parse_item')
                ]
                

        def parse_item(self, response):
            items = []
            sel = Selector(response)
            base_url = get_base_url(response)
            CollumBase = sel.css('div.artists')
            ColumnLeft = CollumBase.css('div.fl').xpath("//a[starts-with(@href, 'a')]")
            
            for site in ColumnLeft:
                item = DarklyricItem()
                #print ("the css elements "+site.css("//a[contains(@href, 'a')]"))
                item['name'] = site.xpath('text()').extract()
                relative_url = site.xpath('@href').extract()[0]
                item['RefLink'] = urljoin_rfc(base_url, relative_url)
                items.append(item)
            
            #print repr(item).decode("unicode-escape") + '\n'

            ColumnRight = sel.css('div.fr').xpath("//a[starts-with(@href, 'a')]")
            for site in ColumnRight:
                item = DarklyricItem()
                item['name'] = site.xpath('text()').extract()
                relative_url = site.xpath('@href').extract()[0]
                item['RefLink'] = urljoin_rfc(base_url, relative_url)
                items.append(item)
            #print repr(item).decode("unicode-escape") + '\n'

            info('parsed '+str(response))
            return items

        def _process_request(self, request):
            info('process '+str(request))
            return request

