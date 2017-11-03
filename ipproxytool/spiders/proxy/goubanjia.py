# -*- coding: utf-8 -*-
from .basespider import BaseSpider
from scrapy.selector import Selector
from ...items  import IpProxyItem
from lxml import etree
import re
from datetime import datetime



class GoubanjiaSpider(BaseSpider):
    name = 'Goubanjia'
    maxPage = 100
    def __init__(self, *a, **kwargs):
        super(GoubanjiaSpider, self).__init__(*a, **kwargs)
        
        self.urls = ['http://www.goubanjia.com/free/index{n}.shtml'.format(n=n) for n in range(1, GoubanjiaSpider.maxPage)]
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 Firefox/50.0',
        }

        self.is_record_web_page = False
        self.init()

    def parse_page(self, response):
        print("start parse...")
        try:
            html = etree.HTML(response.text)
            iprow=html.xpath("//table//tr[td]")
            if len(iprow)==0:
                print("%s empty,please check"%GoubanjiaSpider.name)             
            for row in iprow:
                item = IpProxyItem()
                ipList=row.xpath('./td[1]/div[@style]/text() | ./td[1]/span[@style]/text() | ./td[1]/span/text()')[:-1]
                ip = ''.join(ipList)
                item['ip']=ip
                portstr = row.xpath('./td[1]/span[contains(@class,"port")]/@class')[0] #['port EAEDCA']            
                port = self.get_poxy(portstr)
                item['port']=port                
                item['country'] = ''.join(row.xpath('./td[4]/a/text()'))
                anonymity = row.xpath('./td[2]/a/text()')[0] 
                anonymity = anonymity.strip()
                if anonymity == '高匿':
                    anonymity = 1
                elif anonymity == '透明':
                    anonymity = 3
                elif anonymity == '匿名' or anonymity == '普匿':
                    anonymity = 2
                else:
                    anonymity = 0 #unkown                
                item['anonymity'] =  anonymity          #匿名，高匿
                httptype = row.xpath('./td[3]/a/text()')[0] 
                httptype = httptype.strip()
                if httptype == 'https':
                    https='yes'
                elif httptype == 'http':
                    https='no'
                elif httptype =='http,https' or httptype =='https,http':
                    https='all'
                else:
                    https = httptype[:4]   
                item['https'] = https
                item['httptype'] = httptype
                speed = 0  #<td>1.714 秒</td>            
                item['speed'] = 0                
                item['alive'] = 0             
                item['valid_time'] = '0000-00-00 00:00:00'
                item['valid_count'] = 0
                item['save_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['source'] = 'Goubanjia'
                yield item             
        except Exception as e:
            print('error : ')  
            print(e)
            self.logger.warning(e)         
            
    def get_poxy(self,port_word): 
        _, word = port_word.split(' ') 
        num_list = [] 
        for item in word: 
            num = 'ABCDEFGHIZ'.find(item) 
            num_list.append(str(num)) 
        
        port = int("".join(num_list)) >> 0x3 
        return port 
        '''
        182.253.191.114:8080
        <td class="ip">     <td.*?><div.*?>(.*?)</div>
        <div style='display:inline-block;'></div>
        <p style='display: none;'>18</p>   
        <span>18</span>     .*?<span>(.*?)</span>
        <p style='display: none;'>2</p>
        <span>2</span>      .*?<span>(.*?)</span>
        <span style='display:inline-block;'></span>    <span.*?>(.*?)</span>
        <span style='display:inline-block;'>.2</span>  <span.*?>(.*?)</span>
        <div style='display:inline-block;'></div>      <div.*?>(.*?)</div> 
        <span style='display:inline-block;'></span>    <span.*?>(.*?)</span>
        <div style='display:inline-block;'>5</div>     <div.*?>(.*?)</div> 
        <span style='display:inline-block;'></span>    <span.*?>(.*?)</span>
        <div style='display:inline-block;'>3</div>     <div.*?>(.*?)</div> 
        <p style='display: none;'>.1</p>               .*?
        <span>.1</span>                                <span>(.*?)</span>
        <p style='display: none;'></p>                 .*?
        <span></span>                                  <span>(.*?)</span>
        <span style='display:inline-block;'>9</span>   <span.*?>(.*?)</span>
        <div style='display:inline-block;'></div>      <div.*?>(.*?)</div> 
        <p style='display: none;'>1.</p>               .*?
        <span>1.</span>                                <span>(.*?)</span>
        <div style='display:inline-block;'></div>      <div.*?>(.*?)</div> 
        <p style='display: none;'>1</p>                .*?
        <span>1</span>                                 <span>(.*?)</span>
        <span style='display:inline-block;'>14</span>: <span.*?>(.*?)</span>
        <span class="port GEGEA">8244</span></td>      <span class=\"(.*?)\">.*?</span></td>

        '''
            
        '''
        <td class="ip"><div style='display: inline-block;'></div><div style='display:inline-block;'></div><span style='display:inline-block;'>11</span><span style='display:inline-block;'></span><p style='display: none;'>5</p><span>5</span><span style='display:inline-block;'>.1</span><span style='display:inline-block;'>24</span><span style='display:inline-block;'></span><span style='display: inline-block;'>.7</span><div style='display:inline-block;'>1</div><p style='display: none;'>.</p><span>.</span><div style='display: inline-block;'></div><p style='display: none;'>2</p><span>2</span><div style='display:inline-block;'>1</div><div style='display:inline-block;'>0</div>:<span class="port GEGEA">8866</span></td>

        '''
            
