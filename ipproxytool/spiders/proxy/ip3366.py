#-*- coding: utf-8 -*-
from scrapy.exceptions import CloseSpider,IgnoreRequest
from .basespider import BaseSpider
from datetime import datetime
import time 
from ...items  import IpProxyItem
import re

class ip3366Spider(BaseSpider):
    name = 'ip3366'
    maxPage=8
    
    def __init__(self,*a,**kw):
        super(ip3366Spider,self).__init__(*a,**kw)
        
        #http://www.ip3366.net/free/?stype=4&page=2
        url_head = ''
        self.urls = []
        for i in range(1,5):
            self.urls +=["http://www.ip3366.net/free/?stype={stype}&page={page}".format(stype=i,page=page) for page in range(1,8)]
            
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 Firefox/50.0',
        }

        self.init()        
    def parse_page(self, response):
        try:
            pattern = re.compile("<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*</tr>",re.S)
            infos=re.findall(pattern,response.text)
            time.sleep(3)
            if len(infos)==0:
                print("%s empty,please check"%ip3366Spider.name) 
                raise CloseSpider
            for i in infos:
                item = IpProxyItem()
                item['ip'] = i[0]
                item['port'] = i[1]
                item['country'] = i[4]
                anonymity = i[2]   
                if '高匿' in anonymity:
                    anonymity = 1
                elif '普通' in  anonymity:
                    anonymity = 2
                elif '透明' in anonymity :
                    anonymity = 3
                else:
                    print("unknow anonymity type:{name},{a}".format(name=ip3366Spider.name,a=anonymity))
                    anonymity = 0
                item['anonymity'] = anonymity
                httptype = i[3].upper().strip()
                if httptype == 'HTTPS' :
                    item['https'] = 'yes' 
                elif httptype == 'HTTP':
                    item['https'] = 'no' 
                else:
                    item['https'] ='all'
                item['httptype'] = httptype
                item['speed'] = 0                
                item['alive'] = 0             
                item['valid_time'] = "0000-00-00 00:00:00"
                item['valid_count'] = 0
                item['save_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['source'] = 'ip3366'
                yield item        
        except Exception as e:
                print(e)
                self.logger.warning(e)                  