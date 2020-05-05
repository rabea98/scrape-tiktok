# -*- coding: utf-8 -*-
import scrapy
import json
from Naked.toolshed.shell import muterun_js

class UsersSpider(scrapy.Spider):
    name = 'users'
    allowed_domains = ['tiktok.com']
    start_urls = ['https://tikrank.com/influencer/influencers?page_num=1&page_size=10000&sorted_by=followers&country=DE&fans_count=0&keyword=&order=desc',
     'https://tikrank.com/influencer/influencers?page_num=1&page_size=10000&sorted_by=followers&country=ES&fans_count=0&keyword=&order=desc',
     'https://tikrank.com/influencer/influencers?page_num=1&page_size=10000&sorted_by=followers&country=FR&fans_count=0&keyword=&order=desc']
    custom_settings = {'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    tiktok_url = 'https://www.tiktok.com/@'
    def parse(self, response):
        people = response.text
        parsed = json.loads(people)["data"]["kols"]
        for person in parsed:
            yield scrapy.Request(url = self.tiktok_url + person["kol_unique_id"], callback = self.parse_user_info, meta = { "country" : response.request.url })
    def parse_user_info(self, response):
        data = json.loads(response.css('script#__NEXT_DATA__::text')[0].re('.*')[0])['props']['pageProps']
        if 'userData' not in data:
            yield None
        else:
            if response.meta['country'] == 'https://tikrank.com/influencer/influencers?page_num=1&page_size=10000&sorted_by=followers&country=DE&fans_count=0&keyword=&order=desc':
                country = 'Germany'
            elif response.meta['country'] == 'https://tikrank.com/influencer/influencers?page_num=1&page_size=10000&sorted_by=followers&country=ES&fans_count=0&keyword=&order=desc':
                country = 'Spain'
            else:
                country = 'France'
            # Generating user media singature using nodeJS browser.js script. Script is called using Naked lib
            #https://m.tiktok.com/api/item_list/?count=20&id=24708389&type=1&maxCursor=0&minCursor=0&sourceType=8&appId=1233&region=ES&language=es&verifyFp=&_signature=
            userMediaLink = "https://m.tiktok.com/api/item_list/?count=60&id=" + data['userData']['userId'] + "&type=1&secUid=" + data['userData']['secUid'] + "&maxCursor=0&minCursor=0&sourceType=8&appId=1233&region=ES&language=es&verifyFp="
            userMediaSignature = muterun_js('..\\..\\tiktok-signature-master\\browser.js', '"' + userMediaLink + '"')   # TODO get correct absolute path to the script
            if userMediaSignature.exitcode == 0:
            # Calling method get_media_data and passing some meta data
                yield scrapy.Request(userMediaLink + "&_signature=" + userMediaSignature.stdout.decode("utf-8"), 
                    callback=self.parse_user_media, 
                    meta={
                    'ChannelName':  data['userData']['uniqueId'],
                    'Nickname':  data['userData']['nickName'],
                    'FollowingCount':  data['userData']['following'],
                    'FollowerCount':  data['userData']['fans'],
                    'ChannelDescription':  data['userData']['signature'],
                    'VideoCount' :  data['userData']['video'],
                    'TotalLikes' :  data['userData']['heart'], 
                    'Verified' :  data['userData']['verified'],
                    'Country': country})
    def parse_user_media(self, response):
        userContent = json.loads(response.text)
        userVideos = []
        if 'items' not in userContent:
            yield {
                'ChannelName': response.meta['ChannelName'],
                'Nickname': response.meta['ChannelName'],
                'FollowingCount':  response.meta['FollowingCount'],
                'FollowerCount':  response.meta['FollowerCount'],
                'ChannelDescription':  response.meta['ChannelDescription'],
                'VideoCount' :  response.meta['VideoCount'],
                'TotalLikes' :  response.meta['TotalLikes'], 
                'Verified' :  response.meta['Verified'],
                'Country': response.meta['Country'],
                'VideosInfo': userVideos
                }
        else:
            items = userContent['items']
            for item in items:
                try:
                    textExtra = item['textExtra']
                except KeyError:
                    textExtra = []
                try:
                    musicInfo = {
                        'Author': item['music']['authorName'],
                        'Title': item['music']['title'],
                        'MusicUrl': item['music']['playUrl'],
                        'MusicOriginal': item['music']['original']  
                    }
                except KeyError:
                    musicInfo = {}
                userVideos.append({
                    'Description': {
                        'DescText': item['desc'],
                        'Duration': item['video']['duration'],
                    },
                    'Music': musicInfo,
                    'Hashtags': textExtra,
                    'Stats': {
                        'LikesCount': item['stats']['diggCount'],
                        'ShareCount': item['stats']['shareCount'],
                        'CommentsCount': item['stats']['commentCount'],
                        'ViewsCount': item['stats']['playCount']
                    }
                })
            yield {
                'ChannelName': response.meta['ChannelName'],
                'Nickname': response.meta['ChannelName'],
                'FollowingCount':  response.meta['FollowingCount'],
                'FollowerCount':  response.meta['FollowerCount'],
                'ChannelDescription':  response.meta['ChannelDescription'],
                'VideoCount' :  response.meta['VideoCount'],
                'TotalLikes' :  response.meta['TotalLikes'], 
                'Verified' :  response.meta['Verified'],
                'Country': response.meta['Country'],
                'VideosInfo': userVideos
                }
