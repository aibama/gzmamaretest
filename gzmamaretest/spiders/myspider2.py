# coding:utf-8
import time
import os
import re
import shutil
import scrapy  # 导入scrapy包
from bs4 import BeautifulSoup
from parsel import Selector
from scrapy.http import Request  ##一个单独的request的模块，需要跟进URL的时候，需要用它
from gzmamaretest.items import *
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import logging

logging.info('进入Log文件')
logger = logging.getLogger('Myspider2')
logger.warning("也要进入Log文件")

class Myspider2(scrapy.Spider):
    name = 'Myspider2'
    start_urls = ['http://www.gzmama.com/forum.html',]
    # bashurl = '.html'
    dir_path = 'G:\gzMaMa'# 图片存放的路径
    lastpage=0

    url_domin = "http://www.gzmama.com/"

    #设置下载延时  
    download_delay = 1
    '''
    rule2 包含 rule1
    rule2 定义了主页的url抽取逻辑
    '''
    #Rule(LinkExtractor(allow=(r"http://www.gzmama.com/(?i)[0-9A-Z-]*.html$")),callback='_url_parse',follow=True),
    rules = [
    Rule(LinkExtractor(allow=(r"^[0-9A-Za-z-]*.*html$")),callback='parse_content',follow=True),
    ]

    def parse_content(self,response):
        item = TutorialItem()
        logger.debug(response.url,level=logging.DEBUG)
        item['URL'] = response.url
        #取nav的文字信息
        item['title'] =  response.meta['title']
        #取评论div的文字信息
        #有一页评论，就继续添加request,并将此item带给下一个requests
        item['extraInfo'] = response.xpath("//td[@class='t_f']")
        
        logger.debug(item['extraInfo'])
        nxtPageDetect = response.xpath("//a[@class='nxt']/text()").extract()
        mainContentUrl = response.meta['mainContentUrl']
        if '下一页' in nxtPageDetect:
            commentpage=mainContentUrl.split('-')
            commentpage[2]=str(int(commentpage[2])+1)
            newcommentpage = '-'.join(commentpage)
            url_new = url_pre + newcommentpage
            yield Request(url_new,meta={'lastItem':item},callback=self.parse_content_next)
            url_new = url_pre
        else:
            yield item


    def parse_content_next(self,response):
        url_pre = "http://www.gzmama.com/"
        d = response.meta['lastItem']
        #在原来的item里面的extraInfo继续添加评论
        d['extraInfo'].append(response.xpath("//td[@class='t_f']"))
        nxtPageDetect = response.xpath("//a[@class='nxt']/text()").extract()
        mainContentUrl = response.meta['mainContentUrl']
        if '下一页' in nxtPageDetect:
            commentpage=mainContentUrl.split('-')
            commentpage[2]=str(int(commentpage[2])+1)
            newcommentpage = '-'.join(commentpage)
            url_new = url_pre + newcommentpage
            yield Request(url_new,callback=self.parse_content_next)
            url_new = url_pre
        else:
            yield d
