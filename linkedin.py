# -*- coding: utf-8 -*-
import scrapy
import time


class LinkedinSpider(scrapy.Spider):
    name = 'linkedin'
    allowed_domains = ['linkedin.com']
    start_urls = ['https://linkedin.com/login']

    def parse(self, response):
        self.log("I just visited " + response.url)
        return scrapy.FormRequest.from_response(
            response,
            formdata={'session_key': 'EMAIL/NUMBER', 'session_password': 'PASSWORD'},
            callback=self.afterlogin
        )
    def afterlogin(self, response):
        time.sleep(5)
        return scrapy.Request(url="https://linkedin.com/in/NAMEOFPERSON", callback=self.scraperado)
        #if "Incorrect password" in response.body:
         #   self.logger.error("Login failed!")
        #else:
        #self.logger.error("Login succeeded!")
        #time.sleep(10)
        #yield {
        #    'pleasetext': response.body,
        #    'sometext': response.css('h4.launchpad__title::text').extract()
        #}

    def scraperado(self, response):
        time.sleep(4)
        yield {
            'pleasetext': response.body,
            'sometext': response.css('h2.pv-app-promo-section__main-title::text').extract()
        }
