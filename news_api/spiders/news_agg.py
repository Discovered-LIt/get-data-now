import scrapy
import json
import pdb

from scrapy import Spider
from newsapi import NewsApiClient
from news_api.items import NewsApiItem
from datetime import datetime


from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import os
from google.oauth2 import service_account

import readtime

#API Key: 2f48e626e6bb43afa1d50e6a9cce7728
credentials = service_account.Credentials.from_service_account_file("/Users/jjdaurora/dev/mvp/get-data-now/news_api/google.json")

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
            # pdb.set_trace()

            readTime = readtime.of_text(content)

            newsItem = NewsApiItem()
            
            newsItem['publishDate'] = value['publishedAt']
            newsItem['publisher'] = value['source']['name']
            newsItem['author'] = value['author']
            newsItem['description'] = value['description']
            newsItem['articleLink'] = value['url']
            newsItem['sentiment'] = sentiment.score
            newsItem['magnitude'] = sentiment.magnitude
            newsItem['title'] = value['title']
            newsItem['tags'] = {
            'name': 'auto',
            'emote': 'U+1F697'
            }
            newsItem['readTime'] = readTime.seconds
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