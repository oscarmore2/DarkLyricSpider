import re, json
from scrapy.selector import Selector
try:
        from scrapy.spider import Spider
except:
        from scrapy.spider import BaseSpider as Spider
        from scrapy.utils.response import get_base_url
        from scrapy.utils.url import urljoin_rfc
        from scrapy.contrib.spiders import CrawSpider, Rule
        from scrapy.contrib.linkextractors.sgm1 import SgmlLinkExtractor as sle

        from DarkLyric.items import *
        from DarkLyric.misc.log import *

class DarkLyricSpider(CrawlSpider):
        name = "Dark Lyric"
        start_urls = ["darklyric.com/"+char(95)+".html"]
        SubUrl = ""
        maxpage = 40
        chrStart = 97
        i = charStart
        start_urls = ["http://www.darklyrics.com"]
        rules = [Rule(
                sle(allow=(allow=(char(i)+".html")), follow=True, callback='parse_item'))
                )]

        def parse_item(self, response):
        items = []
        sel = Selector(response)
        base_url = get_base_url(response)
        CollumBase = sel.css('div.artists')
        ColumnLeft = CollumBase.css('div.fl')
        for site in ColumnLeft:
            item = DarkLyricItem()
            item['name'] = site.css('//a[contains(@href, "image")]').xpath('text()').extract()[0]
            relative_url = site.css('//a[contains(@href, "image")]').xpath('@href').extract()[0]
            items.append(item)
            print repr(item).decode("unicode-escape") + '\n'

        ColumnRight = sel.css('div.fr')
        for site in ColumnRight:
            item = DarkLyricItem()
            item['name'] = site.css('//a[contains(@href, "image")]').xpath('text()').extract()[0]
            relative_url = site.css('//a[contains(@href, "image")]').xpath('@href').extract()[0]
            items.append(item)
            print repr(item).decode("unicode-escape") + '\n'

        info('parsed '+str(response))
        return items

        def _process_request(self, request):
                info('process '+str(request))
                return request

