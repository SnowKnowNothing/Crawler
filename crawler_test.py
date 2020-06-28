#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : crawler_test.py
# @Author: Feng
# @Date  : 2020/6/26
# @Desc  :

import requests
from operator import itemgetter
from bilibili import BiliSpider


if __name__ == '__main__':
    try:
        url = 'https://s.search.bilibili.com/cate/search?main_ver=v3&search_type=video&view_type=hot_rank&order=dm&copy_right=-1&cate_id=21&page=1&pagesize=20&jsonp=jsonp&time_from=20200619&time_to=20200626&_=1593140806247'
        word_freq = dict()
        word_list = list()
        resp = requests.get(url)
        if resp.status_code != 200:
            print(resp.status_code)
        resp_json = resp.json()
        if resp_json['code'] != 0:
            print('no result')
        else:
            print(resp_json['msg'])
        result_list = resp_json.get('result', [])
        for item in result_list:
            if item.get('tag', None) is None:
                continue
            # 统计标签词频
            tag_list = item['tag'].split(',')
            for tag in tag_list:
                word_freq[tag] = 1 if word_freq.get(tag, 0) == 0 else word_freq[tag] + 1
            #
            spider = BiliSpider(item['bvid'], item['type'])
            print(spider.getXml_url())
        word_freq = sorted(word_freq.items(),key=itemgetter(1), reverse=True)
        # 统计值大于1的加入词频列表
        for item in word_freq:
            if item[1] > 1:
                word_list.append({'name': item[0], 'count': item[1]})
    except Exception as e:
        print(str(e))