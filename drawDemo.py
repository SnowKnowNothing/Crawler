#导入柱状图-Bar
import pyecharts
def draw_01():
    #设置行名
    columns = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    #设置数据
    data1 = [2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3]
    data2 = [2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3]
    #设置柱状图的主标题与副标题
    #bar = Bar("柱状图", "一年的降水量与蒸发量")
    context={"柱状图":"一年的降水量与蒸发量"}
    bar = pyecharts.Bar(context)
    #添加柱状图的数据及配置项
    bar.add("降水量", columns, data1, )
    bar.add("蒸发量", columns, data2, mark_line=["average"], mark_point=["max", "min"])
    #生成本地文件（默认为.html文件）
    bar.render()

def draw_02():
    bar = pyecharts.Bar("贵州GDP柱状图", "副标题")
    bar.add("GDP", ["贵阳市", "遵义市", "六盘水市", "安顺市", "黔东南州"], [40, 30, 26, 22, 15])
    bar.show_config()
    bar.render()

if __name__=="__main__":
    draw_01()