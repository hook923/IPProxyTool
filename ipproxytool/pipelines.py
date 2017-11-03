# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from .items import IpProxyItem
import pymysql
class IpproxytoolPipeline(object):
    def process_item(self, item, spider):
        return item
class IpSqlPipeline(object):
    iptable = '' 
    
    def __init__(self,sqlDict):
        self.sqlDict=sqlDict
        #IpSqlPipeline.iptable = iptable
    
    @classmethod
    def from_crawler(cls,crawler):
        host=crawler.settings.get('MYSQL_HOST')
        port=crawler.settings.get('MYSQL_PORT')
        user = crawler.settings.get('MYSQL_USER')
        password = crawler.settings.get('MYSQL_PASSWORD')
        charset = crawler.settings.get('MYSQL_CHARSET')
        database = crawler.settings.get('DATABASE')
        cls.iptable = crawler.settings.get('IPTABLE')
        return cls(sqlDict={'host':host,
                            'port':port,
                            'user':user,
                            'password':password,
                            'db':database,
                            'charset':charset,})
                            #'cursorclass':pymysql.cursors.DictCursor})
    def open_spider(self,spider):
        self.connect=pymysql.connect(**self.sqlDict)
        self.cursor = self.connect.cursor()
    def close_spider(self,spider):
        self.connect.commit()
        self.connect.close()
    
    
    def process_item(self,item,spider):  
        print("start save...")
        if dict(item)=={}:
            print('empty item')
            return item
        
        try:            
            command =   (" insert IGNORE into {} " 
                         " (id,ip,port,country,anonymity,https,httptype,speed,alive,valid_time,valid_count,save_time,source)" 
                         " values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ".format(IpSqlPipeline.iptable))
            data = (None,item['ip'],item['port'],item['country'],item['anonymity'],item['https'],item['httptype'],item['speed'],
                    item['alive'],item['valid_time'],item['valid_count'],item['save_time'],item['source']) 
            #print(command)
            print(data)
            self.cursor.execute(command,data)
            #self.connect.commit()
            return item
        except Excetion as e:
            print(e)
            spider.logger.warning("save exception:%s" % item)
            return item
