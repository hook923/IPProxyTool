# -*- coding: utf-8 -*-
from .basespider import BaseSpider
from scrapy.selector import Selector
from ...items  import IpProxyItem
import json
import re
from  datetime import datetime
import time
import hashlib
import base64

#https://www.nyloner.cn/proxy
class nylonerSpider(BaseSpider):
    name = 'nyloner'
    maxPage = 7
    
    def __init__(self, *a, **kwargs):
        super(nylonerSpider, self).__init__(*a,**kwargs)
        
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 Firefox/50.0',}
        self.urls = [self.geturl(page) for page in range(1,nylonerSpider.maxPage)]
        self.init()
    def parse_page(self, response):
        #'{"status": "true", "list": "OUofAQ89MwA2BS4AKCYvAyAFJxI8F00UIRQkByMtPVwkHAUJM18tGAYcPxcjBi8LPDowFiIUMBwiOi0BCiIeGiM/DFgsMQ0AISsrVj46PBsjOiwIJz0pXSEPP1s2BiZfL0FeCiUnHQsTNjgCIAckHCMtLRUiDyMXNQYIXykYP0smFhkCOF07GgwANBwhEC0BIDE/FzYoKgApMS8XCCgCESg9GlomLQYLIz0pXCIxNxk1OCYULDYrSyMFI1A9BDBdJV1VAScxHwEPPTMANgUuACgmLwEgBTsfPgQ8GyI9UQogAyUBIiYzABorVhcBMQ1PJSwNUD06ElklFxIVJEo+HwwyJwA2BS4AKBgvASIWXh0/LUkVIhckCiATAxUhMR0XNy8LVykxLE4mXQISOBQWCyUUIAojKlheIAxGXzUGPhYvCxkeJlwsExEAKAIgByQcIT0tASImMwAdKwMaPyENTyUsDRw/KjxfIzogBSItJRUnITdcNgYiWyoYJ0kmXF4WOyYKAg42JBwhEC0BIzE3FjUGOlwpGDsMIisnCz4tOAIMKVwLCjoPWScmEVo0KAgZLwsZHiZcPBUQOSwCIAckHCMTLRcgHEIWNC9fFygLLwEiBQEfPToWFSEtAUsiOi5YJFceGTMWAAkvCCsBIixaHD86LBkiOiQLIhMpXSEmER0wLwsZB0EkSSYVAQI4FB4bICogHCI6LQEKIh4aIz8MWCwxDQAhKytWPjo8GyM6LAgnPSldIQ8/WzYGJl4vQV4KJScdCxM2OAIgByQcIy0pXyIPOxY3P1sWKDYjDCE7Jx04Fw4LJV0nBA0XPQEhDDMANiguWighDQolLApVEzlIACUUChUkAyUYIzERGjQ4LhooGCMeITs3Uz8UEloiBDQcCCobCAscFh4aLwxYLDENASE7OxA/OixZIwQwBSITORYkHAUJM18tGAYcPxcjBi8LPSo4AiMtJBwKPgAbNDYRWDAvDBcoNitKIDsrEj46MBYmKiBAIRMhWiEPO14zX18dLDodFw03Lws9BzgCIjogCCITJRcgJkYWNBVbFi8LGR4mXCwTEQAoAiAHJBwhPS0YIyYRHTAvC14EJV8VJhUBAjgUMBsiOgYGIy0tGyMPPwk0ODZYKAgFTyEFIwsUPQ4LChcBAg06D1knJhEWNDg2GygmBUwgBSsdPD1NXyAtBgEnOggYDFY4XjMWAAkvCAkBJhYZAjhdKxwNOTAcIRAtASMPMxY3FV8WKDFeACEWLx08BBYWIDoKCyMACFYiJjBZM14DGS8IAR4mFSsSPxdNFCIHUQogEykaIzErFzMVGAkvQSwPDwE/Cz0HOAIhBDALIz05ASImMwAdKwMaPyENTyUsDRw/KjxfIzogBSItJRUnITdcNgYiWyoYJwAmXF4WOyYKAg42JBwhEC0BIzE/XDUGJl4pGCsDIRZaVT09Gh8mLQEFDEomXyQfHQkzFjoXKAgjSCYWGQI4XSscDTkwHCEQLQEjDzMWNxVfFigxXgAhFi8dPAQWFiA6CgsjEAhWIiYwWTNeAxkvCAEeJhUrHT0tTV4gPVFAIypYXiAcER0wLwsZB0EkSSYVAQI4FB5YICoCHCI6LQEKIh4aIz8MWCwxDQAhKytWPjo8GyM6LAgnPSldIQ8/WzYGJhkvQV4KJScdCxM2OAIgByQcIy0pXSIPN1s2P1sWKCY7DCIVBQs+LTgCDClcCwo6D1knJhFaNC8MHSwxCkkNOF8JOBQWCyUULAUjLQ8bIzEzGjQGIgkoJjdPIRUFUz86EgIJPRIVCwAIHw0mEVgwLwwWKCY3DCE7BVA+BDAZIgQkRiQAGwgkVjAYGgI+ACobLxcjKy8LPi04AgspCQY0Kg9ZJyYRFzQoKl0pJisOIDsnHzsqPF4gBChHIRMpWiRWQwo="}'
        try:
            print(response.text)            
            ipdict=eval(response.text)
            
            ipstr = ipdict['list']
            iplist =eval(self.decode_str(ipstr.encode()))
            ##[{'ip': '103.12.161.160', 'port': '52335', 'time': '2017-10-23 02:21:28'}, {'ip': '101.53.101.172', 'port': '9999', 'time': '2017-10-23 02:21:27'}, {'ip': '103.9.188.32', 'port': '52335', 'time': '2017-10-23 02:21:27'}, {'ip': '1.190.237.12', 'port': '8888', 'time': '2017-10-23 02:21:26'}, {'ip': '109.71.181.234', 'port': '53281', 'time': '2017-10-23 02:21:22'}, {'ip': '107.172.4.198', 'port': '1080', 'time': '2017-10-23 02:21:21'}, {'ip': '107.172.4.204', 'port': '1080', 'time': '2017-10-23 02:21:21'}, {'ip': '107.175.70.88', 'port': '1080', 'time': '2017-10-23 02:21:21'}, {'ip': '110.10.72.39', 'port': '80', 'time': '2017-10-23 02:21:21'}, {'ip': '110.78.141.133', 'port': '52335', 'time': '2017-10-23 02:21:21'}, {'ip': '111.185.153.40', 'port': '80', 'time': '2017-10-23 02:21:21'}, {'ip': '111.56.5.41', 'port': '80', 'time': '2017-10-23 02:21:21'}, {'ip': '113.214.13.1', 'port': '8000', 'time': '2017-10-23 02:21:21'}, {'ip': '114.215.102.168', 'port': '8081', 'time': '2017-10-23 02:21:21'}, {'ip': '114.215.103.121', 'port': '8081', 'time': '2017-10-23 02:21:21'}]
            if len(iplist)==0:
                print("%s empty,please check"%nylonerSpider.name)            
            for ip in iplist:
                item = IpProxyItem()
                item['ip'] = ip['ip']
                item['port'] = ip['port']
                item['country'] = ''
                item['anonymity'] = 1
                item['https'] = 0 
                item['httptype'] = ''
                item['speed'] = 0                
                item['alive'] = 0            
                item['valid_time'] = ip['time']
                item['valid_count'] = 0
                item['save_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['source'] = 'nyloner'
            
                yield item
        except Exception as e:
            print(e)
            self.logger.warning(e)                 
        '''
        https://www.nyloner.cn/proxy?page=1&num=15&token=d71f5af7c6bda3b7fc96812fd339a114&t=1508754621
        [{'ip': '43.240.138.31', 'port': '8080', 'time': '2017-10-23 18:30:24'}, {'ip': '197.250.8.162', 'port': '65103', 'time': '2017-10-23 18:30:24'}, {'ip': '118.69.61.212', 'port': '53281', 'time': '2017-10-23 18:30:14'}, {'ip': '103.53.83.112', 'port': '52335', 'time': '2017-10-23 18:29:58'}, {'ip': '180.183.249.214', 'port': '8080', 'time': '2017-10-23 18:29:58'}, {'ip': '91.197.220.51', 'port': '3128', 'time': '2017-10-23 18:29:57'}, {'ip': '172.80.118.212', 'port': '1080', 'time': '2017-10-23 18:29:55'}, {'ip': '41.184.178.86', 'port': '53281', 'time': '2017-10-23 18:29:55'}, {'ip': '190.186.58.214', 'port': '53281', 'time': '2017-10-23 18:29:52'}, {'ip': '67.53.121.66', 'port': '8080', 'time': '2017-10-23 18:29:52'}, {'ip': '115.200.12.52', 'port': '80', 'time': '2017-10-23 18:29:51'}, {'ip': '109.72.230.214', 'port': '53281', 'time': '2017-10-23 18:29:49'}, {'ip': '101.53.101.172', 'port': '9999', 'time': '2017-10-23 18:29:47'}, {'ip': '183.26.244.96', 'port': '8080', 'time': '2017-10-23 18:29:47'}, {'ip': '115.79.43.156', 'port': '8888', 'time': '2017-10-23 18:29:46'}]
        https://www.nyloner.cn/proxy?page=2&num=15&token=1db9a65fd986884006482d771c0f495c&t=1508754621
        [{'ip': '115.79.43.156', 'port': '8888', 'time': '2017-10-23 18:29:46'}, {'ip': '116.199.2.197', 'port': '80', 'time': '2017-10-23 18:29:42'}, {'ip': '116.199.2.208', 'port': '80', 'time': '2017-10-23 18:29:42'}, {'ip': '116.199.115.78', 'port': '81', 'time': '2017-10-23 18:29:42'}, {'ip': '117.4.246.95', 'port': '8080', 'time': '2017-10-23 18:29:42'}, {'ip': '115.159.50.52', 'port': '80', 'time': '2017-10-23 18:29:42'}, {'ip': '119.23.59.171', 'port': '8080', 'time': '2017-10-23 18:29:42'}, {'ip': '120.77.201.46', 'port': '8080', 'time': '2017-10-23 18:29:42'}, {'ip': '120.77.255.133', 'port': '8088', 'time': '2017-10-23 18:29:42'}, {'ip': '113.89.56.40', 'port': '8118', 'time': '2017-10-23 18:29:42'}, {'ip': '113.214.13.1', 'port': '8000', 'time': '2017-10-23 18:29:42'}, {'ip': '112.35.48.144', 'port': '8088', 'time': '2017-10-23 18:29:42'}, {'ip': '112.35.29.53', 'port': '8088', 'time': '2017-10-23 18:29:42'}, {'ip': '111.56.5.42', 'port': '8080', 'time': '2017-10-23 18:29:42'}, {'ip': '110.77.238.132', 'port': '52335', 'time': '2017-10-23 18:29:42'}]
        https://www.nyloner.cn/proxy?page=3&num=15&token=cbb915e9eaf5814636960ceb5dc22bc4&t=1508754621
        [{'ip': '115.159.50.52', 'port': '80', 'time': '2017-10-23 18:29:42'}, {'ip': '116.199.2.209', 'port': '80', 'time': '2017-10-23 18:29:42'}, {'ip': '114.226.38.171', 'port': '808', 'time': '2017-10-23 18:29:41'}, {'ip': '14.102.46.133', 'port': '53005', 'time': '2017-10-23 18:29:40'}, {'ip': '124.41.213.92', 'port': '53005', 'time': '2017-10-23 18:29:39'}, {'ip': '177.131.55.147', 'port': '53281', 'time': '2017-10-23 18:29:38'}, {'ip': '164.160.142.60', 'port': '53281', 'time': '2017-10-23 18:29:38'}, {'ip': '182.253.178.103', 'port': '8080', 'time': '2017-10-23 18:29:38'}, {'ip': '49.69.106.229', 'port': '8888', 'time': '2017-10-23 18:29:38'}, {'ip': '185.135.226.254', 'port': '52335', 'time': '2017-10-23 18:29:38'}, {'ip': '121.196.226.246', 'port': '84', 'time': '2017-10-23 18:29:38'}, {'ip': '188.0.184.100', 'port': '8080', 'time': '2017-10-23 18:29:38'}, {'ip': '130.185.78.176', 'port': '80', 'time': '2017-10-23 18:29:37'}, {'ip': '186.227.8.21', 'port': '3128', 'time': '2017-10-23 18:29:37'}, {'ip': '95.78.192.135', 'port': '53281', 'time': '2017-10-23 18:29:37'}]
        https://www.nyloner.cn/proxy?page=4&num=15&token=2e8e5a44fedfd765bbc41901e0fc83c1&t=1508754621
        [{'ip': '193.37.152.6', 'port': '3128', 'time': '2017-10-23 18:29:37'}, {'ip': '130.185.78.176', 'port': '80', 'time': '2017-10-23 18:29:37'}, {'ip': '186.227.8.21', 'port': '3128', 'time': '2017-10-23 18:29:37'}, {'ip': '180.153.58.154', 'port': '8088', 'time': '2017-10-23 18:29:37'}, {'ip': '183.230.177.170', 'port': '8081', 'time': '2017-10-23 18:29:37'}, {'ip': '182.254.247.171', 'port': '9000', 'time': '2017-10-23 18:29:37'}, {'ip': '182.254.152.225', 'port': '80', 'time': '2017-10-23 18:29:37'}, {'ip': '188.165.240.92', 'port': '3128', 'time': '2017-10-23 18:29:36'}, {'ip': '103.209.177.162', 'port': '52305', 'time': '2017-10-23 18:29:34'}, {'ip': '187.69.120.151', 'port': '8080', 'time': '2017-10-23 18:29:34'}, {'ip': '187.243.251.34', 'port': '65103', 'time': '2017-10-23 18:29:34'}, {'ip': '87.228.29.154', 'port': '53281', 'time': '2017-10-23 18:29:33'}, {'ip': '60.169.19.66', 'port': '9000', 'time': '2017-10-23 18:29:33'}, {'ip': '187.69.242.217', 'port': '8080', 'time': '2017-10-23 18:29:33'}, {'ip': '117.2.128.168', 'port': '8888', 'time': '2017-10-23 18:29:33'}]
        https://www.nyloner.cn/proxy?page=5&num=15&token=be63611cfb88f68cf74b7a363e60f591&t=1508754621
        [{'ip': '60.169.19.66', 'port': '9000', 'time': '2017-10-23 18:29:33'}, {'ip': '47.89.41.164', 'port': '80', 'time': '2017-10-23 18:29:32'}, {'ip': '47.94.230.42', 'port': '9999', 'time': '2017-10-23 18:29:32'}, {'ip': '47.94.81.119', 'port': '8888', 'time': '2017-10-23 18:29:32'}, {'ip': '47.52.20.43', 'port': '8080', 'time': '2017-10-23 18:29:32'}, {'ip': '221.7.1.99', 'port': '8080', 'time': '2017-10-23 18:29:32'}, {'ip': '5.2.69.112', 'port': '1080', 'time': '2017-10-23 18:29:32'}, {'ip': '52.17.46.39', 'port': '80', 'time': '2017-10-23 18:29:32'}, {'ip': '60.168.2.182', 'port': '8118', 'time': '2017-10-23 18:29:32'}, {'ip': '47.52.154.114', 'port': '80', 'time': '2017-10-23 18:29:32'}, {'ip': '62.255.12.3', 'port': '80', 'time': '2017-10-23 18:29:32'}, {'ip': '213.233.57.135', 'port': '80', 'time': '2017-10-23 18:29:32'}, {'ip': '77.104.250.236', 'port': '53281', 'time': '2017-10-23 18:29:32'}, {'ip': '217.65.217.68', 'port': '8080', 'time': '2017-10-23 18:29:32'}, {'ip': '89.22.175.43', 'port': '8080', 'time': '2017-10-23 18:29:32'}]        
        '''
        
    def decode_str(self,scHZjLUh1):        
        scHZjLUh1 = base64.decodestring(scHZjLUh1)
        key=b'nyloner' 
        lenth= len(key)
        schlenth=len(scHZjLUh1)
        code=''
        for i in range(schlenth):
            coeFYlqUm2 = i % lenth
            code+= chr(scHZjLUh1[i] ^ key[coeFYlqUm2])
        #print(code)
        code = base64.decodestring(code.encode())
        iplist = code.decode()
        ##[{'ip': '103.12.161.160', 'port': '52335', 'time': '2017-10-23 02:21:28'}, {'ip': '101.53.101.172', 'port': '9999', 'time': '2017-10-23 02:21:27'}, {'ip': '103.9.188.32', 'port': '52335', 'time': '2017-10-23 02:21:27'}, {'ip': '1.190.237.12', 'port': '8888', 'time': '2017-10-23 02:21:26'}, {'ip': '109.71.181.234', 'port': '53281', 'time': '2017-10-23 02:21:22'}, {'ip': '107.172.4.198', 'port': '1080', 'time': '2017-10-23 02:21:21'}, {'ip': '107.172.4.204', 'port': '1080', 'time': '2017-10-23 02:21:21'}, {'ip': '107.175.70.88', 'port': '1080', 'time': '2017-10-23 02:21:21'}, {'ip': '110.10.72.39', 'port': '80', 'time': '2017-10-23 02:21:21'}, {'ip': '110.78.141.133', 'port': '52335', 'time': '2017-10-23 02:21:21'}, {'ip': '111.185.153.40', 'port': '80', 'time': '2017-10-23 02:21:21'}, {'ip': '111.56.5.41', 'port': '80', 'time': '2017-10-23 02:21:21'}, {'ip': '113.214.13.1', 'port': '8000', 'time': '2017-10-23 02:21:21'}, {'ip': '114.215.102.168', 'port': '8081', 'time': '2017-10-23 02:21:21'}, {'ip': '114.215.103.121', 'port': '8081', 'time': '2017-10-23 02:21:21'}]
        return iplist
        
    def geturl(self,page,limitnum=15):
        '''
        var timestamp = Date.parse(new Date());
        timestamp = timestamp / 1000;
        var token = md5(String(page) + String(num) + String(timestamp)); 
    
        https://www.nyloner.cn/proxy?page=1&num=15&token=c2330aa79c46539e69e0b3f333b46c2b&t=1508695746
        '''        
        timestamp = datetime.now().timestamp()
        timestamp = int(timestamp)
        token = str(page) + str(limitnum) + str(timestamp)
        token = hashlib.md5(token.encode()).hexdigest()
        url = "https://www.nyloner.cn/proxy?page={page}&num={num}&token={token}&t={t}".format(page=page,num=limitnum,token=token,t=timestamp)
        return url
        
        