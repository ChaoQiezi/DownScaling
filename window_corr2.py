# @炒茄子  2023-05-19

# 该程序主要用于解决window_corr1中遗留的问题，由于window_corr1中的数据是按照窗口大小进行排列的，因此在绘制箱线图时，需要将数据按照窗口大小进行分组，然后再绘制箱线图。
# 其实主要是为了方便得到excel数据能够在https://hiplot.com.cn/cloud-tool/drawing-tool/detail/178进行绘制
# 该程序的主要思路是：
# 1. 读取excel数据
# 2. 将数据按照窗口大小进行分组
# 3. 输出excel数据
"""
步骤2的具体思路就是，将数据分为三列，第一列存储相关系数，第二列存储该相关系数对应的变量, 第三列存储该相关系数对应的窗口大小
"""
import pandas as pd
import numpy as np

# 读取excel数据
df = pd.read_excel(r'E:\PRCP\table\window_corr\_correlation_matrices.xlsx', sheet_name='年平均相关系数')

# 创建一个空的DataFrame，用于存储数据
df_new = pd.DataFrame(columns=['相关系数', '变量', '窗口大小'])
window_sizes = ['11']
for column_name in df.columns:
    # 提取窗口大小
    window_size = column_name.split('_')[-1]
    if window_size not in window_sizes:
        continue
    # 提取当前所在列的相关系数
    corr = df[column_name].values
    # 剔除无效值
    corr = corr[~np.isnan(corr)]
    # 将数据存储到df_new中
    df_temp = pd.DataFrame({'相关系数': corr, '变量': column_name, '窗口大小': window_size})
    df_new = pd.concat([df_new, df_temp])

# 输出为excel文件
df_new.to_excel(r'E:\PRCP\table\window_corr\correlation_matrices_new.xlsx', index=False)
