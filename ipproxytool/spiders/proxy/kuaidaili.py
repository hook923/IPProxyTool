#-*- coding: utf-8 -*-

import re

from .basespider import BaseSpider
from datetime import datetime
from ...items  import IpProxyItem


class KuaiDaiLiSpider(BaseSpider):
    name = 'kuaidaili'
    maxPage=10

    def __init__(self, *a, **kwargs):
        super(KuaiDaiLiSpider, self).__init__(*a, **kwargs)
        self.urls = ["http://www.kuaidaili.com/ops/proxylist/{page}/".format(page=i) for i in range(1,KuaiDaiLiSpider.maxPage)]

        self.headers = {
            'Host': 'www.kuaidaili.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:52.0) Gecko/20100101 Firefox/52.0',
            # 'Referer': 'http://www.kuaidaili.com/free/inha/1/',
        }

        self.is_record_web_page = False
        self.init()

    def parse_page(self, response):
        try:
            pattern = re.compile(
                    '<tr>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>('
                    '.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?</tr>',
                    re.S)
            items = re.findall(pattern, response.text)
            if len(items)==0:
                print("%s empty,please check"%KuaiDaiLiSpider.name)               
            for i in items[2:]:
                #('121.232.145.54', '9000', '高匿名', 'HTTP', 'GET, POST', '中国 江苏省 镇江市 电信', '2秒')
                item = IpProxyItem()
                item['ip'] = i[0]
                item['port'] = i[1]
                item['country'] = i[5]
                anonymity = i[2]
                anonymity = anonymity.strip()
                if anonymity == '高匿名' or anonymity == '高匿':
                    anonymity = 1
                elif anonymity == '透明':
                    anonymity = 3
                elif anonymity == '匿名' or anonymity == '普匿':
                    anonymity = 2
                else:
                    anonymity = 0 #unkown                
                item['anonymity'] = anonymity
                httptype = i[3]
                httptype = httptype.strip()
                if httptype == 'HTTPS':
                    https='yes'
                elif httptype == 'HTTP':
                    https='no'
                elif 'HTTP' in httptype and 'HTTPS' in httptype :
                    https='all'
                else:
                    https = httptype[:4]
                item['https'] = https
                item['httptype'] = httptype
                item['speed'] = 0                
                item['alive'] = 0 
                item['valid_time'] = "0000-00-00 00:00:00"
                item['valid_count'] = 0
                item['save_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['source'] = 'kuaidaili'
                yield item
        except Exception as e:
            print(e)
            self.logger.warning(e)   