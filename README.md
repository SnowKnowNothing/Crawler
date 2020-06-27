# A Crawler for Bilibili

可以根据视频地址爬取某个视频的弹幕。以及对弹幕做可视化词云和情感分析。

## 准备步骤

除了必要的依赖包，还需要通过命令行安装结巴分词（pip install jieba）
以及词云包（pip install wordcloud）

使用pyecharts0.5.10进行绘图（pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pyecharts==0.5.10）
注意版本，1.0版本及以上不兼容，如已安装高版本先卸载 pip uninstall pyecharts

安装snapshot，下载网址https://pypi.org/project/pyecharts-snapshot/0.1.10/#files
然后在下载文件目录打开命令行执行pip install pyecharts_snapshot-0.1.10-py2.py3-none-any.whl

## 目录说明
### 文件夹
AnalysisResult用于保存情感分析的图片结果

AnimeBarrageFiles用于以csv的格式分话保存一个番剧的弹幕

BilibiliBarrageFile用于保存解析后单个视频的弹幕文本

BilibiliBarrageXmls用于保存下载的单个视频弹幕的xml文件

StyleLibrary用于保存样式文件

WorldCloudPictures用于保存单个视频文件的词云

WordLibrary用于保存情感分析使用的词库

### 文件
bilibili.py主程序源码

spider_anime.py番剧弹幕下载处理源码

analysis_barrage_anime.py番剧弹幕统计分析可视化输出源码

drawDemo.py画图工具测试

*.html可视化图表输出，浏览器打开
