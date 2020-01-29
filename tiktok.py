# -*- coding: utf-8 -*-
import scrapy


class TiktokSpider(scrapy.Spider):
    name = 'tiktok'
    allowed_domains = ['tiktok.com']
    start_urls = ['https://www.tiktok.com/@andragogan']
    custom_settings = {'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}

    def parse(self, response):
        yield {
            'ChannelName': response.css('h1.share-title::text').extract(),
            'UserName': response.css('h1.share-sub-title::text').extract(),
            'FollowingCount': response.css("h2.count-infos span.number[title='Following']::text").extract(),
            'FollowerCount': response.css("h2.count-infos span.number[title='Followers']::text").extract(),
            'ChannelDescription': response.css('h2.share-desc::text').extract(),
        }



