# A Crawler for Bilibili

可以根据视频地址爬取某个视频的弹幕。以及对弹幕做可视化词云和情感分析。

## 准备步骤

除了必要的依赖包，还需要通过命令行安装结巴分词（pip install jieba）
以及词云包（pip install wordcloud）

使用pyecharts0.5.10进行绘图（pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pyecharts==0.5.10）
注意版本，1.0版本及以上不兼容，如已安装高版本先卸载 pip uninstall pyecharts

安装snapshot，下载网址https://pypi.org/project/pyecharts-snapshot/0.1.10/#files
然后在下载文件目录打开命令行执行pip install pyecharts_snapshot-0.1.10-py2.py3-none-any.whl
