# -*- coding:utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from doubanSpider.items import DoubanspiderItem

class Douban(CrawlSpider):
    name = "douban"
    redis_key = "douban:start_urls"
    start_urls = ['http://movie.douban.com/top250']

    url = 'http://movie.douban.com/top250'

    def parse(self, response):
        item = DoubanspiderItem()
        selector  = Selector(response)
        movies = selector.xpath('//div[@class="info"]')
        for eachmovie in movies:
            title = eachmovie.xpath('//div[@class="hd"]/a/span/text()').extract()
            fulltitle = ''
            for each in title:
                fulltitle +=each

            moviesinfo = eachmovie.xpath('//div[@class="bd"]/p/text()').extract()
            # star = eachmovie.xpath('//div[@class="bd"]/div[@class="star"]/span/em/text()').extract()[0]
            quote = eachmovie.xpath('//div[@class="bd"]/p[@class="quote"]/span/text()').extract()
            if quote:
                quote = quote[0]
            else:
                quote = ''
            item['title'] = fulltitle
            item['movieInfo'] = ';'.join(moviesinfo)
            # item['star'] = star
            item['quote'] = quote
            yield item
        nextlinks = selector.xpath('//span[@class="next"]/link/@href').extract()
        if nextlinks:
            nextlinks = nextlinks[0]
            print nextlinks
            yield Request(self.url + nextlinks,callback = self.parse)

