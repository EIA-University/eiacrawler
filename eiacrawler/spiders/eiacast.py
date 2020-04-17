# -*- coding: utf-8 -*-
import scrapy
import os
from scrapy.http import FormRequest
from ..items import EiacrawlerItem


class EiacastSpider(scrapy.Spider):
    name = 'eiacast'
    allowed_domains = ['eia.edu.co']
    start_urls = ['https://inicio.saber.eia.edu.co/login/index.php/']

    def parse(self, response):
        token = response.css(
            '#page-wrapper #page #page-content #region-main-box #region-main div .card .card-block div div form input::attr(value)').getall()[1]
        if token is not None:
            print(token)
            self.logger.info("got response for %r" % response.url)
            return [FormRequest.from_response(response, formid="login", formdata={
                'anchor': '',
                'logintoken': token,
                'username': os.getenv("USERNAME"),
                'password': os.getenv("PASSWORD"),

            }, callback=self.go_to_videoteca)]

    def go_to_videoteca(self, response):
        # items = EiacrawlerItem()
        self.logger.info("got response for %r" % response.url)
        url = response.css(
            '#page #page-content #region-bs-main-and-pre div #hexGrid .hex .hexIn .hexLink::attr(href)').getall()[5]
        return response.follow(url, callback=self.go_to_library)

    def go_to_library(self, response):
        print('****************************************')
        self.logger.info("got response for %r" % response.url)
        value = response.css('form input::attr(value)').getall()
        return [FormRequest.from_response(response, formid="login", formdata={
            'username': value[0],
            'password': value[1],
        }, callback=self.parse_links)]

    def parse_links(self, response):
        print('****************************************')
        self.logger.info("got response for %r" % response.url)
        urls = response.css(
            '#page #content #layout-table tr #middle-column ul li span div a::attr(href )').getall()
        return response.follow_all(urls, callback=self.go_to_libraries)

    def go_to_libraries(self, response):
        print('****************************************')
        self.logger.info("got response for %r" % response.url)
        videos = response.css(
            '#page #content .course-content #layout-table #middle-column div #thetopics .main')
        courses = response.css(
            '#page #content .course-content #layout-table #middle-column div #thetopics .cps td a span::text').getall()
        urls = []
        items = EiacrawlerItem()
        for idx, video in enumerate(videos):
            lectures = video.css('.content ul li a::attr(href)').getall()
            topics = video.css('.content ul li a span::text').getall()
            for lecture in lectures:
                urls.append(lecture)
            if len(courses) > idx:
                items['title'] = courses[idx]
                items['topics'] = topics
                items['lectures'] = lectures
            print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
            print(urls)
            print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
            yield items
