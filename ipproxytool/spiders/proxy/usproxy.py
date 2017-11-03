# coding=utf-8

import re

from proxy import Proxy
from .basespider import BaseSpider
from datetime import datetime
from ...items  import IpProxyItem

class UsProxySpider(BaseSpider):
    name = 'usproxy'

    def __init__(self, *a, **kwargs):
        super(UsProxySpider, self).__init__(*a, **kwargs)

        self.urls = [
            'https://www.sslproxies.org/',
            'https://www.us-proxy.org/',
            #'https://free-proxy-list.net/uk-proxy.html',
            #'https://www.socks-proxy.net/',
        ]
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 Firefox/50.0',}
        self.init()

    def parse_page(self, response):  
        try:        
            pattern = re.compile('<tr><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td class=\'hm\'>(.*?)</td><td>(.*?)</td><td class=\'hm\'>(.*?)</td><td class=\'hx\'>(.*?)</td><td class=\'hm\'>(.*?)</td></tr>',
                    re.S)
            
            infos = re.findall(pattern, response.text)
            if len(infos)==0:
                print("%s empty,please check"%UsProxySpider.name)             
            for i in infos:
                item = IpProxyItem()
                item['ip'] = i[0]
                item['port'] = i[1]
                #country = re.findall("flags/(.*?).png", i[0])
                item['country'] = i[3]
                anonymity = i[4]
                anonymity = anonymity.strip()
                #	anonymous < elite proxy                
                if 'elite' in anonymity: #'高匿'
                    anonymity = 1
                elif anonymity == 'anonymous' :
                    anonymity = 2
                elif 'transparent' in anonymity :
                    anonymity = 3                    
                else:
                    anonymity = 0 #unkown              
                item['anonymity'] = anonymity
                item['https'] = i[6]
                httptype ='https' if i[6].strip()=='yes' else 'http'
                item['httptype'] = httptype
                item['speed'] = 0                
                item['alive'] = 0              
                item['valid_time'] = "0000-00-00 00:00:00"
                item['valid_count'] = 0
                item['save_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['source'] = 'us-proxy'
                yield item  
        except Exception as e:
            print(e)
            self.logger.warning(e) 