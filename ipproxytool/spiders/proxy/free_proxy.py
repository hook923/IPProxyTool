#-*- coding: utf-8 -*-

from proxy import Proxy
from .basespider import BaseSpider
from scrapy.selector import Selector
#from time import strptime
from datetime import datetime
from ...items  import IpProxyItem


class free_porxySpider(BaseSpider):
    name = 'free_porxy'
    maxPage=8

    def __init__(self, *a, **kw):
        super(free_porxySpider, self).__init__(*a, **kw)
        
        
        self.urls = ['https://free-proxy-list.com/?search=1&page={page}&port=&type%5B%5D=http&type%5B%5D=https&up_time=0'.format(page=n) for n in range(1, free_porxySpider.maxPage)] 
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 Firefox/50.0',
        }

        self.init()

    def parse_page(self, response):
        try:
            sel = Selector(response=response)
            infos = sel.xpath('//table[@class="table table-striped proxy-list"]/tbody/tr').extract()
            if len(infos)==0:
                print("%s empty,please check"%free_porxySpider.name)              
            for info in infos:
                item = IpProxyItem()
                val = Selector(text = info)
                item['ip'] = val.xpath('//td[1]/a/text()').extract_first()
                item['port'] = val.xpath('//td[3]/text()').extract_first()
                item['country'] = val.xpath('//td[5]/text()').extract_first()
                anonymity = val.xpath('//td[10]/text()').extract_first()
                anonymity = anonymity.strip()
                if anonymity == 'High Anonymous':
                    anonymity = 1
                elif anonymity == 'Transparent':
                    anonymity = 3
                elif anonymity == 'Anonymous' :
                    anonymity = 2
                else:
                    anonymity = 0 #unkown                
                item['anonymity'] = anonymity
                httptype = val.xpath('//td[9]/text()').extract_first()
                item['https'] ='yes' if httptype=='https' else 'no'
                item['httptype'] =  httptype          
                item['speed'] = 0         
                item['alive'] = 0
                item['valid_time'] = '0000-00-00 00:00:00'
                item['valid_count'] = 0
                item['save_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['source'] = 'free_porxy'
                
                yield item
        except Exception as e:
            print(e)
            self.logger.warning(e)                 