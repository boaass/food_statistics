# -*- coding:utf-8 -*-
import requests
import json
from Logging import Logging

class IPProxyTool(object):

    def __init__(self):
        self.ip_pool = []

    def requestIPs(self):
        # 讯代理
        res = requests.get('http://www.xdaili.cn/ipagent//freeip/getFreeIps?page=1&rows=10', timeout=3)
        try:
            res_dict = json.loads(res.text)
            for ip_dict in res_dict['rows']:
                address = (ip_dict['ip']+':'+ip_dict['port']).encode('u8')
                self.ip_pool.append(address) if self.isValidIP(address) else None
        except Exception as e:
            Logging.error(e.message)
            self.ip_pool = []

    def circleRequestIPs(self, retryTime):
        if retryTime == 0 or len(self.ip_pool)>5:
            return
        self.requestIPs()

        return self.circleRequestIPs(retryTime-1)

    def refresh(self):
        self.circleRequestIPs(5)

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
# tool.refresh()
# [Logging.info(ip) for ip in tool.getIPs()]