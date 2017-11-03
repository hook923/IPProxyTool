# coding=utf-8

import re

from proxy import Proxy
from .basespider import BaseSpider
from datetime import datetime
from ...items  import IpProxyItem


class SixSixIpSpider(BaseSpider):
    name = 'sixsixip'
    maxPage=100

    def __init__(self, *a, **kwargs):
        super(SixSixIpSpider, self).__init__(*a, **kwargs)

        self.urls = ['http://m.66ip.cn/%s.html' % n for n in range(1, SixSixIpSpider.maxPage)]
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'm.66ip.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 Firefox/50.0',
        }

        self.init()

    def parse_page(self, response):
        try:
            pattern = re.compile('<tr><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td></tr>',
                                 re.S)
            ##because r.encoding=='ISO-8859-1' ,r.text.encode(r.encoding).decode('utf-8')
            items = re.findall(pattern, response.body.decode('utf-8'))
            if len(items)==0:
                print("%s empty " % SixSixIpSpider.name)
                self.logger.warning("%s empty:%s"%(SixSixIpSpider.name,response.encoding))
            
            for i in items[1:]:
                #('60.178.174.42', '8081', '浙江省宁波市', '高匿代理', '2017年10月20日22时 验证')
                item = IpProxyItem()
                item['ip'] = i[0]
                item['port'] = i[1]
                item['country'] = i[2]
                anonymity = i[3] #	高匿代理
                #anonymity = anonymity.strip()
                if '高匿' in anonymity:
                    anonymity = 1
                elif '透明' in anonymity:
                    anonymity = 3
                elif '匿名' in anonymity:
                    anonymity = 2
                else:
                    anonymity = 0 #unkown
                item['anonymity'] = anonymity
                item['https'] = "unkn" #unknow 未知
                item['httptype'] = ""
                item['speed'] = 0            
                item['alive'] = 0 
                #2017年09月27日22时 验证
                datelist = re.findall('(.*?)年(.*?)月(.*?)日(.*?)时 验证',i[4])[0]
                valid_time = '%s-%s-%s %s:00:00' %(datelist[0],datelist[1],datelist[2],datelist[3])            
                item['valid_time'] = valid_time
                item['valid_count'] = 0
                item['save_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['source'] = 'sixsixip'
                yield item  
        except Exception as e:
            print(e)
            self.logger.warning(e)              
        

