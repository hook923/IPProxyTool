#-*- coding: utf-8 -*-

from scrapy import Selector
from .basespider import BaseSpider
from proxy import Proxy
from ...items import IpProxyItem
from datetime import datetime

class data5uSpider(BaseSpider):
    name = 'data5u'

    def __init__(self, *a, **kw):
        # 在类的继承中，如果重定义某个方法，该方法会覆盖父类的同名方法
        # 但有时，我们希望能同时实现父类的功能，这时，我们就需要调用父类的方法了，可通过使用 super 来实现，比如：
        super(data5uSpider, self).__init__(*a, **kw)

        self.urls = ['http://www.data5u.com/']
        self.headers = {
            # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            # 'Accept-Encoding': 'gzip, deflate, sdch',
            # 'Accept-Language': 'zh-CN,zh;q=0.8',
            # 'Connection': 'keep-alive',
            'Host': 'www.data5u.com',
            'Upgrade-Insecure-Requests': 1,
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
        }

        self.init()

    def parse_page(self, response):
        #self.write(response.body)
        print("start parse data5u...")
        try:
            sel = Selector(response)
            infos = sel.xpath('//ul[@class="l2"]').extract()
            if len(infos)==0:
                print("%s empty,please check"%data5uSpider.name)            
            for i, info in enumerate(infos):
                item = IpProxyItem()
                val = Selector(text = info)
                ip = val.xpath('//ul[@class="l2"]/span[1]/li/text()').extract_first()
                port = val.xpath('//ul[@class="l2"]/span[2]/li/text()').extract_first()
                anonymity = val.xpath('//ul[@class="l2"]/span[3]/li/a/text()').extract_first()
                anonymity = anonymity.strip()
                if anonymity == '高匿':
                    anonymity = 1
                elif anonymity == '透明':
                    anonymity = 3
                elif anonymity == '匿名' or anonymity == '普匿':
                    anonymity = 2
                else:
                    anonymity = 0 #unkown                
                httptype = val.xpath('//ul[@class="l2"]/span[4]/li/a/text()').extract_first()
                country1 = val.xpath('//ul[@class="l2"]/span[5]/li/a/text()').extract_first()
                country1 = country1 if country1 else ""
                country2 = val.xpath('//ul[@class="l2"]/span[6]/li/a[1]/text()').extract_first()
                country2 = country2 if country2 else ""
                country3 = val.xpath('//ul[@class="l2"]/span[6]/li/a[2]/text()').extract_first()
                country3 = country3 if country3 else ""
                country = country1 + country2 + country3
                item['ip'] = ip
                item['port'] = port
                item['anonymity'] = anonymity
                item['https'] = 'yes' if httptype=='https' else 'no'
                item['httptype'] = httptype
                item['country'] = country
                item['speed'] = 0                
                item['alive'] = 0        
                item['valid_time'] = '0000-00-00 00:00:00'
                item['valid_count'] = 0
                item['save_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['source'] = 'data5u'
                yield item             
        except Exception as e:
            print(e)
            self.logger.warning(e)  
