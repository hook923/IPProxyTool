# -*- coding: utf-8 -*-

import logging
import os
import sys
import time
from datetime import datetime
import telnetlib
import requests
import json
import pymysql
import traceback
import threading
lock = threading.Lock()

from ipproxytool.settings import MYSQL_HOST,MYSQL_PORT,MYSQL_USER,MYSQL_PASSWORD,MYSQL_CHARSET,DATABASE,IPTABLE
from concurrent.futures import ThreadPoolExecutor

sqlDict={'host':MYSQL_HOST,
         'port':MYSQL_PORT,
         'user':MYSQL_USER,
         'password':MYSQL_PASSWORD,
         'db':DATABASE,
         'charset':MYSQL_CHARSET,
         'cursorclass': pymysql.cursors.DictCursor}
conn =pymysql.connect(**sqlDict)
cursor = conn.cursor()

max_workers=64
telnet_pool =ThreadPoolExecutor(max_workers=max_workers)
httpbin_pool = ThreadPoolExecutor(max_workers=max_workers)
httpbin_future = []
saveip_pool = ThreadPoolExecutor(max_workers=200)
saveip_future = []
all_count=0
telnet_count=0
httpbin_count=0
saveip_count=0
  
def telnetip(ipdict):
    global all_count
    global telnet_count
    all_count+=1
    if all_count % 100==0:
        print("all:%d"%all_count)
    timeout=5
    ip = ipdict['ip']
    port = ipdict['port']
    #print("prepare valid {ip}:{port}" .format(ip=ip,port=port))    
    istelnet=False
    try:
        telnetlib.Telnet(host=ip,port=port,timeout=timeout)
        httpbin_future.append(httpbin_pool.submit(httpbin,ipdict) ) 
        telnet_count+=1
        if telnet_count % 10==0:
            print("telnet ok:%d"% telnet_count)
    except Exception:
        #print("valid {ip}:{port} fail".format(ip=ip,port=port))
        pass
    

def  httpbin(ipdict):
    global httpbin_count
    if ipdict['https']=='yes':
        httptype="https"
    elif ipdict['https']=='no':
        httptype="http"
    else:
        httptype="https" ##'unkn'
    ip = ipdict['ip']
    port = ipdict['port']    
    #print("  prepare testip %s：%s" %(ip,port))
    url="{httptype}://httpbin.org/get?show_env=1".format(httptype=httptype)
    proxies={"{httptype}":"{httptype}://{ip}:{port}".format(httptype=httptype,ip=ip,port=port) }
    headers={'User-Agent': 'BaiDuSpider',
             "Connection": "close",}
    time.sleep(0.1)
    try:
        start=time.time()
        requests.adapters.DEFAULT_RETRIES = 5
        r=requests.get(url,headers=headers,proxies=proxies)
        speed=round(time.time()-start,1)
        #print(r.text)
        try:
            httpbin_dict=r.json()
        except Exception:
            print("can not link httpbin.org:")
            print(r.text)
            httpbin_dict={}

        #print(ipdict['https'].strip())
        if ipdict['https'].strip()=='unkn':
            ipdict['https'] = 'no' if httptype=="http" else "yes"
            ipdict['httptype']='http' if httptype=="http" else "https"
        '''
        if httpbin_dict.get('origin')!="":
            if httpbin_dict.get('origin')!=ip.strip():
                ipdict['anonymity']=3
                print("  透明代理%s:%s" %(ip,port))
            else:
                if ipdict['anonymity']==0 or ipdict['anonymity']==3:
                    ipdict['anonymity'] =2
                else:
                    pass
        else:
            ##代理无法连接到httpbin
            pass 
        '''
        ipdict['speed'] = speed
        ipdict['valid_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ipdict['valid_count'] += 1
        saveip_future.append(saveip_pool.submit(saveip,ipdict))
        httpbin_count+=1
        print("httpbin ok:%d" % httpbin_count)
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
                    
def saveip(ipdict):
    global saveip_count
    try:        
        command= " update {table} set anonymity=%s,speed=%s,valid_time=%s,valid_count=%s,https=%s,httptype=%s where id=%s ".format(table=IPTABLE)
        data=(ipdict['anonymity'],ipdict['speed'],ipdict['valid_time'],ipdict['valid_count'],ipdict['https'],ipdict['httptype'],ipdict['id'])
        lock.acquire()
        cursor.execute(command,data)     
        lock.release()
        saveip_count+=1
        print("saveip ok:%d" % saveip_count)
    except Exception as e:
        exstr=traceback.format_exc()
        print(exstr)
        print("saveip error:{e}".format(e=ipdict))
    #print("saveip {ipdict} end".format(ipdict=ipdict))
    

if __name__ == '__main__':
    command = 'select * from {table} where source="{source}" and https="{https}" and valid_count>0'.format(table=IPTABLE,source='sixsixip' , https='unkn')
    command = 'select * from {table} where save_time>"2017-11-2 16:30:00" '.format(table=IPTABLE)
    #command = 'select * from {table} where id=7312 or id=7313'.format(table=IPTABLE)
    cursor.execute(command)
    iplist = cursor.fetchall()
    
    print(len(iplist))
    start=time.time()
    telnet_future = [telnet_pool.submit(telnetip,ipdict)  for ipdict in iplist]      
    
    for f in telnet_future:
        f.result()
    for f in httpbin_future:
        f.result()
    for f in saveip_future:
        f.result()
    end=time.time()-start
    print("all_count:%d ,telnet_count:%d ,httpbin:%d ,saveip_count:%d "% (all_count,telnet_count,httpbin_count,saveip_count))
    conn.commit()
    conn.close()    
    print(end)
    
    ##pymysql.err.InternalError: Packet sequence number wrong - got 1 expected 2
    ##pymysql.err.InterfaceError: (0, '') conn被占用时试图exec
    ##testip error:Expecting value: line 1 column 1 (char 0)  解决
    ##testip error:HTTPConnectionPool(host='121.31.101.27', port=8123): Max retries exceeded with url: http://httpbin.org/get?show_env=1 (Caused by ConnectTimeoutError(<requests.packages.urllib3.connection.HTTPConnection object at 0x0000025B0E474550>, 'Connection to 121.31.101.27 timed out. (connect timeout=5)'))
    ##testip error:HTTPConnectionPool(host='117.190.191.198', port=80): Max retries exceeded with url: http://httpbin.org/get?show_env=1 (Caused by ProxyError('Cannot connect to proxy.', ConnectionResetError(10054, '远程主机强迫关闭了一个现有的连接。', None, 10054, None)))
    ##testip error:HTTPConnectionPool(host='124.206.133.219', port=3128): Read timed out. (read timeout=5)
    ##testip error:HTTPConnectionPool(host='101.201.234.108', port=808): Max retries exceeded with url: http://httpbin.org/get?show_env=1 (Caused by ProxyError('Cannot connect to proxy.', NewConnectionError('<requests.packages.urllib3.connection.HTTPConnection object at 0x000001688FC5D7B8>: Failed to establish a new connection: [WinError 10060] 由于连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败。',)))
    ##ConnectionResetError: [WinError 10054] 远程主机强迫关闭了一个现有的连接
    ##ConnectionRefusedError: [WinError 10061] 由于目标计算机积极拒绝，无法连接。
    ##builtins.GeneratorExit yeild item时少赋值了一个字段
    
    ##'2017-10-26 03:05:52'
    ##all_count:6933 ,telnet_count:120 ,httpbin:118 ,saveip_count:118 
    ##508.0142614841461    
    ##alter table free_ipproxy change save_time save_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP;
    
    

    

