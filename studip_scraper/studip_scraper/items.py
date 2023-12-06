# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class StudipFiles(scrapy.Item):
    file_urls = scrapy.Field()
    parent_folders = scrapy.Field()
    course = scrapy.Field()

class StudipCourse(scrapy.Item):
    cid = scrapy.Field()
    course_name = scrapy.Field()
    # TODO: Semester switching support
    # semester = scrapy.Field()
