# -*- coding: utf-8 -*-
import scrapy
import json
from pinduoduo.items import PinduoduoItem
from copy import deepcopy
from scrapy_redis.spiders import RedisSpider
import re


class PdditemSpider(RedisSpider):
    name = 'pdditem'
    allowed_domains = ['yangkeduo.com']
    page = 1  # 起始页码数
    size = 400  # 单页显示数量（最大400）
    opt_type = 1
    offset = 0  # 偏移量100为一页
    # start_urls = ['http://apiv3.yangkeduo.com/operation/14/groups?page={}&size={}&opt_type={}'.format(page, size,opt_type)]  # 女装商品
    # 'http://apiv3.yangkeduo.com/operation/14/groups?page=1&size=400&opt_type=1'
    redis_key = "pinduoduo"

    def parse(self, response):  # 解析分类页
        goods_list_json = json.loads(response.body)
        url = response.url
        # print(goods_list_json)
        keys = goods_list_json.keys()
        key = list(keys)[2]
        if key == "error_code":  # 请求失败获取到错误json代码，重新请求
            print(key, "再次尝试请求")
            yield scrapy.Request(
                url,
                callback=self.parse,
                dont_filter=True
            )
        else:
            item = PinduoduoItem()
            # goods_list = goods_list_json['goods_list']
            opt_infos = goods_list_json['opt_infos']
            print(opt_infos)
            if opt_infos is not None:
                # item = PinduoduoItem()
                for info in opt_infos:
                    item['opt_id'] = info['id']
                    item['opt_name'] = info['opt_name']
                    print(item)
                    yield scrapy.Request(
                        'http://apiv3.yangkeduo.com/operation/'+ str(item['opt_id'])+ '/groups?offset=0&size=100&opt_type=2',
                        callback=self.parse_good,
                        meta={"item": deepcopy(item)}
                    )

    def parse_good(self, response):  # 解析商品页
        item = response.meta["item"]
        print(item['opt_name'])
        goods_list_json = json.loads(response.body)
        url = response.url
        # print(goods_list_json)
        keys = goods_list_json.keys()
        key = list(keys)[-1]
        # print(key)
        if key == "error_code":
            print(key,"再次尝试请求")
            yield scrapy.Request(
                url,
                callback=self.parse_good,
                meta={"item": deepcopy(item)},  # 大坑！！重新请求需要带上item
                dont_filter=True
            )
        else:
            goods_list = goods_list_json['goods_list']
            # print(goods_list)
            # if goods_list is not None:
                # 判断是否是最后一页
            if not goods_list:
                return
            for each in goods_list:
                # item = PinduoduoItem()
                item['goods_name'] = each['goods_name']
                item['price'] = float(each['group']['price']) / 100  # 拼多多的价格默认多乘了100
                item['sales'] = each['cnt']
                item['normal_price'] = float(each['normal_price']) / 100
                item['goods_id'] = each['goods_id']
                item['link_url'] = 'http://yangkeduo.com/'+ each['link_url']
                # item['mall_name'] = each['mall_name']
                # item['mall_id'] = each['ad']['mall_id']
                print(item)
                yield item
                # yield scrapy.Request(
                #     item['link_url'],
                #     callback=self.get_mall_data, meta={"item": item},)

            self.page += 1
            self.offset = self.page*100  # 构造下一页地址
            yield scrapy.Request(url='http://apiv3.yangkeduo.com/operation/'+ str(item['opt_id'])+ '/groups?offset={}&size=100&opt_type=2'.format(self.offset),
                                 callback=self.parse_good,
                                 meta={"item": item}
                                 )

    def get_mall_data(self, response):  # 获取店铺信息
        item = response.meta["item"]
        Cookie = response.request.headers.getlist('Cookie')
        print(Cookie)
        mall_name = response.xpath("//div[@class='goods-mall-name']/text()").extract_first()
        print('*'*50, mall_name)
        if mall_name is not None:
            item['mall_name'] = mall_name
        data = response.body.decode('utf-8')
        pattern = re.compile(r'mall_id=(.*?)\"', re.S)
        result = re.search(pattern, data)
        # print(result.group(1))
        if result is not None:
            item['mall_id'] = result.group(1)
        else:
            yield scrapy.Request(
                response.url,
                callback=self.get_mall_data,
                meta={"item": item},
                dont_filter=True
            )
        if item['mall_name'] and item['mall_id']:
            print(item)
            yield (item)
        else:
            print('数据获取不全，重新获取')



        # mall_id_json = json.loads(response.body)
        # # print(mall_id_json)
        # if mall_id_json['data'][0] is not None:
        #     item['mall_id'] = mall_id_json['data'][0]['mall_id']

        # url = 'http://yangkeduo.com/mall_page.html?mall_id={}'.format(item['mall_id'])
        # yield scrapy.Request(
        #     url,
        #     callback=self.get_mall_name,
        #     meta={"item": item}
        # )

    # def get_mall_name(self, response):  # 获取店铺名字信息
    #     item = response.meta["item"]
    #     mall_name = response.xpath("//div[@class='mall-title']/span/text()").extract_first()
    #     if mall_name is not None:
    #         item['mall_name'] = mall_name
    #     print(item)
    #     yield item

