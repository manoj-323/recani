import scrapy
import time
from ani_spider.items import aniItem

class WebCrawlerSpider(scrapy.Spider):

    name = "web_crawler"
    allowed_domains = ["myanimelist.net"]
    start_urls = ["https://myanimelist.net/topanime.php?limit=100"]
    
    custom_settings = {
        'CONCURRENT_REQUESTS': 1,  # Limit concurrent requests to avoid overwhelming the server
        # 'DOWNLOAD_DELAY': .5,  # Add a small delay between requests to be polite
        # 'CLOSESPIDER_PAGECOUNT' : 50,
        'FEEDS' : {
            'data.json' : {'format' : 'json', 'overwrite' : False}
        }
    }


    # def parse(self, response):

    #     page_rows = response.xpath("//table[@class='top-ranking-table']/tr[@class='ranking-list']")
        
    #     for anime in range(1,51):
    #         url = f"//table[@class='top-ranking-table']/tr[@class='ranking-list'][{anime}]//td[2]/a/@href"
    #         completer = response.xpath("//a[@class='link-blue-box next']/@href").get()
            
    #         next_page = "https://myanimelist.net/topanime.php" + completer

    #         url = response.xpath(url).get()
    #         stats_url = url + "/stats"

    #         yield response.follow(url, callback = self.parseAnimePage, meta={'stats_url' : stats_url})
            
    #         if anime < 50:
    #             return
    #         else:
    #             yield response.follow(next_page, callback=self.parse)

    def parse(self, response):

        page_anime = response.xpath("//table[@class='top-ranking-table']//tr[@class='ranking-list']//td[2]/a/@href").getall()

        for anime in page_anime:
            print("==================================== FOR ===========================")
            stats_url = anime + '/stats'
            yield scrapy.Request(anime, callback = self.parseAnimePage, meta={'stats_url' : stats_url})
            print("==================================== FOR yield ===========================")
            
        next_page =  "https://myanimelist.net/topanime.php" + response.xpath("//*[@id='content']/div[4]/div/a[text()='Next 50']/@href").get()
        if next_page == "https://myanimelist.net/topanime.php?limit=150":
            return
        print("==================================== NEXT-PAGE ===========================")
        yield response.follow(next_page, callback=self.parse)
        time.sleep(10)



    def parseAnimePage(self, response):
            
        item = aniItem()
    
        item['name_english'] = response.xpath("//div['contentWrapper']//div[@class='spaceit_pad']//span[text()='English:']/following-sibling::text()").get()
        item['name'] = response.xpath("//div[@id='contentWrapper']//h1[@class='title-name h1_bold_none']/strong/text()").get()
        item['score'] = response.xpath("//div[@id='contentWrapper']//div[@id='content']//div[@class='stats-block po-r clearfix']/div/div/text()").get()
        item['ranked'] = response.xpath("//div[@id='contentWrapper']//div[@id='content']//div[@class='stats-block po-r clearfix']//div[@class='di-ib ml12 pl20 pt8']/span/strong/text()").get()
        item['popularity'] = response.xpath("//div[@id='contentWrapper']//div[@id='content']//div[@class='stats-block po-r clearfix']//div[@class='di-ib ml12 pl20 pt8']/span[2]/strong/text()").get()
        item['members'] = response.xpath("//div[@id='contentWrapper']//div[@id='content']//div[@class='stats-block po-r clearfix']//div[@class='di-ib ml12 pl20 pt8']/span[3]/strong/text()").get()
        item['synopsis'] = response.xpath("//div[@id='contentWrapper']//div[@id='content']//p[@itemprop='description']/text()[normalize-space()]").getall() # this xpath statement is not totally correct it needs a lot of processing
        item['synonyms'] = response.xpath("//div[@id='content']/table//td[@class='borderClass']//div[@class='spaceit_pad']/span/following-sibling::text()").get()
        
        stats_url = response.meta['stats_url']
        yield response.follow(stats_url, callback=self.parse_anime_stats, meta={'item': item})

    def parse_anime_stats(self, response):

        item = response.meta['item']
        item['type_of'] = response.xpath("//div[@id='content']//div[@class='spaceit_pad']//span[text()='Type:']/parent::div//a/text()").get()
        item['total_episodes'] = response.xpath("//div[@id='content']//div[@class='spaceit_pad']//span[text()='Episodes:']/following-sibling::text()").get()
        item['premiered'] = response.xpath("//div[@id='content']//div[@class='spaceit_pad']//span[text()='Premiered:']/parent::div//a/text()").get()
        item['studios'] = response.xpath("//div[@id='content']//div[@class='spaceit_pad']//span[text()='Studios:']/parent::div//a/text()").get()
        item['genres'] = response.xpath("//div[@id='content']//div[@class='spaceit_pad']//span[text()='Genres:']/parent::div//a/text()").getall()
        item['demographic'] = response.xpath("//div[@id='content']//div[@class='spaceit_pad']//span[text()='Demographic:']/parent::div//a/text()").get()
        item['duration_per_ep'] = response.xpath("//div[@id='content']//div[@class='spaceit_pad']//span[text()='Duration:']/following-sibling::text()").get()
        item['rating'] = response.xpath("//div[@id='content']//div[@class='spaceit_pad']//span[text()='Rating:']/following-sibling::text()").get()
        item['scored_by'] = response.xpath("//div[@id='content']//div//span[text()='Score:']/parent::div//span[@itemprop='ratingCount']/text()").get()
        item['favorites'] = response.xpath("//div[@id='content']//div[@class='spaceit_pad']/span[text()='Favorites:']/following-sibling::text()").get()
        item['aired'] = response.xpath("//div[@id='content']//div[@class='spaceit_pad']//span[text()='Aired:']/following-sibling::text()").get()
        item['source'] = response.xpath("//div[@id='content']//div[@class='spaceit_pad']//span[text()='Source:']/following-sibling::text()").get()
        item['watching'] = response.xpath("//div['contentWrapper']//div[@class='spaceit_pad']//span[text()='Watching:']/following-sibling::text()").get()
        item['completed'] = response.xpath("//div['contentWrapper']//div[@class='spaceit_pad']//span[text()='Completed:']/following-sibling::text()").get()
        item['on_hold'] = response.xpath("//div['contentWrapper']//div[@class='spaceit_pad']//span[text()='On-Hold:']/following-sibling::text()").get()
        item ['dropped'] = response.xpath("//div['contentWrapper']//div[@class='spaceit_pad']//span[text()='Dropped:']/following-sibling::text()").get()
        item['plan_to_watch'] = response.xpath("//div['contentWrapper']//div[@class='spaceit_pad']//span[text()='Plan to Watch:']/following-sibling::text()").get()
        item['total'] = response.xpath("//div['contentWrapper']//div[@class='spaceit_pad']//span[text()='Total:']/following-sibling::text()").get()
        item['scored_10_by'] = response.xpath("//div['contentWrapper']//h2[text()='Score Stats']/following-sibling::table/tr[1]//small/text()").get()
        item['scored_9_by'] = response.xpath("//div['contentWrapper']//h2[text()='Score Stats']/following-sibling::table/tr[2]//small/text()").get()
        item['scored_8_by'] = response.xpath("//div['contentWrapper']//h2[text()='Score Stats']/following-sibling::table/tr[3]//small/text()").get()
        item['scored_7_by'] = response.xpath("//div['contentWrapper']//h2[text()='Score Stats']/following-sibling::table/tr[4]//small/text()").get()
        item['scored_6_by'] = response.xpath("//div['contentWrapper']//h2[text()='Score Stats']/following-sibling::table/tr[5]//small/text()").get()
        item['scored_5_by'] = response.xpath("//div['contentWrapper']//h2[text()='Score Stats']/following-sibling::table/tr[6]//small/text()").get()
        item['scored_4_by'] = response.xpath("//div['contentWrapper']//h2[text()='Score Stats']/following-sibling::table/tr[7]//small/text()").get()
        item['scored_3_by'] = response.xpath("//div['contentWrapper']//h2[text()='Score Stats']/following-sibling::table/tr[8]//small/text()").get()
        item['scored_2_by'] = response.xpath("//div['contentWrapper']//h2[text()='Score Stats']/following-sibling::table/tr[9]//small/text()").get()
        item['scored_1_by'] = response.xpath("//div['contentWrapper']//h2[text()='Score Stats']/following-sibling::table/tr[10]//small/text()").get()


        yield item
