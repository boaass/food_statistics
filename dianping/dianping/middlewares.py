# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from IPProxyTool import IPProxyTool
from random import choice
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
from Logging import Logging

class DianpingSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    def __init__(self):
        self.ipTool = IPProxyTool()
        super(DianpingSpiderMiddleware, self).__init__()

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).


        for r in start_requests:
            yield r

    def process_request(self, request, spider):
        request.meta['proxy'] = 'http://' + choice(self.ipTool.getIPs()) if len(self.ipTool.getIPs()) != 0 else None
        Logging.debug('{(request_url)%s : (proxy)%s}' % (request.url, request.meta['proxy']))


    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class DianpingSpiderRetryMiddleware(RetryMiddleware):

    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response

        if response.status in self.retry_http_codes:
            Logging.warning('<---------- url:%s retry ---------->')
            reason = response_status_message(response.status)
            request.meta['proxy'] = 'http://' + choice(IPProxyTool().getIPs()) if len(IPProxyTool().getIPs()) != 0 else None
            return self._retry(request, reason, spider) or response

        return response

