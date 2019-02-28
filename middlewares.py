# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import logging
from pinduoduo.user_agents import user_agents
import random
import requests


class RandomUserAgentMiddleware():
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.user_agents = user_agents

    def process_request(self, request, spider):
        user_agents = random.choice(self.user_agents)
        request.headers['User-Agent'] = user_agents
        request.headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8'
        request.headers['Host'] = 'yangkeduo.com'
        request.headers['AccessToken'] = 'XGLTR4GHEIFAT34TGF262AC4WEIAQ6MAQHEMESRFMDZPKHBGLSTA102d0c5'
        cookie = {'api_uid': 'rBQh5lwt5tIz5kOSFgGsAg==', '_nano_fp': 'XpdYn5daX59JnqTaXC_yIU_LNQ_M7ShVGMFp9Twc',
                  'msec': '1800000',
                  'pdd_user_uin': 'ZYXPDBINPYLGJO5SOEUSCV6ML4_GEXDA', 'pdd_user_id': '1528432695058',
                  'PDDAccessToken': 'WPKHYTN6D5YYNC6FZIVVAH3TXQ2IYHWF5T35UJVBIEDON56NF47A10312a4',
                  'rec_list_personal': 'rec_list_personal_PukFyh', 'ab': '0', 'gp': '0',
                  'rec_list_index': 'rec_list_index_ZtrfcY',
                  'rec_list_catgoods': 'rec_list_catgoods_NL09Bs', 'sp': '1',
                  'ua': 'Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F70.0.3538.110%20Safari%2F537.36',
                  'webp': '1',
                  'rec_list': 'rec_list_13cfnX', 'goods_detail_mall': 'goods_detail_mall_ehF1Wj'}

        request.cookies = cookie

        # self.logger.debug('使用请求头 ' + user_agents)


class ProxyMiddleware():
    def __init__(self, proxy_url):
        self.logger = logging.getLogger(__name__)
        self.proxy_url = proxy_url
        self.count = 10

    def get_random_proxy(self):
        try:
            response = requests.get(self.proxy_url)
            if response.status_code == 200:
                proxy = response.text
                return proxy
        except requests.ConnectionError:
            return False

    def process_request(self, request, spider):
        self.count -= 1
        if self.count == 0:
            proxy = self.get_random_proxy()
            if proxy:
                uri = 'https://{proxy}'.format(proxy=proxy)
                self.logger.debug('使用代理 ' + uri)
                request.meta['proxy'] = uri
                self.count = 10

        elif request.meta.get('Retrying'):
            self.logger.debug('请求失败 ','*'*50 )
            proxy = self.get_random_proxy()
            if proxy:
                uri = 'https://{proxy}'.format(proxy=proxy)
                self.logger.debug('使用代理 ' + uri)
                request.meta['proxy'] = uri

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            proxy_url=settings.get('PROXY_URL')
        )
