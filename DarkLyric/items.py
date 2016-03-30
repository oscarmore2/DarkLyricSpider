# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class DarklyricItem (Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    artistName = Field()
    RefLink = Field()
    albums = Field()

class AlbumItem (Item) :
    albumName = Field()
    RefLink = Field()
    songs = Field()

class SongItem (Item) :
    songName = Field()
    lyric = Field()


