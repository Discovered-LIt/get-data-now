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

#API Key: 2f48e626e6bb43afa1d50e6a9cce7728
credentials = service_account.Credentials.from_service_account_file("/Users/jjdaurora/Downloads/DiscoveredLIt-800929a7e827.json")

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

        value = {
            "source": {
                "id": "recode",
                "name": "Recode"
            },
            "author": "Sara Morrison",
            "title": "Elon Musk looks bad after coronavirus cases reported at Tesla factory",
            "description": "A predictable result.",
            "url": "https://www.vox.com/recode/2020/6/9/21285625/coronavirus-tesla-elon-musk-fremont-factory",
            "urlToImage": "https://cdn.vox-cdn.com/thumbor/dNhVEBSo_eqxyUOLeOp8bGRST4A=/0x392:5472x3257/fit-in/1200x630/cdn.vox-cdn.com/uploads/chorus_asset/file/20026842/GettyImages_1224450795.jpg",
            "publishedAt": "2020-06-09T21:45:00Z",
            "content": "In news that should surprise no one, workers at the Tesla factory reportedly have coronavirus. Two anonymous workers told the Washington Post reports that several cases of Covid-19 had been confirmed… [+4666 chars]"
        }

        googleClient = language.LanguageServiceClient(credentials=credentials)

        document = types.Document(
            content=value['content'],
            type=enums.Document.Type.PLAIN_TEXT)
        sentiment = googleClient.analyze_sentiment(document=document).document_sentiment

        newsItem = NewsApiItem()
        newsItem['publishedat'] = value['publishedAt']
        newsItem['id'] = value['source']['id']
        newsItem['name'] = value['source']['name']
        newsItem['author'] = value['author']
        newsItem['description'] = value['description']
        newsItem['url'] = value['url']
        newsItem['content'] = value['content']
        newsItem['sentiment'] = sentiment.score
        newsItem['magnitude'] = sentiment.magnitude

        print('news item', newsItem)
