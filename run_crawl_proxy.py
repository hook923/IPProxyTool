# -*- coding: utf-8 -*-

import logging
import os
import sys
import scrapydo
import time
import utils
import config

from sql import SqlManager
from ipproxytool.spiders.proxy.xicidaili import XiCiDaiLiSpider
from ipproxytool.spiders.proxy.sixsixip import SixSixIpSpider
from ipproxytool.spiders.proxy.ip181 import IpOneEightOneSpider
from ipproxytool.spiders.proxy.kuaidaili import KuaiDaiLiSpider
#from ipproxytool.spiders.proxy.gatherproxy import GatherproxySpider
#from ipproxytool.spiders.proxy.hidemy import HidemySpider
from ipproxytool.spiders.proxy.proxylistplus import ProxylistplusSpider
#from ipproxytool.spiders.proxy.freeproxylists import FreeProxyListsSpider
#from ipproxytool.spiders.proxy.peuland import PeulandSpider
from ipproxytool.spiders.proxy.usproxy import UsProxySpider
from ipproxytool.spiders.proxy.proxydb import ProxyDBSpider
#from ipproxytool.spiders.proxy.proxyrox import ProxyRoxSpider
from ipproxytool.spiders.proxy.socks_proxy import Socks_proxySpider
from ipproxytool.spiders.proxy.nyloner import nylonerSpider
from ipproxytool.spiders.proxy.free_proxy import free_porxySpider
from ipproxytool.spiders.proxy.data5u import data5uSpider
from ipproxytool.spiders.proxy.goubanjia import GoubanjiaSpider
from ipproxytool.spiders.proxy.ip3366 import ip3366Spider
from ipproxytool.spiders.proxy.zdaye import zdayeSpider

scrapydo.setup()

if __name__ == '__main__':
    os.chdir(sys.path[0])

    if not os.path.exists('log'):
        os.makedirs('log')

    logging.basicConfig(
        filename = 'log/crawl_proxy.log',
        format = '%(levelname)s %(asctime)s: %(message)s',
        level = logging.DEBUG
    )

    sql = SqlManager()

    spiders = [
        #XiCiDaiLiSpider,
        #SixSixIpSpider,
        #IpOneEightOneSpider,
        #KuaiDaiLiSpider,  # js 
        #GatherproxySpider,# 无法打开目标站点
        #HidemySpider,# 无法打开目标站点
        #ProxylistplusSpider,
        #FreeProxyListsSpider, # 无法打开目标站点
        # PeulandSpider,  # 目标站点失效
        #UsProxySpider,
        ProxyDBSpider, ##js
        #ProxyRoxSpider,# 无法打开目标站点
        #Socks_proxySpider,
        #nylonerSpider,#js
        #free_porxySpider,
        #data5uSpider,
        #GoubanjiaSpider,#js
        #ip3366Spider,
        #zdayeSpider,
    ]

    while True:
        utils.log('*******************run spider start...*******************')

        #sql.delete_old(config.free_ipproxy_table, 0.5)

        for spider in spiders:
            scrapydo.run_spider(spider_cls = spider)        
            
        utils.log('*******************run spider waiting...*******************')
        time.sleep(1200)
