import requests
import json
import redis
import logging
import hashlib as hasher
from gzmamaretest.settings import REDIS_URL

logger = logging.getLogger(__name__)
##使用REDIS_URL链接Redis数据库, deconde_responses=True这个参数必须要，数据会变成byte形式 完全没法用
reds = redis.Redis.from_url(REDIS_URL, db=2, decode_responses=True)
login_url = 'https://passport.mama.cn/index/login/'


def init_cookie(red, spidername):
    redkeys = reds.keys()
    for user in redkeys:
        password = reds.get(user)
        if red.get("%s:Cookies:%s--%s" % (spidername, user, password)) is None:
            cookie = get_cookie(user,password)
            red.set("%s:Cookies:%s--%s"% (spidername, user, password), cookie)
##获取Cookie
#需要获得formhash
def get_cookie(account,password,formhash):
    s = requests.Session()
    md5password = md5(password)
    payload = {
        'usename': account,
        'password': md5password,
        'wp-submit': formhash,
        'redirect_to': "http://www.gzmama.com/index.html",
    }
    response = s.post(login_url, data=payload)
    cookies = response.cookies.get_dict()
    logger.warning("获取Cookie成功！（账号为:%s）" % account)
    return json.dumps(cookies)

def md5(str):
    m = hasher.md5()  
    m.update(str)
    return m.hexdigest()