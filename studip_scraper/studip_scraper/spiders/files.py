import scrapy
import json
from studip_scraper.items import StudipFiles
from studip_scraper.spiders.courses import CoursesSpider

class FilesSpider(CoursesSpider):
    name = "files"
        
    def after_login(self, _response):
        return scrapy.Request("https://elearning.uni-bremen.de/dispatch.php/my_courses", self.scrape_courses2)

    def scrape_courses2(self, response):
        for course in self.scrape_courses(response):
            yield scrapy.Request(f"https://elearning.uni-bremen.de/dispatch.php/course/overview?cid={course['cid']}",
                                    callback=self.scrape_course, cb_kwargs={"course_name": course["course_name"]})

    def scrape_course(self, response, course_name):
        tabs = response.selector.css("#tabs > li > a::attr(href)").extract()
        for tab in tabs:
            if tab.find("files") >= 0:
                yield scrapy.Request(tab, callback=self.scrape_files, cb_kwargs={
                    "course_name": course_name,
                    "parent_folders": []
                    })
        
    def scrape_files(self, response, course_name, parent_folders):
        files_table = response.selector.css("#files_table_form")
        files_data = json.loads(files_table.css("::attr(data-files)").get())

        file_urls = []
        for file_data in files_data:
            file_urls.append(file_data["download_url"])
                        
        files = StudipFiles(file_urls=file_urls, course=course_name, parent_folders=parent_folders)
        yield files
        
        folders = json.loads(files_table.css("::attr(data-folders)").get())
        for folder in folders:
            yield scrapy.Request(folder["url"], self.scrape_files, cb_kwargs={
                "course_name": course_name,
                "parent_folders": parent_folders + [folder["name"]]
                })
