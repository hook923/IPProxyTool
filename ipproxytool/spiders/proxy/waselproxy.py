#-*- coding: utf-8 -*-

from proxy import Proxy
from .basespider import BaseSpider
from scrapy.selector import Selector
#from time import strptime
from datetime import datetime
from ...items  import IpProxyItem


class waselproxySpider(BaseSpider):
    name = 'waselproxy'
    maxPage=8

    def __init__(self, *a, **kw):
        super(free_porxySpider, self).__init__(*a, **kw)
        
        
        self.urls = ['http://www2.waselproxy.com/free-china-proxy-list/#'] 
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 Firefox/50.0',
        }

        self.init()

    def parse_page(self, response):
        
        sel = Selector(response=response)
        '''
        infos = sel.xpath('//table[@class="table table-striped proxy-list"]/tbody/tr').extract()
        
        for info in infos:
            item = IpProxyItem()
            val = Selector(text = info)
            item['ip'] = val.xpath('//td[1]/a/text()').extract_first()
            item['port'] = val.xpath('//td[3]/text()').extract_first()
            item['country'] = val.xpath('//td[5]/text()').extract_first()
            item['anonymity'] = val.xpath('//td[10]/text()').extract_first()
            item['httptype'] = val.xpath('//td[9]/text()').extract_first()            
            item['speed'] = 0            
            item['connect'] = 0            
            item['alive'] = 0
            item['lastvalid'] = 0
            item['validtime'] = 0
            item['inputstamp'] = int(datetime.now().timestamp())
            item['url'] = 'waselproxy'
            
            yield item
        '''