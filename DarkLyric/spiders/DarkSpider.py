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
from scrapy.http import Request
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
            download_delay = 0.5
            CollumBase = sel.css('div.artists')
            ColumnLeft = CollumBase.css('div.fl').xpath("//a[starts-with(@href, 'a/aa')]")

            """
            item = DarklyricItem()
            relative_url = ColumnLeft[1].xpath('@href').extract()
            relative_url = urljoin_rfc(base_url, relative_url)
            request = Request (relative_url, callback=self.parse_artist)
            yield request
            item['artistName'] = ColumnLeft[0].xpath('text()').extract()[0]
            item['RefLink'] = relative_url
            item['ablums'] = request
            items.append(item)
            info('parsed '+str(response))
            yield  items
            """
            
            
            print (ColumnLeft)
            
            for site in ColumnLeft:
                item = DarklyricItem()
                #print ("the css elements "+site.css("//a[contains(@href, 'a')]"))
                item['artistName'] = site.xpath('text()').extract()
                relative_url = site.xpath('@href').extract()[0]
                relative_url = urljoin_rfc(base_url, relative_url)
                item['RefLink'] = relative_url
                request = Request (relative_url, callback=self.parse_album)
                
                item['albums'] = request
                items.append(item)
                

            info('parsed '+str(response))
            return items
            
            #print repr(item).decode("unicode-escape") + '\n'
            
            
 #           ColumnRight = sel.css('div.fr').xpath("//a[starts-with(@href, 'a')]")
            """
            for site in ColumnRight:
                item = DarklyricItem()
                item['name'] = site.xpath('text()').extract()[0  ]
                relative_url = site.xpath('@href').extract()[0]
                item['RefLink'] = urljoin_rfc(base_url, relative_url)
                items.append(item)
            #print repr(item).decode("unicode-escape") + '\n'
            """
            
        
        def parse_album(self, response):
            items = []
            mainContent = Selector (response)
            base = get_base_url(response)
            albumContent = mainContent.xpath("//div[@id='album']").extract
            
            for album in albumContent :
                item = AlbumItem()
                item['albumName'] = album.css('h2').css('strong').xpath('text()').extract[0]
                rel_url = album.xpath("//a[starts-with(@href, '..\/lyrics')]")[0]
                rel_url = urljoin_rfc(base, rel_url)
                #request = Request(rel_url, callback = self.parse_song)
                #yield request
                item['RefLink'] = rel_url
                item['songs'] = 'test'
                items.append(item)
            
            info('parsed album '+str(response))
            return items
        
        def parse_song (self, response) :
            items = []
            mainContent = Selector(response)
            songsItem = mainContent.css('lyric').extrect()
            
            item = SongItem()
            
            info('parsed song '+str(response))
            return items
        


        def _process_request(self, request):
            info('process '+str(request))
            return request

