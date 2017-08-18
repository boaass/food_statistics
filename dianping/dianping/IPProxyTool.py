# -*- coding:utf-8 -*-
import requests
import json
from Logging import Logging


class Singleton(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class IPProxyTool(Singleton):

    def __init__(self):
        self.ip_pool = []

    def requestIPs(self):
        # 讯代理
        res = requests.get('http://www.xdaili.cn/ipagent//freeip/getFreeIps?page=1&rows=10', timeout=3)
        try:
            res_dict = json.loads(res.text)
            for ip_dict in res_dict['RESULT']['rows']:
                address = (ip_dict['ip']+':'+ip_dict['port']).encode('u8')
                self.ip_pool.append(address) if self.isValidIP(address) else None
        except Exception as e:
            # Logging.debug(res.text)
            Logging.error(e.message)

    def circleRequestIPs(self, retryTime, min_ip_count):
        if retryTime == 0 or len(self.ip_pool)>=min_ip_count:
            return
        self.requestIPs()

        return self.circleRequestIPs(retryTime-1, min_ip_count)

    def refresh(self, retryTime=5, min_ip_count=10):
        self.ip_pool = []
        self.circleRequestIPs(retryTime, min_ip_count)

    def isValidIP(self, address):
        try:
            res = requests.get('https://www.baidu.com', proxies={"http":"http://%s" % address}, timeout=2)
        except Exception as e:
            Logging.warning('proxy ip: %s is invalid...' % address)
            return False
        else:
            if res.status_code == 200:
                Logging.info('proxy ip: %s is valid...' % address)
                return True
            else:
                return False

    # 获取IP池
    def getIPs(self):
        return self.ip_pool

# tool = IPProxyTool()
# tool.refresh(10, 10)
# [Logging.info(ip) for ip in tool.getIPs()]