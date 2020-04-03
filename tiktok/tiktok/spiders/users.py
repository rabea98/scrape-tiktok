# -*- coding: utf-8 -*-
import scrapy
import json

class UsersSpider(scrapy.Spider):
	name = 'users'
	allowed_domains = ['tiktok.com']
	start_urls = ['https://www.tiktok.com/@andragogan']
	custom_settings = {'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}

	def parse(self, response):
		data = json.loads(response.css('script#__NEXT_DATA__::text')[0].re('.*')[0])['props']['pageProps']
		if 'userData' not in data:
		    yield None
		else:
		    yield {
			'ChannelName': data['userData']['uniqueId'],
			'Nickname':  data['userData']['nickName'],
			'FollowingCount':  data['userData']['following'],
			'FollowerCount':  data['userData']['fans'],
			'ChannelDescription':  data['userData']['signature'],
			'VideoCount' :  data['userData']['video'],
			'TotalLikes' :  data['userData']['heart'],
			'Verified' :  data['userData']['verified'],
		    }
