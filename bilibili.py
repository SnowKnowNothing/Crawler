# coding=utf-8
import requests
from lxml import etree
import re
class BiliSpider:
    def __init__(self,BV):
        # 构造要爬取的视频url地址
        self.BVurl = "https://bilibili.com/video/"+BV
        self.headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Mobile Safari/537.36"}

    # 弹幕都是在一个url请求中，该url请求在视频url的js脚本中构造
    def getXml_url(self):
        # 获取该视频网页的内容
        response = requests.get(self.BVurl, headers = self.headers)
        html_str = response.content.decode()
        # 使用正则找出该弹幕地址
        # 格式为:'//api.bilibili.com/x/v1/dm/list.so?oid=36482143'
        # 我们分隔出的是地址中的弹幕请求参数名，即 36482143
        getWord_url = re.findall("api.bilibili.com/x/v1/dm/list.so\?oid=(\d+)", html_str)
        getWord_url = getWord_url[0].replace("'","")
        # 组装成要请求的xml地址
        xml_url="https://api.bilibili.com/x/v1/dm/list.so?oid={}".format(getWord_url)
        return xml_url

    # Xpath不能解析指明编码格式的字符串，所以此处我们不解码，还是二进制文本
    def parse_url(self,url):
        response = requests.get(url,headers = self.headers)
        return response.content

    # 弹幕包含在xml中的<d></d>中，取出即可
    def get_word_list(self,str):
        html = etree.HTML(str)
        word_list = html.xpath("//d/text()")
        return word_list

    def run(self):
        # 1.根据BV号获取弹幕的地址
        start_url = self.getXml_url()
        # 2.请求并解析数据
        xml_str = self.parse_url(start_url)
        word_list = self.get_word_list(xml_str)
        # 3.打印
        for word in word_list:
            print(word)

if __name__ == '__main__':
    BVName = input("请输入要爬取的视频的BV号\n"
                   "例如视频地址为https://www.bilibili.com/video/BV1MZ4y1x77S?spm_id_from=333.5.b_6d757369635f6f726967696e616c.33\n"
                   "则输入：BV1MZ4y1x77S?spm_id_from=333.5.b_6d757369635f6f726967696e616c.33\n"
                   "好了来吧：")
    spider = BiliSpider(BVName)
    spider.run()


