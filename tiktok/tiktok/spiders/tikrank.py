# -*- coding: utf-8 -*-
import scrapy
import json


class TikrankSpider(scrapy.Spider):
    name = 'tikrank'
    start_urls = ['https://tikrank.com/tiktok-influencer-rank/top-100-influencer-in-tiktok-sorted-by-video-viewing-weekly']
    base_url = 'https://tikrank.com'
    
    def parse(self, response):
        tbody = response.css('tbody')[0]
        links = tbody.css('a::attr(href)').extract()
        for link in links:
            next_page_url = self.base_url + link
            yield scrapy.Request(url=next_page_url, callback=self.parse_details)

    def parse_details(self, response):
        userinfo = json.loads(response.text)
        data = userinfo["data"]
        username = data["platform_unique_id"]
        yield {
            'username': username
        }
        
