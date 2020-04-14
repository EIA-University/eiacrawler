# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest


class EiacastSpider(scrapy.Spider):
    name = 'eiacast'
    allowed_domains = ['inicio.saber.eia.edu.co']
    start_urls = ['https://inicio.saber.eia.edu.co/login/index.php/']

    def parse(self, response):
        token = response.css(
            '#costum-login div form input::attr(value)').extract_first()
        if token is not None:
            print(token)
        else:
            print('Error: login no encontrado')
