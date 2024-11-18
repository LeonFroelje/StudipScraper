# syntax=docker/dockerfile:1
FROM python:3
COPY dependencies.txt ./
RUN pip install -r dependencies.txt
RUN rm dependencies.txt
WORKDIR /scraper
COPY ./studip_scraper .
CMD ["scrapy", "crawl", "files"]
