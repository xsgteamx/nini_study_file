# 导入包
import talib # 需要解决这个
import numpy as np
import pandas as pd
import tushare as ts
import mplfinance as mpf
import matplotlib.pyplot as plt
# 登录tushare数据接口
pro = ts.pro_api('843a691bbc6634614b03c3233904e9777ced48a72aab4d7cd3e014f7')
# 获取所需的股票数据
df = pro.daily(ts_code="600012.SH", start_date="20230101", fields='trade_date,open,high,low,close,vol')
# 计算ATR指标
ATR = talib.ATR(df['high'], df['low'], df['close'], timeperiod=14)
# 可视化
fig = plt.figure()
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)
# 绘制K线图
mpf.candlestick2_ohlc(ax1, df['open'], df['high'], df['low'], df['close'], width=0.6, colorup='red', colordown='green')
# 绘制ATR曲线
ax2.plot(0, np.mean(ATR))  # 使上下坐标对应
ax2.plot(ATR, label='ATR')
# 显示图像
plt.legend()
plt.savefig("ATR.jpg")
plt.show()
# 计算RSI指标
rsi = talib.RSI(df['close'], timeperiod = 14)
# 可视化
fig = plt.figure()
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)
# 绘制K线图
mpf.candlestick2_ohlc(ax1, df['open'], df['high'], df['low'], df['close'], width=0.6, colorup='red', colordown='green')
# 绘制RSI曲线
ax2.plot(0, np.mean(rsi))  # 使上下坐标对应
ax2.plot(rsi, label='RSI')
# 显示图像
plt.legend()
plt.savefig("RSI.jpg")
plt.show()
# 计算OBV指标
OBV = talib.OBV(df['close'], df['vol'])
# 计算OBV的9日均线
OBV_MA = talib.MA(OBV, timeperiod=9)
# 可视化
fig = plt.figure()
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)
# 绘制K线图
mpf.candlestick2_ohlc(ax1, df['open'], df['high'], df['low'], df['close'], width=0.6, colorup='red', colordown='green')
# 绘制OBV曲线
ax2.plot(OBV, label='OBV')
ax2.plot(OBV_MA, label='OBV_MA9')
# 显示图像
plt.legend()
plt.savefig("OBV.jpg")
plt.show()
# 计算CCI指标
CCI = talib.CCI(df['high'], df['low'], df['close'], timeperiod=14)
# 可视化
fig = plt.figure()
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)
# 绘制K线图
mpf.candlestick2_ohlc(ax1, df['open'], df['high'], df['low'], df['close'], width=0.6, colorup='red', colordown='green')
# 绘制CCI曲线
ax2.plot(0, np.mean(CCI))  # 使上下坐标对应
ax2.plot(CCI, label='CCI')
# 显示图像
plt.legend()
plt.savefig("CCI.jpg")
plt.show()