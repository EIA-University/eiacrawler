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
        divs = response.css('div').getall()
        print(divs)
