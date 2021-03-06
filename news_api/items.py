# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsApiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    id = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    description = scrapy.Field()
    articleLink = scrapy.Field()
    publishDate = scrapy.Field()
    content = scrapy.Field()    
    sentiment = scrapy.Field()
    magnitude = scrapy.Field()
    publisher = scrapy.Field()
    title = scrapy.Field()
    tags = scrapy.Field()
    readTime = scrapy.Field()
    utc = scrapy.Field()
    topic = scrapy.Field()
    
    pass