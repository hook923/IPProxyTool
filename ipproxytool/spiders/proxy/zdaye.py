#-*- coding: utf-8 -*-
#from scrapy.exceptions import CloseSpider,IgnoreRequest
from .basespider import BaseSpider
from datetime import datetime
import time 
from ...items  import IpProxyItem
import re
import requests

class zdayeSpider(BaseSpider):
    name="zdaye"
    #startPage=6503  #2017-10-1号
    maxPage=700
    
    def __init__(self, *a, **kw):
        super(zdayeSpider, self).__init__(*a, **kw)    
        
        #"http://ip.zdaye.com/dayProxy/2017/10/1.html" 每月1号
        currdate=datetime.now()
        url="http://ip.zdaye.com/dayProxy/{year}/{month}/1.html".format(year=currdate.year,month=currdate.month)
        headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:51.0) Gecko/20100101 Firefox/51.0',}
        try:         
            r=requests.get(url,headers=headers)
            pattern=re.compile("dayProxy/ip/(.*?)\.html",re.S)
            article_num = re.findall(pattern,r.text)[0]    
            article_num = int(article_num)
            if article_num:
                self.urls = ["http://ip.zdaye.com/dayProxy/ip/{num}.html".format(num=num) for num in range(article_num,article_num-zdayeSpider.maxPage,-1)]
            else:
                print("%s can not find start page"%zdayeSpider.name)
        except Exception as e:
            print(e)
            
        self.is_record_web_page = False
        self.init() 
    def parse_page(self,response):
        try:
            pattern = re.compile("><br>(.*?)</div>",re.S)
            infostr =re.findall(pattern,response.text)[0]
            infos = infostr.split("<br>")
            for info in infos:
                ##'111.161.22.15:8081@HTTP#[未知]天津市 网宿科技联通CDN节点'                
                item = IpProxyItem()
                row=info.split(":")
                item['ip'] = row[0]
                
                row=row[1].split("@")                
                item['port'] = row[0]
                
                row=row[1].split("#[")
                httptype = row[0].upper()
                item['httptype'] = httptype
                if httptype=='HTTP':
                    item['https'] = "no"
                elif httptype=='HTTPS':
                    item['https']=='yes'
                else:
                    item['https'] = 'unkn'
                
                row=row[1].split("]") 
                anonymity = row[0]
                if '高匿' in anonymity: #'高匿'
                    anonymity = 1
                elif anonymity == '透明':
                    anonymity = 3
                elif anonymity == '普匿' :
                    anonymity = 2
                else:   
                    anonymity = 0 #未知                
                item['anonymity'] = anonymity
                
                item['country'] = row[1]
                item['speed'] = 0                
                item['alive'] = 0             
                item['valid_time'] = "0000-00-00 00:00:00"
                item['valid_count'] = 0
                item['save_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['source'] = 'zdaye'
                print(item)
                yield item        
        except Exception as e:
            print("zdaye error")
            print(e)
            self.logger.warning(e)                 