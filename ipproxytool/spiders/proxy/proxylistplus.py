#-*- coding: utf-8 -*-

from scrapy import Selector
from .basespider import BaseSpider
from proxy import Proxy
from datetime import datetime
from ...items  import IpProxyItem
import re

class ProxylistplusSpider(BaseSpider):
    name = 'proxylistplus'
    maxPage=7

    def __init__(self, *a, **kw):
        super(ProxylistplusSpider, self).__init__(*a, **kw)

        self.urls = ['https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-%s' % n for n in range(1, ProxylistplusSpider.maxPage)]
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'list.proxylistplus.com',
            'If-Modified-Since': 'Mon, 20 Feb 2017 07:47:35 GMT',
            'If-None-Match': 'list381487576865',
            'Referer': 'https://list.proxylistplus.com/Fresh-HTTP-Proxy',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:51.0) Gecko/20100101 Firefox/51.0',
        }

        self.is_record_web_page = False
        self.init()

    def parse_page(self, response):
        #self.write(response.body)
        try:
            pattern=re.compile("<td>(.*?)</td>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*<td>(.*?)</td>")
            infos = re.findall(pattern,response.text)
            if len(infos)==0:
                print("%s empty,please check"%ProxylistplusSpider.name)
            for i in infos:
                item = IpProxyItem()
                item['ip'] = i[1]
                item['port'] = i[2]
                #country = re.findall("flags/(.*?).png", i[0])
                item['country'] = i[4]
                anonymity = i[3]                
                # transparent < anonymous < elite(High Anonymity) | 	elite 27ed
                if 'elite' in anonymity: #'高匿'
                    anonymity = 1
                elif anonymity == 'transparent':
                    anonymity = 3
                elif anonymity == 'anonymous' :
                    anonymity = 2
                else:
                    anonymity = 0 #unkown                
                item['anonymity'] = anonymity
                item['https'] = i[5]
                httptype ='http' if i[5].strip()=='no' else 'https'
                item['httptype'] = httptype
                item['speed'] = 0                
                item['alive'] = 0             
                item['valid_time'] = "0000-00-00 00:00:00"
                item['valid_count'] = 0
                item['save_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['source'] = 'proxylistplus'
                yield item        
        except Exception as e:
            print(e)
            self.logger.warning(e)    