# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HpdItem(scrapy.Item):
    street_name = scrapy.Field()
    borough = scrapy.Field()
    house_number = scrapy.Field()
    
    hpd_no = scrapy.Field()
    range_ = scrapy.Field()
    block = scrapy.Field()
    lot = scrapy.Field()
    cd = scrapy.Field()
    census_tract = scrapy.Field()
    stories = scrapy.Field()
    a_units = scrapy.Field()
    b_units = scrapy.Field()
    ownership = scrapy.Field()
    registration_no = scrapy.Field()
    class_ = scrapy.Field()
    source_url = scrapy.Field()

