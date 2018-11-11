# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FindJobItem(scrapy.Item):
	unique_id = scrapy.Field()
	position_name = scrapy.Field()
	work_year = scrapy.Field()
	salary = scrapy.Field()
	company_name = scrapy.Field()
	city = scrapy.Field()
	create_time = scrapy.Field()


