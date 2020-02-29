import scrapy
import json

from scrapy import Spider
from newsapi import NewsApiClient
from news_api.items import NewsApiItem

#API Key: 2f48e626e6bb43afa1d50e6a9cce7728

class NewsApiSpider(scrapy.Spider):
    name = "newsagg"
    #headers = {'Connection': 'keep-alive','Cache-Control': 'max-age=0','DNT': '1','Upgrade-Insecure-Requests': '1','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36','Sec-Fetch-User': '?1','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3','Sec-Fetch-Site': 'same-origin','Sec-Fetch-Mode': 'navigate','Accept-Encoding': 'gzip, deflate, br','Accept-Language': 'en-US,en;q=0.9',}
    newsapi = NewsApiClient(api_key='2f48e626e6bb43afa1d50e6a9cce7728')

    def start_requests(self):
        #urls = [
        #    'http://newsapi.org/v2/everything?q=tesla&from=2020-02-27&to=2020-02-27&sortBy=popularity&apiKey=2f48e626e6bb43afa1d50e6a9cce7728'
        #    ]

        #for url in urls:
        #    yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

        all_articles = self.newsapi.get_everything(q='tesla',
                                      #sources='bbc-news,the-verge',
                                      #domains='bbc.co.uk,techcrunch.com',
                                      from_param='2020-02-27',
                                      to='2020-02-27',
                                      language='en',
                                      sort_by='popularity')#,
                                      #page=2)

        yield scrapy.Request(url=all_articles, callback=self.parse)


    def parse(self, response):
        body = json.loads(response.body)
        
        for key, value in body['articles'].items():
            NewsApi = NewsApiItem()
            NewsApi['publishedat'] = key
            NewsApi['id'] = value['id']
            NewsApi['name'] = value['name']
            NewsApi['author'] = value['author']
            NewsApi['description'] = value['description']
            NewsApi['url'] = value['url']
            NewsApi['content'] = value['content']

            print(NewsApi)
            yield NewsApi
