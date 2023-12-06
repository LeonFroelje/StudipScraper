from studip_scraper.spiders.login import LoginSpider
import scrapy
import re
import json
from studip_scraper.items import StudipCourse

class CoursesSpider(LoginSpider):
    name = "courses"

    def after_login(self, response):
        return scrapy.Request("https://elearning.uni-bremen.de/dispatch.php/my_courses", self.scrape_courses)

    def scrape_courses(self, response):
        # StudIP dynamically generates the courses in the browser with a javascript script. The course
        # ids are stored in the script in a javascript object which can be extracted as json.
        # The extracted course ids can then be used to scrape each of the courses themselves for files,
        # information etc.
        text_scripts = response.selector.xpath("/html/head/script[@type=\"text/javascript\"]/text()")
        # traverse through every script
        for script in text_scripts:
            # attempt to get the javascript object containing all of the courses and their information
            course_data_raw = re.search(r"(?<=window.STUDIP.MyCoursesData\s=\s)([\s\S]+)", script.get())
            #if the information is contained in the script
            if(course_data_raw):
                # load it in json format, the last char in the raw data is a semicolon so it should be removed
                course_data = json.loads(course_data_raw.group()[:-1])
                # traverse each course
                for course_id in course_data["courses"]:
                    # extract the course
                    course_name = course_data["courses"][course_id]["name"]
                    course = StudipCourse(cid=course_id, course_name=course_name)
                    yield course
