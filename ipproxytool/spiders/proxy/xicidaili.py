#-*- coding: utf-8 -*-

from .basespider import BaseSpider
from scrapy.selector import Selector
from time import strptime,sleep
from datetime import datetime
from ...items  import IpProxyItem


class XiCiDaiLiSpider(BaseSpider):
    name = 'xici'  
    maxPage=200
    def __init__(self, *a, **kw):
        super(XiCiDaiLiSpider, self).__init__(*a, **kw)
        global maxPage
        
        #self.urls = ['http://www.xicidaili.com/nn/%s' % n for n in range(300, 702)] + ["http://www.xicidaili.com/wn/{n}".format(n=n ) for n in range(300, 702)]
        self.urls = ['http://www.xicidaili.com/nn/%s' % n for n in range(1, XiCiDaiLiSpider.maxPage)] + ["http://www.xicidaili.com/wn/{n}".format(n=n ) for n in range(1, XiCiDaiLiSpider.maxPage)]
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.xicidaili.com',
            'If-None-Match': 'W/"cb655e834a031d9237e3c33f3499bd34"',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 Firefox/50.0',
        }
        self.init()
    def parse_page(self, response):
        sleep(0.5)
        try:
            sel = Selector(text = response.body)
            infos = sel.xpath('//tr[@class="odd"]').extract()
            if len(infos)==0:
                print("%s empty,please check"%XiCiDaiLiSpider.name)            
            for info in infos:
                item = IpProxyItem()
                val = Selector(text = info)
                item['ip'] = val.xpath('//td[2]/text()').extract_first()
                item['port'] = val.xpath('//td[3]/text()').extract_first()
                item['country'] = val.xpath('//td[4]/a/text()').extract_first()
                anonymity = val.xpath('//td[5]/text()').extract_first()
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
                httptype =  val.xpath('//td[6]/text()').extract_first()
                httptype = httptype.strip()
                if httptype == 'HTTPS':
                    https='yes'
                elif httptype == 'HTTP':
                    https='no'
                elif 'HTTP' in httptype  and 'HTTPS' in  httptype :
                    https='all'
                else:
                    https = httptype[:4]
                item['https'] = https
                item['httptype'] = val.xpath('//td[6]/text()').extract_first()
                
                #item['speed'] = val.xpath('//td[7]/div/title').extract_first()
                item['speed'] = 0
                #item['alive'] = val.xpath('//td[9]/text()').extract_first()
                item['alive'] = 0
                validtime = val.xpath('//td[10]/text()').extract_first()
                #t = time.strptime('20' + validtime,'%Y-%m-%d %H:%M')
                #'2017-10-19 02:56:00'+
                t = '20' + validtime + ":00"
                #item['valid_time'] = datetime(*t[:6]).timestamp()
                item['valid_time'] = t
                item['valid_count'] = 0
                #item['save_time'] = int(datetime.now().timestamp())
                item['save_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['source'] = 'xici'
                yield item
        except Exception as e:
            print(e)
            self.logger.warning(e)            
            '''
            proxy = Proxy()
            proxy.set_value(
                    ip = ip,
                    port = port,
                    country = country,
                    anonymity = anonymity,
                    source = self.name,
            )

            self.add_proxy(proxy = proxy)
            '''
