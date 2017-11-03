#-*- coding: utf-8 -*-

from scrapy import Selector
from .basespider import BaseSpider
from proxy import Proxy
from ...items import IpProxyItem
from time import strptime
from datetime import datetime
import re


class IpOneEightOneSpider(BaseSpider):
    name = 'ip181'
    maxPage=695

    def __init__(self, *a, **kw):
        super(IpOneEightOneSpider, self).__init__(*a, **kw)

        self.urls = ['http://www.ip181.com/daili/{i}.html'.format(i=i) for i in range(1,IpOneEightOneSpider.maxPage)]
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Host': 'www.ip181.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 Firefox/50.0',
        }

        self.init()

    def parse_page(self, response):
        #self.write(response.body)
        try:
            html = response.text.encode(response.encoding).decode('gb2312')
            pattern=re.compile('''<tr.*?>\s+<td>(.*?)</td>\s+<td>(.*?)</td>\s+<td>(.*?)</td>\s+<td>(.*?)</td>\s+<td>(.*?)</td>\s+<td.*?>(.*?)</td>\s+<td.*?>(.*?)</td>\s+</tr>''',re.S)
            infos = re.findall(pattern,html)
            if len(infos)==0:
                print("%s empty,please check"% IpOneEightOneSpider.name)
            for i in infos[1:]:
                item = IpProxyItem()
                item['ip'] = i[0]
                item['port'] = i[1]
                item['country'] = i[5]
                anonymity = i[2]
                anonymity = anonymity.strip()
                if anonymity == '高匿':
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
                elif 'HTTP' in httptype  and 'HTTPS' in  httptype :
                    https='all'
                else:
                    https = httptype[:4]  
                item['https'] =  https   
                item['httptype'] = i[3]
                item['speed'] = 0                
                item['alive'] = 0                 
                #2017/10/23 9:00:17
                t=i[6].replace('/','-')
                item['valid_time'] = t
                item['valid_count'] = 0
                item['save_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['source'] = 'ip181'
                yield item
        except Exception as e:
            print(e)
            self.logger.warning(e)