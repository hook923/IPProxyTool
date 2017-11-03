# coding=utf-8
import re

from proxy import Proxy
from .basespider import BaseSpider
from ...items  import IpProxyItem
from datetime import datetime

class Socks_proxySpider(BaseSpider):
    name = 'Socks_proxy'

    def __init__(self, *a, **kwargs):
        super(Socks_proxySpider, self).__init__(*a, **kwargs)

        self.urls = [
            #'https://free-proxy-list.net/uk-proxy.html',
            'https://www.socks-proxy.net/',
        ]
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 Firefox/50.0',}
        '''
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.us-proxy.org',
            'If-Modified-Since': 'Tue, 24 Jan 2017 03:32:01 GMT',
            'Referer': 'http://www.sslproxies.org/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 Firefox/50.0',
        }
        '''
        self.init()

    def parse_page(self, response):   
        try:
            pattern = pattern = re.compile('<tr><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td class=\'hm\'>(.*?)</td><td>(.*?)</td><td class=\'hm\'>(.*?)</td><td class=\'hm\'>(.*?)</td><td class=\'hd\'>(.*?)</td></tr>',       re.S)
            
            infos = re.findall(pattern, response.text)
            if len(infos)==0:
                print("%s empty,please check"%Socks_proxySpider.name)               
            for i in infos:
                item = IpProxyItem()
                item['ip'] = i[0]
                item['port'] = i[1]
                #country = re.findall("flags/(.*?).png", i[0])
                item['country'] = i[3] + "_" + i[4]
                anonymity = i[5]
                anonymity = anonymity.strip()
                if 'Elite' in anonymity or 'elite' in anonymity : #'高匿'
                    anonymity = 1
                elif anonymity == 'Transparent':
                    anonymity = 3
                elif anonymity == 'Anonymous' :
                    anonymity = 2
                else:
                    anonymity = 0 #unkown                 
                item['anonymity'] = anonymity
                Https = i[6]
                item['https'] = Https
                httptype ='https' if i[6].strip()=='Yes' else 'http'
                item['httptype'] = httptype
                item['speed'] = 0                
                item['alive'] = 0              
                item['valid_time'] = "0000-00-00 00:00:00"
                item['valid_count'] = 0
                item['save_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['source'] = 'Socks_proxy'
                yield item  
        except Exception as e:
            print(e)
            self.logger.warning(e)                 