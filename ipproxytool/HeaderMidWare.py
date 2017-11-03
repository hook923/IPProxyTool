#!user/bin/env python3
#encoding:utf-8
from scrapy.utils.project import get_project_settings
from scrapy.downloadermiddlewares.retry import RetryMiddleware
#from scrapy.utils.response import response_status_message
from scrapy.exceptions import CloseSpider,IgnoreRequest
import random
#import time
#import os
#import re
#import logging
settings = get_project_settings()

'''
https
proxyList1=['120.78.15.63:80', '124.232.148.7:3128', '61.160.208.222:8080', '220.248.207.105:53281', '39.88.13.3:53281', '123.13.205.185:8080', '122.192.66.50:808']
proxyList=['124.232.148.7:3128','61.160.208.222:8080','39.88.13.3:53281']
proxyList=['111.13.7.120:80', '64.173.224.142:9991','180.173.177.64:53281', '124.232.148.7:3128', '221.229.252.98:8080', '202.98.20.209:80',  '61.158.111.142:53281', '119.90.63.3:3128']
站大爷"119.90.63.3:3128","123.138.89.133:9999","124.232.148.7:3128","122.224.227.202:3128","61.155.164.106:3128","218.201.98.196:3128","118.114.77.47:8080","47.93.3.242:80"
'''
#http
#httpproxy=['']

#import telnetlib

class ProcessHeaderMidware():
    """process request add request info"""
    
    def process_request(self,request,spider):
        """
        随机从列表中获得header， 并传给user_agent进行使用
        """
            
        userAgent=random.choice(settings.get('USER_AGENT_LIST'))
        #spider.logger.info(msg="now entring download midware")
        if userAgent:
            request.headers['User-Agent']=userAgent
            # Add desired logging message here.
            spider.logger.info(u'request headers is {}\n{}'.format(request.headers,request))
    
class CookiesMiddleware(RetryMiddleware):
    def __init__(self, settings, crawler):
        RetryMiddleware.__init__(self, settings)           
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler)
    def repushUrl(self,url,spider):
        try:
            '''
            zipUrl=zip_url(url)
            if zipUrl:
                print("re push %s" % zipUrl)
                redisConnect.rpush(redisKey,zipUrl)
            else:
                print("%s zip empty,cannot repush" % url)
            '''
        except Exception:
            print("repush url error:%s" % url)
            spider.logger.warning("<403 %s>" % url)
    def process_response(self, request, response, spider):           
        #reason=response_status_message(response.status)
        #401:{'error': {'name': 'AuthenticationInvalidRequest', 'code': 100, 'message': '请求头或参数封装错误'}}
        #403:Forbidden
        if response.status==200:
            return response
        elif response.status==404:
            print("404:%s" % request.url)
            spider.logger.warning('response error:%d ,Ignore request:<404 %s>' %( response.status,request.url))
            raise IgnoreRequest
        elif response.status in [401,403,414]: 
            print("<%d : %s>" % (response.status,request.url) )            
            spider.logger.warning("<%d : %s>" % (response.status,request.url) )
            raise IgnoreRequest
        else:##429,>500            
            print("<%d : %s>" % (response.status,request.url) )            
            spider.logger.warning("<%d : %s>" % (response.status,request.url) )
            raise IgnoreRequest            
