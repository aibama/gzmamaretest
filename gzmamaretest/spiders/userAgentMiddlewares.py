#-*-coding:utf-8-*-  
  
import random
import logging
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware #UserAegent中间件


import json ##处理json的包
import redis #Python操作redis的包
from scrapy.downloadermiddlewares.retry import RetryMiddleware #重试中间件
from gzmamaretest.settings import REDIS_URL

logger = logging.getLogger(__name__)
##使用REDIS_URL链接Redis数据库, deconde_responses=True这个参数必须要，数据会变成byte形式 完全没法用
reds = redis.Redis.from_url(REDIS_URL, db=2, decode_responses=True)


class RotateUserAgentMiddleware(object):
    """
    def __init__(self, user_agent=''):  
        self.user_agent = user_agent
    """
    def process_request(self, request, spider):  
        ua = random.choice(self.user_agent_list)  
        if ua:  
            logger.debug(ua)
            request.headers.setdefault('User-Agent', ua)  
  
    #the default user_agent_list composes chrome,I E,firefox,Mozilla,opera,netscape  
    #for more user agent strings,you can find it in http://www.useragentstring.com/pages/useragentstring.php  
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"
       ]

