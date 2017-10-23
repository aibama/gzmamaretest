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
logger = logging.getLogger('Myspider')
logger.warning("也要进入Log文件")

class Myspider(scrapy.Spider):
    name = 'secondHouse'
    start_urls = ['http://www.gzmama.com/forum-1253-1.html',]
    # bashurl = '.html'
    dir_path = 'G:\gzMaMaSecondHouse'# 图片存放的路径
    urlformat='http://www.gzmama.com/forum.php?mod=forumdisplay&fid=1253&page='
    lastpage=0
    urlRun = start_urls
    
    url_domin = "http://www.gzmama.com/"

    #设置下载延时  
    download_delay = 1
    #rules = [Rule(LinkExtractor(allow=[r"http://www.gzmama.com/forum.php?mod=forumdisplay&fid=1253&page=?[0-9]*"]),callback='_url_parse',follow=True),]

    def parse(self,response):
        #url_pre = "http://www.gzmama.com/"
        nxtPageDetect = response.xpath("//a[@class='nxt']/text()").extract()
        if '下一页' in nxtPageDetect:
            self.lastpage = self.lastpage+1
            #数字+样式
            urlRun =  self.urlformat+str(self.lastpage)
            yield Request(urlRun,callback=self.parse)
        item = TutorialItem()
        item['URL'] = response.xpath("//a[@class='xst']/@href").extract()
        testlist22 = response.xpath("// a[@class='xst']")
        item['title'] =  testlist22.xpath("string(.)" ).extract()
        b = zip(item['URL'],item['title'])
        #内容页爬取
        for x,y in b:
            #self.log('the url put in main page is %s',x,level=logging.DEBUG)
            #logger.debug('the url in main page is %s',x)
            #logger.debug('the title in main page is %s',y)
            url_pre = Myspider.url_domin + x
            logger.debug('the url in main page is %s',url_pre)
            yield Request(url_pre,meta={'mainContentUrl':x,'title':y},callback=self.parse_content)
            url_pre = Myspider.url_domin
        #self.log("main page response",level=logging.INFO)
        #self.log(response.text,level=logging.DEBUG)
        
    def parse_content(self,response):
        
        item = TutorialItem()
        # 应该是url_pre + mainContentUrl = response.url
        self.log(response.url,level=logging.DEBUG)
        item['URL'] = response.url
        #取nav的文字信息
        item['title'] =  response.meta['title']
        #取评论div的文字信息
        #有一页评论，就继续添加request,并将此item带给下一个requests
        item['extraInfo'] = response.xpath("//td[@class='t_f']/text()").extract()
        #self.log(item['extraInfo'],level=logging.DEBUG)
        #logger.debug(item['extraInfo'])
        nxtPageDetect = response.xpath("//a[@class='nxt']/text()").extract()
        mainContentUrl = response.meta['mainContentUrl']
        if '下一页' in nxtPageDetect:
            commentpage=mainContentUrl.split('-')
            commentpage[2]=str(int(commentpage[2])+1)
            newcommentpage = '-'.join(commentpage)
            url_new = Myspider.url_domin + newcommentpage
            yield Request(url_new,meta={'lastItem':item},callback=self.parse_content_next)
            url_new = Myspider.url_domin
        else:
            yield item


    def parse_content_next(self,response):
        #url_pre = "http://www.gzmama.com/"
        d = response.meta['lastItem']
        #在原来的item里面的extraInfo继续添加评论
        d['extraInfo'].append(response.xpath("//td[@class='t_f']/text()").extract())
        nxtPageDetect = response.xpath("//a[@class='nxt']/text()").extract()
        item = response.meta['lastItem']
        mainContentUrl = item['URL']
        if '下一页' in nxtPageDetect:
            commentpage=mainContentUrl.split('-')
            commentpage[2]=str(int(commentpage[2])+1)
            newcommentpage = '-'.join(commentpage)
            url_new = Myspider.url_domin + newcommentpage
            yield Request(url_new,callback=self.parse_content_next)
            url_new = Myspider.url_domin
        else:
            yield d
