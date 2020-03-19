# -*- coding: utf-8 -*-
import scrapy
import json

class UsersSpider(scrapy.Spider):
	name = 'users'
	allowed_domains = ['tiktok.com']
	start_urls = ['https://www.tiktok.com/@andragogan']
	custom_settings = {'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}

	def parse(self, response):
		yield {
			'ChannelName': json.loads(response.css('script#__NEXT_DATA__::text')[0].re('.*')[0])['props']['pageProps']['userData']['uniqueId'],
			'Nickname': json.loads(response.css('script#__NEXT_DATA__::text')[0].re('.*')[0])['props']['pageProps']['userData']['nickName'],
			'FollowingCount': json.loads(response.css('script#__NEXT_DATA__::text')[0].re('.*')[0])['props']['pageProps']['userData']['following'],
			'FollowerCount': json.loads(response.css('script#__NEXT_DATA__::text')[0].re('.*')[0])['props']['pageProps']['userData']['fans'],
			'ChannelDescription': json.loads(response.css('script#__NEXT_DATA__::text')[0].re('.*')[0])['props']['pageProps']['userData']['signature'],
			'VideoCount' : json.loads(response.css('script#__NEXT_DATA__::text')[0].re('.*')[0])['props']['pageProps']['userData']['video'],
			'TotalLikes' : json.loads(response.css('script#__NEXT_DATA__::text')[0].re('.*')[0])['props']['pageProps']['userData']['heart'],
			'Verified' : json.loads(response.css('script#__NEXT_DATA__::text')[0].re('.*')[0])['props']['pageProps']['userData']['verified'],
		}
