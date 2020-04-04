# -*- coding: utf-8 -*-
import scrapy
import json

class UsersSpider(scrapy.Spider):
    name = 'users'
    allowed_domains = ['tiktok.com']
    start_urls = ['https://tikrank.com/influencer/influencers?page_num=10000&page_size=1&sorted_by=followers&country=FR&fans_count=0&keyword=&order=desc', 'https://tikrank.com/influencer/influencers?page_num=1&page_size=10000&sorted_by=followers&country=ES&fans_count=0&keyword=&order=desc']
    custom_settings = {'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    tiktok_url = 'https://www.tiktok.com/@'
    def parse(self, response):
        people = response.text
        parsed = json.loads(people)["data"]["kols"]
        for person in parsed:
            yield scrapy.Request(url = self.tiktok_url + person["kol_unique_id"], callback = self.parse_users, meta = { "country" : response.request.url })
    def parse_users(self, response):
        data = json.loads(response.css('script#__NEXT_DATA__::text')[0].re('.*')[0])['props']['pageProps']
        if 'userData' not in data:
            yield None
        else:
            if response.meta['country'] == 'https://tikrank.com/influencer/influencers?page_num=1&page_size=1&sorted_by=followers&country=DE&fans_count=0&keyword=&order=desc':
                country = 'Germany'
            else:
                country = 'Spain'
            yield {
                'ChannelName': data['userData']['uniqueId'],
                'Nickname':  data['userData']['nickName'],
                'FollowingCount':  data['userData']['following'],
                'FollowerCount':  data['userData']['fans'],
                'ChannelDescription':  data['userData']['signature'],
                'VideoCount' :  data['userData']['video'],
                'TotalLikes' :  data['userData']['heart'],
                'Verified' :  data['userData']['verified'],
                'Country': country
            }