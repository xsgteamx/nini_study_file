# !/usr/bin/env python
# coding=utf-8
import pandas as pd 
from sklearn import svm, preprocessing
import matplotlib.pyplot as plt 

origDf = pd.read_excel(r'B:\Desktop\files\share.xlsx')
print(origDf.columns)
df = origDf[['close', 'high', 'low', 'open', 'vol', 'trade_date']].copy()
# diff列表示本日和上日收盘价的差
df['diff'] = df["close"]-df["close"].shift(1)
df['diff'].fillna(0, inplace=True)
# up列表示本日是否上涨，1表示涨，0表示跌
df['up'] = df['diff'].apply(lambda x: 1 if x > 0 else 0)
# 预测值暂且初始化为0
df['predictForUp'] = 0

# 目标值是真实的涨跌情况
target = df['up']

length = len(df)
trainNum = int(length*0.8)
predictNum = length-trainNum
# 选择指定列作为特征列
feature = df[['close', 'high', 'low', 'open', 'vol']]
# 标准化处理特征值
feature = preprocessing.scale(feature)

# 训练集的特征值和目标值
featureTrain = feature[0:trainNum]
targetTrain = target[0:trainNum]
svmTool = svm.SVC(kernel='linear')
svmTool.fit(featureTrain, targetTrain)

print(svmTool.score(featureTrain, targetTrain))

predictedIndex = trainNum
# 逐行预测测试集
while predictedIndex < length:
    testFeature = feature[predictedIndex:predictedIndex+1]
    predictForUp = svmTool.predict(testFeature)
    df.loc[predictedIndex, 'predictForUp'] = predictForUp
    predictedIndex += 1