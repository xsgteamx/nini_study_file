# =============================================================================
# 6.2.2 Excel等文件的读取和写入 by wyt&xjx
# =============================================================================

# 1.文件读取
# 1.1 读取Excel文件
import pandas as pd
data = pd.read_excel('C:\\Users\\XQ\\Desktop\\配套源代码文件2019-08\\第6章源代码汇总\\data.xlsx')  # data为DataFrame结构,这里设置是相对路径，也可以改成绝对路径
print(data)

# 1.2 读取CSV文件,CSV文件类似Excel文件，不过专门用来存储数据的，所占空间更小
data = pd.read_csv('C:\\Users\\XQ\\Desktop\\配套源代码文件2019-08\\第6章源代码汇总\\data.csv')
print(data)

# 2.文件写入
# 2.1 写入到一个Excel当中
data = pd.DataFrame([[1, 2], [3, 4], [5, 6]], columns=['A列', 'B列'])  # 先生成一个DataFrame
print(data)
data.to_excel('C:\\Users\\XQ\\Desktop\\配套源代码文件2019-08\\第6章源代码汇总\\data_0.xlsx')  # 将DataFrame导入到Excel当中

# 忽略索引信息的写法
data.to_excel('C:\\Users\\XQ\\Desktop\\配套源代码文件2019-08\\第6章源代码汇总\\data_1.xlsx', columns=['A列', 'B列'], index=False)

# 2.2 写入到一个CSV文件当中
data = pd.DataFrame([[1, 2], [3, 4], [5, 6]], columns=['A列', 'B列'])  # 先生成一个DataFrame
data.to_csv('C:\\Users\\XQ\\Desktop\\配套源代码文件2019-08\\第6章源代码汇总\\data_0.csv')  # 将DataFrame导入到CSV文件当中

