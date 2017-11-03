# coding=utf-8

from proxy import Proxy
#from scrapy.spiders import Spider
from .basespider import BaseSpider
from scrapy.selector import Selector
from ...items  import IpProxyItem
from datetime import datetime
import re


class ProxyDBSpider(BaseSpider):
    name = 'proxydb'
    maxPage=500

    def __init__(self, *a, **kwargs):
        super(ProxyDBSpider, self).__init__(*a, **kwargs)

        self.urls = ['http://proxydb.net/?protocol=http&protocol=https&offset=%s' % n for n in range(1, ProxyDBSpider.maxPage, 20)]
        self.headers = {
            'Host': 'proxydb.net',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 Firefox/50.0',
        }

        self.is_record_web_page = False
        self.init()

    def parse_page(self, response):
        try:
            sel = Selector(text = response.text)
            infos = sel.xpath('//tbody/tr').extract()
            if len(infos)==0:
                print("%s empty,please check"%ProxyDBSpider.name)             
            for i in infos:
                item = IpProxyItem()
                val = Selector(text=i)
                ipjava = val.xpath("//td[1]/script/text()").extract_first()               
                
                '''159.255.162.222:53281
                var w = \'61.552.951\'.split(\'\').reverse().join(\'\');\n                        
                var yy = \'2.222\';\n                        
                var pp = -7421 + 60702;\n            
                '''
                pattern=re.compile(".*?\'(.*?)\'.*?=\s*\'(.*?)\'.*?=\s*(.*?);.*?",re.S)           
                ipList = re.findall(pattern,ipjava) ##[('61.552.951', '2.222', '-7421 + 60702')]
                item['ip'] = ipList[0][0][::-1] + ipList[0][1] #'159.255.162.222'
                item['port'] = str(eval(ipList[0][2]))  #'53281'
                country = val.xpath("//td[3]/abbr/text()").extract_first()                
                item['country'] = country
                anonymity = val.xpath("//td[4]/span/text()").extract_first()     #'Elite'  
                anonymity = anonymity.strip()
                if anonymity == 'Elite':
                    anonymity = 1
                elif anonymity == 'Transparent':
                    anonymity = 3
                elif anonymity == 'Anonymous' :
                    anonymity = 2
                else:
                    anonymity = 0 #unkown              
                item['anonymity'] = anonymity  
                httptype = val.xpath("//td[2]/text()").extract_first()
                httptype = httptype.replace("\n","").strip()
                if httptype == 'HTTPS':
                    https='yes'
                elif httptype == 'HTTP':
                    https='no'
                elif httptype =='HTTP,HTTPS' or httptype =='HTTPS,HTTP':
                    https='all'
                else:
                    https = httptype[:4]   
                item['https'] =  https   
                item['httptype'] = httptype
                '''\n       <span class="text-success" title="Last Connect Time: 0.12s">1.0s</span>\n       /\n      <span class="text-success" title="Last Response Time: 1.73s">2.1s</span>\n'''
                speedStr=i[5]
                #speedlist = re.findall(">(.*?)s<",i[5]) #['1.0', '2.1']
                item['speed'] = 0                
                item['alive'] = 0             
                item['valid_time'] = "0000-00-00 00:00:00"
                item['valid_count'] = 0
                item['save_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['source'] = 'proxydb'
                yield item 
        except Exception as e:
            print(e)
            self.logger.warning(e) 

