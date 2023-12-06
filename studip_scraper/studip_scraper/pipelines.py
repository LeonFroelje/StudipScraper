# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
from scrapy.pipelines.files import FilesPipeline
from urllib import parse
import logging
import re


class StudipFilesPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        # logging.info("hier")
        filename = parse.parse_qs(parse.urlparse(request.url).query)['file_name'][0]
        logging.info(os.path.join(re.sub(r"-+", "-", re.sub(r"[/:><\"\\|\?\*\.\s]", "-", item["course"])),
                            *item["parent_folders"], filename))
        return os.path.join(re.sub(r"-+", "-", re.sub(r"[/:><\"\\|\?\*\.\s]", "-", item["course"])),
                            *item["parent_folders"], filename)
    
    
