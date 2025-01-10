import scrapy
class xiaohongshu_spider(scrapy.Spider):
    name="xiaohongshu"
    def start_requests(self):
        urls="https://edith.xiaohongshu.com/api/sns/web/v1/search/notes"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'content-type':'application/json;;charset=UTF-8',
          }
        yield scrapy.Request(url=urls, headers=headers, callback=self.parse)
    def parse(self,response):
        data=response.json()
        print(data)
        
