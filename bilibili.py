# coding=utf-8
import requests
from Cython.Shadow import inline
from lxml import etree
import re
import sys
# xml包里进行解析的方法
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import jieba
# scipy中处理图像的函数
from matplotlib import pylab
from scipy.misc import imread
from wordcloud import WordCloud,ImageColorGenerator
import matplotlib.pyplot as plt
#%matplotlib inline
import warnings
from collections import defaultdict

warnings.filterwarnings('ignore')


class BiliSpider:
    def __init__(self, BV):
        # 构造要爬取的视频url地址
        self.BVurl = "https://bilibili.com/video/" + BV
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Mobile Safari/537.36"}

    # 弹幕都是在一个url请求中，该url请求在视频url的js脚本中构造
    def getXml_url(self):
        # 获取该视频网页的内容
        response = requests.get(self.BVurl, headers=self.headers)
        html_str = response.content.decode()
        # 使用正则找出该弹幕地址
        # 格式为:'//api.bilibili.com/x/v1/dm/list.so?oid=36482143'
        # 我们分隔出的是地址中的弹幕请求参数名，即 36482143
        getWord_url = re.findall("api.bilibili.com/x/v1/dm/list.so\?oid=(\d+)", html_str)
        if getWord_url:
            getWord_url = getWord_url[0].replace("'", "")
        else:
            print("未获取到URL，请重试！")
            sys.exit()
        # 组装成要请求的xml地址
        xml_url = "https://api.bilibili.com/x/v1/dm/list.so?oid={}".format(getWord_url)
        return xml_url

    # Xpath不能解析指明编码格式的字符串，所以此处我们不解码，还是二进制文本
    def parse_url(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content

    # 弹幕包含在xml中的<d></d>中，取出即可
    def get_word_list(self, str):
        html = etree.HTML(str)
        word_list = html.xpath("//d/text()")
        return word_list

    # 解析xml
    def parseXml(self, file):
        text_all = ''''''
        tree = ET.parse(file)
        # 获取节点
        root = tree.getroot()
        for child in root:
            if child.tag == 'd':
                text_all = text_all + child.text
        return text_all

    # 写入文件
    def write_file(self, xml_bytes):
        # 将字节流编码
        xml_str = xml_bytes.decode('utf-8')
        # 打开文件，若无则新增
        fileOb = open('bilibili.txt', 'w', encoding='utf-8')
        fileOb.write(xml_str)
        fileOb.close()
    #绘制词云
    def draw_word_picture(self,text_all):
        # 设置文字颜色以及字体
        word_color = imread('backColor.jpg')
        font = 'Tensentype-DouDouJ.ttf'
        # 获取WordCloud对象
        wc = WordCloud(background_color='white',
                       max_words=1000,
                       mask=word_color,
                       font_path=font,
                       random_state=15)
        # jieba分词，形成有空格的字符串
        word_list = []
        word_generator = jieba.cut(text_all, cut_all=False)
        for word in word_generator:
            word_list.append(word)
        text = ' '.join(word_list)
        wc.generate(text)
        plt.figure(figsize=(20, 10))
        plt.axis('off')
        plt.imshow(wc)
        plt.savefig('./bilibili_wordcloud.jpg')
        plt.show()

    def run(self):
        # 1.根据BV号获取弹幕的地址
        start_url = self.getXml_url()
        # 2.请求并解析数据
        xml_bytes = self.parse_url(start_url)
        # 3.将xml写入文件
        self.write_file(xml_bytes)
        # 4.解析xml文件
        text_all = self.parseXml('bilibili.txt')
        # 5.绘制词云
        self.draw_word_picture(text_all)
        # 6.情感分析
        ## 载入停用词，使用的是百度的停用词库
        f = open('baidu_stopwords.txt', encoding='UTF-8')
        stopwords = f.readlines()
        stopwords = [i.replace("\n", "") for i in stopwords]

        ## 载入情感词
        f1 = open("BosonNLP_sentiment_score.txt", encoding='UTF-8')
        senList = f1.readlines()
        senDict = defaultdict()
        for s in senList:
            s = s.replace("\n", "")
            #print(s)
            senDict[s.split(' ')[0]] = float(s.split(' ')[1])

        # 4.弹幕列表
        word_list = self.get_word_list(xml_bytes)
        # 5.控制台打印弹幕
        for word in word_list:
            print(word)


if __name__ == '__main__':
    BVName = input("请输入要爬取的视频的BV号\n"
                   "例如视频地址为https://www.bilibili.com/video/BV1MZ4y1x77S?spm_id_from=333.5.b_6d757369635f6f726967696e616c.33\n"
                   "则输入（也可以包含？后的请求参数）：BV1MZ4y1x77S\n"
                   "好了请输入吧：")
    spider = BiliSpider(BVName)
    spider.run()
