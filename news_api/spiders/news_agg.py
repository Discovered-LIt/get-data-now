import scrapy
import json
import pdb

from scrapy import Spider
from newsapi import NewsApiClient
from news_api.items import NewsApiItem
from datetime import datetime

import paralleldots

# Setting your API key
paralleldots.set_api_key("D3ZcPSa5zmgWQl4SRgmQa1jhAV9Cgi1P2BUQAFXHDKI")

# Viewing your API key
# paralleldots.get_api_key()

#API Key: 2f48e626e6bb43afa1d50e6a9cce7728

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
        
        for value in body['articles']:
            
            text= value['description']
            lang_code="en"
            response=paralleldots.sentiment(text,lang_code)
            
            # pdb.set_trace()

            newsItem = NewsApiItem()

            newsItem['publishedat'] = value['publishedAt']
            newsItem['id'] = value['source']['id']
            newsItem['name'] = value['source']['name']
            newsItem['author'] = value['author']
            newsItem['description'] = value['description']
            newsItem['url'] = value['url']
            newsItem['content'] = value['content']
            newsItem['sentiment'] = response.keys()
            

            yield newsItem
