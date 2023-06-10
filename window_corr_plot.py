# @炒茄子  2023-05-19

import pandas as pd
import matplotlib.pyplot as plt

# 读取Excel文件
df = pd.read_excel(r'E:\PRCP\table\window_corr\correlation_matrices.xlsx')

# 确定窗口大小的数量（假设每个窗口大小有3列数据：地表温度、NDVI和土壤水分）
num_window_sizes = int(df.shape[1] / 3)

# 为每个窗口大小绘制一个箱线图
for i in range(num_window_sizes):
    # 提取每个窗口大小的相关系数
    window_size_data = df.iloc[:, i * 3:(i + 1) * 3]
    # 获取其中的有效值(np.nan为无效值,需要剔除)
    window_size_data = window_size_data[window_size_data.notnull().all(axis=1)]

    # 创建箱线图
    plt.figure(figsize=(10, 6))
    plt.boxplot(window_size_data.values, notch=True, vert=True)

    # 设置箱线图的标题和坐标轴标签
    plt.title('Boxplot for Window Size ' + str(i + 1))
    plt.xlabel('Variable')
    plt.ylabel('Correlation Coefficient')
    plt.xticks([1, 2, 3], window_size_data.columns)

    # 显示箱线图
    plt.show()

