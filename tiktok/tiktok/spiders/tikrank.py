# -*- coding: utf-8 -*-
import scrapy
import json


class TikrankSpider(scrapy.Spider):
    name = 'tikrank'
    start_urls = ['https://tikrank.com/influencer/influencers?page_num=1&page_size=10000&sorted_by=followers&country=DE&fans_count=0&keyword=&order=desc']
    
    def parse(self, response):
        people = response.text
        parsed = json.loads(people)["data"]["kols"]
        i = 0
        for person in parsed:
            i = i + 1
            print(i ," ", person["kol_unique_id"])
        yield None


#Second page