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
from scipy.misc import imread  # import imageio, imread -> imageio.imread
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import warnings
from collections import defaultdict
import spider_anime
import analysis_barrage_anime
import emotion_analysis

warnings.filterwarnings('ignore')


class BiliSpider:
    def __init__(self, URL):
        # 判断地址类型，1-番剧，2-视频
        if "video" in URL:
            VideoType = "2"
            see = re.compile(r'BV(.*)\?')
            result = see.search(URL)
            if result:
                Name = result.group()
                Name = re.sub(r'\?', "", Name)
            else:
                see = re.compile(r'BV(.*)')
                Name = see.search(URL).group()
        elif "bangumi" in URL:
            VideoType = "1"
            see = re.compile(r'play/(.*)')
            Name = see.search(URL).group()
            Name = re.sub(r'play/', "", Name)
        else:
            print("视频地址无效，请重新输入")
            sys.exit()
        Name = re.sub(r' ', "", Name)
        # 构造要爬取的视频url地址
        self.BV = Name
        self.VideoType = VideoType
        self.BVurl = re.sub(r' ', "", URL)
        # self.headers = {
        #     "User-Agent": "Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Mobile Safari/537.36"}

        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)',
                        'Cookie': 'LIVE_BUVID=AUTO7215383727315695; stardustvideo=1; rpdid=kwxwwoiokwdoskqkmlspw; '
                                  'fts=1540348439; sid=alz55zmj; CURRENT_FNVAL=16; _uuid=08E6859E-EB68-A6B3-5394-65272461BC6E49706infoc; '
                                  'im_notify_type_64915445=0; UM_distinctid=1673553ca94c37-0491294d1a7e36-36664c08-144000-1673553ca956ac; '
                                  'DedeUserID=64915445; DedeUserID__ckMd5=cc0f686b911c9f2d; SESSDATA=7af19f78%2C1545711896%2Cb812f4b1; '
                                  'bili_jct=dc9a675a0d53e8761351d4fb763922d5; BANGUMI_SS_5852_REC=103088; '
                                  'buvid3=AE1D37C0-553C-445A-9979-70927B6C493785514infoc; finger=edc6ecda; CURRENT_QUALITY=80; '
                                  'bp_t_offset_64915445=199482032395569793; _dfcaptcha=44f6fd1eadc58f99515d2981faadba86'}

    # 弹幕都是在一个url请求中，该url请求在视频url的js脚本中构造
    def getXml_url(self):
        # 获取该视频网页的内容
        try:
            response = requests.get(self.BVurl, headers=self.headers, timeout=10)
        except requests.exceptions.ConnectionError as e:
            print("请求失败请重试")
            sys.exit()
        html_str = response.content.decode()

        # 保存获取到的网页源码
        # html_name = "./BilibiliHtmls/" + self.BV + "_bilibili.html"
        # fileOb = open(html_name, 'w', encoding='utf-8')
        # fileOb.write(html_str)
        # fileOb.close()
        # 使用正则找出该弹幕编号cid:36482143（属于抽取web数据的第一种方法字符串匹配）
        # 拼装弹幕请求地址:'//api.bilibili.com/x/v1/dm/list.so?oid=36482143'
        # 使用re匹配出的是地址中的弹幕请求参数名，即 36482143
        # getWord_url = re.findall("api.bilibili.com/x/v1/dm/list.so\?oid=(\d+)", html_str)

        cid_num = re.compile(r'"cid":\d+')
        num = cid_num.search(html_str)
        if num:
            num=num.group()
            cid_num = re.compile(r'\d+')
            num = cid_num.search(num).group()
            print("弹幕的编号是：" + num)
        else:
            print("未获取到弹幕编号，请重试！")
            sys.exit()
        # 组装成要请求的xml地址
        xml_url = "https://api.bilibili.com/x/v1/dm/list.so?oid={}".format(num)
        return xml_url

    # Xpath不能解析指明编码格式的字符串，所以此处我们不解码，还是二进制文本
    def parse_url(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
        except requests.exceptions.ConnectionError as e:
            print("请求失败请重试")
            sys.exit()
        return response.content

    # 弹幕包含在xml中的<d></d>中，使用lxml中的etree解析xml获取弹幕文本（属于抽取web数据的第二种方法通过DOM结构处理）
    def save_print_word(self, str):
        html = etree.HTML(str)
        word_list = html.xpath("//d/text()")
        txt_name = "./BilibiliBarrageFiles/" + self.BV + "_bilibili.txt"
        fileOb = open(txt_name, 'w', encoding='utf-8')
        for word in word_list:
            fileOb.write(word)
        fileOb.close()
        # 控制台输出弹幕
        for word in word_list:
            print(word)
        return word_list

    # 解析xml
    def parseXml(self):
        text_all = ''''''
        xml_name = "./BilibiliBarrageXmls/" + self.BV + "_bilibili.xml"
        tree = ET.parse(xml_name)
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
        xml_name = "./BilibiliBarrageXmls/" + self.BV + "_bilibili.xml"
        fileOb = open(xml_name, 'w', encoding='utf-8')
        fileOb.write(xml_str)
        fileOb.close()

    # 绘制词云
    def draw_word_picture(self, text_all):
        # 设置文字颜色以及字体
        word_color = imread('./StyleLibrary/backColor.jpg')
        font = './StyleLibrary/Tensentype-DouDouJ.ttf'
        # 获取WordCloud对象
        wc = WordCloud(background_color='white',
                       max_words=1000,
                       mask=word_color,
                       font_path=font,
                       random_state=15)
        # jieba分词，形成有空格的字符串
        word_list = []
        stop_words = set(line.strip() for line in open('./WordLibrary/baidu_stopwords.txt', encoding='utf - 8'))
        word_generator = jieba.cut(text_all, cut_all=False)
        for word in word_generator:
            if word not in stop_words:
                word_list.append(word)
        text = ' '.join(word_list)
        wc.generate(text)
        plt.figure(figsize=(20, 10))
        plt.axis('off')
        plt.imshow(wc)
        # 保存词云
        wordcloud_name = "./WordCloudPictures/" + self.BV + "_wordcloud.jpg"
        plt.savefig(wordcloud_name)
        plt.show()

    def getCid_list(self):
        # 获取该视频网页的内容
        try:
            response = requests.get(self.BVurl, headers=self.headers, timeout=10)
        except requests.exceptions.ConnectionError as e:
            print("请求失败请重试")
            sys.exit()
        html_str = response.content.decode()
        cid_num = re.compile(r'"cid":\d\d+')
        cid_list = cid_num.findall(html_str)
        for i in range(len(cid_list)):
            cid_list[i] = re.sub(r'"cid":', "", cid_list[i])
        cid_list = [int(x) for x in cid_list]
        del cid_list[len(cid_list) - 1]
        return cid_list
    def draw_picture(self,score_df):
        # score_df.plot()
        score_df.plot(kind='hist', color='c')
        plt.ylabel('')
        plt.xlabel('Sentiment score')
        plt.xlim(-6, 6)
        plt.grid(True, linestyle='--')
        results_name = "./AnalysisResults/" + self.BV + "_analysis_result.jpg"
        plt.savefig(results_name)
        plt.show()

    def run(self):
        # 视频弹幕处理逻辑BV
        if self.VideoType == "2":
            # 1.根据BV号获取视频页源码解析出弹幕的地址
            start_url = self.getXml_url()
            # 2.请求弹幕地址获取包含弹幕的xml文件
            xml_bytes = self.parse_url(start_url)
            # 3.在本地保存视频弹幕的xml文件
            self.write_file(xml_bytes)
            # 4.解析xml文件，获取弹幕文本
            text_all = self.parseXml()
            # 5.绘制词云
            self.draw_word_picture(text_all)
            # 6.情感分析
            score=emotion_analysis.emotional_analysis(text_all)
            # 7.绘情感得分图
            self.draw_picture(score)
            # 8.本地保存弹幕文本，控制台输出弹幕
            word_list = self.save_print_word(xml_bytes)
        # 番剧弹幕处理逻辑
        elif self.VideoType == "1":
            # 1.根据番剧地址获取所有话的cid
            cid_list = self.getCid_list()
            # 2.根据cid获取所有话的弹幕文件保存为csv
            spider_anime.main(cid_list)
            # 3.进行统计数值分析输出图表
            analysis_barrage_anime.main(len(cid_list))


if __name__ == '__main__':
    URL = input("请输入视频地址:")
    spider = BiliSpider(URL)
    spider.run()
