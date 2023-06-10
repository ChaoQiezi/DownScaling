# @炒茄子  2023-06-03

"""
当前程序用于绘制降水(目标项)与各个因子项(NDVI、地表温度、土壤水分、地形因子、经纬度)的散点核密度图
"""
import pandas as pd
import seaborn as sns
import numpy as np
from scipy.stats import gaussian_kde
import matplotlib.pyplot as plt

# 读取降水数据
precip_data_year = pd.read_excel(r'E:\PRCP\table\unified_date\precip_topo_sc_monthly.xlsx', sheet_name='降水和地形因子月数据')

# 绘制散点核密度图
# 将宽格式的数据转化为长格式的数据
precip_data_year.drop(columns=['lon', 'lat', 'aspect', 'slope', 'DEM'], inplace=True)
df_melted = precip_data_year.melt(var_name='Time', value_name='Correlation').dropna(axis=0, how='any')
df_melted['Time'] = pd.to_datetime(df_melted['Time'], errors='coerce')  # 如果不能转化为日期型，将其设为NaT

# 绘制散点核密度图
# 获取每个时间段的密度估计值
density = gaussian_kde(df_melted['Correlation'])  # 估计密度函数
df_melted['Density'] = density(df_melted['Correlation'])
# 绘制散点图，颜色由密度决定
sns.scatterplot(x='Time', y='Correlation', hue='Density', palette='viridis', data=df_melted)

# 显示图形
plt.show()
