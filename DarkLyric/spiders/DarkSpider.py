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
import re

class DarkLyricSpider(CrawlSpider):
        name = "DarkLyric"
        allowed_domains = ["darklyrics.com"]
        start_urls = ["http://www.darklyrics.com"]
        
        
        rules = [Rule(sle(allow=(".*\.html")), follow=True, callback='parse_item')
                ]
                

        def parse_item(self, response):
            """
            items = []
            sel = Selector(response)
            base_url = get_base_url(response)
            download_delay = 0.5
            CollumBase = sel.css('div.artists')
            ColumnLeft = CollumBase.css('div.fl').xpath("//a[starts-with(@href, 'a/aa')]")

            
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
            
            
            
            print (ColumnLeft)
            
            for site in ColumnLeft:
                item = DarklyricItem()
                #print ("the css elements "+site.css("//a[contains(@href, 'a')]"))
                item['artistName'] = site.xpath('text()').extract()
                relative_url = site.xpath('@href').extract()[0]
                relative_url = urljoin_rfc(base_url, relative_url)
                item['RefLink'] = relative_url
                items = Request (relative_url, callback=self.parse_album)
                
                item['albums'] = request
                items.append(item)
                

            info('parsed '+str(response))
            return items
            
            #print repr(item).decode("unicode-escape") + '\n'
            
            
 #           ColumnRight = sel.css('div.fr').xpath("//a[starts-with(@href, 'a')]")
            
            for site in ColumnRight:
                item = DarklyricItem()
                item['name'] = site.xpath('text()').extract()[0  ]
                relative_url = site.xpath('@href').extract()[0]
                item['RefLink'] = urljoin_rfc(base_url, relative_url)
                items.append(item)
            #print repr(item).decode("unicode-escape") + '\n'
            """

            base_url = get_base_url(response)
            sel = Selector(response)
            matchObjAblum = re.search(r'http\:\/\/www.darklyrics.com\/.\/\.html', base_url, re.M|re.I)
            matchObjSong = re.search(r'http\:\/\/www.darklyrics.com\/.\/.*\.html', base_url, re.M|re.I)
            
            if matchObjAblum:
                CollumBase = sel.css('div.artists')
                ColumnLeft = CollumBase.css('div.fl').xpath("//a[starts-with(@href, '.\/')]")
                for site in ColumnLeft:
                        relative_url = site.xpath('@href').extract()[0]
                        relative_url = urljoin_rfc(base_url, relative_url)
                        print ("@ Artist "+relative_url)
                        request = Request (relative_url, callback=self.parse_item)
                        yield request

                
                ColumnRight = sel.css('div.fr').xpath("//a[starts-with(@href, '.\/')]")                       
                for site in ColumnRight:
                        relative_url = site.xpath('@href').extract()[0]
                        relative_url = urljoin_rfc(base_url, relative_url)
                        print ("@ Artist "+relative_url)
                        request = Request (relative_url, callback=self.parse_item)
                        yield request

            elif matchObjSong:
                
                album = sel.xpath("//div[@id='album']")
                """
                album = urljoin_rfc(base_url, album)
                print ("@ album "+album)
                request = Request (album, callback=self.parse_song)
                yield request
                
                """
                for al in album:
                        relative_url = al.xpath("//a[/a[starts-with(@href, '\.\.\/lyric'')]").xpath('@href').extract()[0]
                        relative_url = urljoin_rfc(base_url, relative_url)
                        print ("@ album "+relative_url)
                        request = Request (relative_url, callback=self.parse_song)
                        yield request
                

            elif base_url == 'http://www.darklyrics.com' :
                listShow = sel.xpath("//div[@class='listrow']/a[starts-with(@href, '.\.html')]")
                """
                listShow = urljoin_rfc(base_url, listShow)
                print ("at root "+listShow)
                request = Request (listShow, callback=self.parse_item)
                yield request
                """
                for Litem in listShow:
                        print (listShow)
                        relative_url = Litem.xpath('@href').extract()[0]
                        relative_url = urljoin_rfc(base_url, relative_url)
                        print ("@ root "+relative_url)
                        request = Request (relative_url, callback=self.parse_item)
                        yield request
                
             
                
        
        def parse_song (self, response) :
            items = []
            mainContent = Selector(response)
            base = get_base_url(response)
            searchObj = re.search( r'.*\/\/.*\/lyrics\/(.*)\/(.*)\.html.*', base, re.M|re.I)
            artist = searchObj.group(1)
            album = searchObj.group(2)
            songsItem = mainContent.css('lyric').xpath("//h3")
            for si in songsItem:
                item = DarklyricItem()
                item['artistName'] = artist
                item['albumName'] = album
                item['songName'] = si.xpath("//a").xpath('@text').extract()
                #add as title for now
                item['lyricContent'] = si.xpath("//a").xpath('@text').extract()
                items.append(item)
                print ("handled item "+item['songName'])
                
            
            info('parsed song '+str(response))
            return items
        


        def _process_request(self, request):
            info('process '+str(request))
            return request

