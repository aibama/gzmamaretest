# -*- coding=utf8 -*-
from scrapy import cmdline
cmdline.execute("scrapy crawl secondHouse".split())

# import scrapy
# from scrapy.crawler import CrawlerProcess
# from gzmamaretest.gzmamaretest.spiders.myspider import *
# from gzmamaretest.gzmamaretest.spiders.myspider2 import *
# process = CrawlerProcess()
# process.crawl(Myspider)
# process.crawl(Myspider2)
# process.start()

#cmdline.execute("scrapy crawl zhihu -L WARNING".split())