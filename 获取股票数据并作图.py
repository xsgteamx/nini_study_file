
# 获取000002的股票数据
# 一、引进相关的库
# 1.各种库
import pandas as pd
import numpy as np
from pylab import *  # * 代表所有，就是从pylab中导入所有的非私有类，函数，全局变量等
import matplotlib.pyplot as plt  # 绘制图形的库
import tushare as ts
import matplotlib.ticker as ticker  # 修改横轴的密度的库

# 2.使中文能正确显示、使坐标轴的负号显示出来
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 二、利用tushare库获取000002指定时间的股票数据
# df = ts.get_hist_data('000002', start='2020-10-01', end='2020-11-02')
df = ts.get_hist_data('600202')
# pd.set_option('display.max_columns', None)
df = df.reset_index()  # 使日期也变成一列数据，方便后续图形的制作
print(df)

# 三、做收盘价的折线图，以日期作为横轴，收盘价作为纵轴，颜色为红色、标签为收盘价、横轴的刻度旋转45度，图例置于右上角
fig = plt.figure(figsize=(20, 5))  # 整个图表的大小
ax = fig.add_subplot(111)  # 第一个子图
plt.plot(df['date'], df['close'], color='red', label='收盘价')
plt.xticks(rotation=45)
plt.legend(loc='upper right')
tick_spacing = 180  # 通过修改tick_spacing的值可以修改x轴的密度
ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
plt.title('收盘价的折线图')
plt.grid()  # 加网格线
plt.show()

# 四、做收盘价的箱线图
df.boxplot(column='volume')
# df.plot.box('volume')
plt.xlabel("横轴", fontsize=16)  # 横轴的名称
plt.ylabel('纵轴', fontsize=16)
plt.grid(linestyle="--", alpha=0.8)
print(df.describe())  # 显示中位数、上下四分位数、标准偏差等内容
plt.show()













