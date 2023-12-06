import scrapy
import logging
from os import environ

class LoginSpider(scrapy.Spider):
    name = "login"
    allowed_domains = ["elearning.uni-bremen.de"]
    start_urls = ["https://elearning.uni-bremen.de/index.php?again=yes"]

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={"loginname": environ["username"], "password": environ["password"]},
            callback=self.after_login,
        )

    def after_login(self, response):
        logging.info("Login erfolgreich")
        
    # def scrape_files(self, response, course_name):
    #     tabs = response.selector.css("#tabs > li > a::attr(href)").extract()
    #     for tab in tabs:
    #         if tab.find("files") >= 0:
    #             yield scrapy.Request(tab, callback=self.scrape_files, cb_kwargs={
    #                 "course_name": course_name,
    #                 "parent_folders": []
    #                 })
