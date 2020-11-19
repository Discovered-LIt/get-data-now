import scrapy
import json
import pdb

from scrapy import Spider
from newsapi import NewsApiClient
from news_api.items import NewsApiItem
from datetime import datetime, timezone


from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import os
from google.oauth2 import service_account
import pytz 
import time

import readtime

import paralleldots

import requests

#API Key: 2f48e626e6bb43afa1d50e6a9cce7728
credentials = service_account.Credentials.from_service_account_file("news_api/google.json")
paralleldots.set_api_key("D3ZcPSa5zmgWQl4SRgmQa1jhAV9Cgi1P2BUQAFXHDKI")


class NewsApiSpider(scrapy.Spider):
    name = "newsagg"
    headers = {'Connection': 'keep-alive','Cache-Control': 'max-age=0','DNT': '1','Upgrade-Insecure-Requests': '1','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36','Sec-Fetch-User': '?1','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3','Sec-Fetch-Site': 'same-origin','Sec-Fetch-Mode': 'navigate','Accept-Encoding': 'gzip, deflate, br','Accept-Language': 'en-US,en;q=0.9',}
    newsapi = NewsApiClient(api_key='2f48e626e6bb43afa1d50e6a9cce7728')
    today = datetime.strftime(datetime.now(), "%Y/%m/%d")
    
    def start_requests(self):
        urls = [
           'http://newsapi.org/v2/everything?q=tesla&from=' + self.today + '&to=' + self.today + '&sortBy=popularity&apiKey=2f48e626e6bb43afa1d50e6a9cce7728'
           ]

        for url in urls:
           yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)



    def parse(self, response):
        body = json.loads(response.body)
        googleClient = language.LanguageServiceClient(credentials=credentials)


        for value in body['articles']:
            
            if value['content'] is None: 
                content = ''
            else: 
                content = value['content']
                
            description = value['description']
            
            document = types.Document(
                content=content,
                type=enums.Document.Type.PLAIN_TEXT)
            sentiment = googleClient.analyze_sentiment(document=document).document_sentiment
            response = paralleldots.keywords(description)
            
            print(response)

            # pdb.set_trace()

            readTime = readtime.of_text(content)

            class Person:
                "This is a person class"
                age = 10

                def greet(self):
                    print('Hello')

            # utc 
            # local_time = pytz.timezone("America/New_York")
            # naive_datetime = datetime.strptime (value['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
            # local_datetime = local_time.localize(naive_datetime, is_dst=None)
            # utc_datetime = local_datetime.astimezone(pytz.utc)
            # utc_timestamp = datetime.replace(tzinfo=timezone.utc).timestamp()
                        
            # Getting the current date  
            # and time 
            dt = datetime.strptime (value['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
  
            
            # pdb.set_trace()

            # utc_time = dt.replace(tzinfo = timezone.utc) 
            # utc_timestamp = utc_time.timestamp() 
            
            # print(utc_timestamp)
            

            newsItem = NewsApiItem()
            
            newsItem['publishDate'] = value['publishedAt']
            newsItem['publisher'] = value['source']['name']
            newsItem['author'] = value['author']
            newsItem['description'] = value['description']
            newsItem['articleLink'] = value['url']
            newsItem['sentiment'] = sentiment.score
            # newsItem['magnitude'] = sentiment.magnitude
            newsItem['title'] = value['title']
            newsItem['tags'] = "auto"
            newsItem['topic'] = 'tesla'
            newsItem['readTime'] = readTime.seconds
            newsItem['utc'] = time.time()
            # pdb.set_trace()

        
            # newsItem['author_sentiment'] = updateAuthorSentiment
            # newsItem['publisher_sentiment'] = updatePublisherSentiment

            # get the news story
            # run the sentiment analysis on that story 
            # attribute sentiment to the author and store that data independently 
            # attribute sentiment to the publisher and store that data independently 
            # attribute sentiment to the news story as well and finish the news agg process and store data

            # print('news item', newsItem)
            yield newsItem