# @炒茄子  2023-06-02

"""
该程序用于将数据(降水、NDVI、地表温度、土壤水分)处理成模型训练所需的格式
"""

import pandas as pd
import numpy as np
import os

# 1.1 读取数据
# 读取年平均降水量和 NDVI 数据、地表温度数据、土壤水分数据
precip_data_year = pd.read_excel(r'E:\PRCP\table\kinds_aver\precipitation_sc_year.xlsx', sheet_name='降水年平均值数据')
ndvi_data_year = pd.read_excel(r'E:\PRCP\table\kinds_aver\ndvi_sc_year.xlsx', sheet_name='NDVI年平均值数据')
temperature_data_year = pd.read_excel(r'E:\PRCP\table\kinds_aver\temperature_sc_year.xlsx', sheet_name='地表温度年平均值数据')
soil_moisture_data_year = pd.read_excel(r'E:\PRCP\table\kinds_aver\soil_moisture_sc_year.xlsx', sheet_name='土壤水分年平均值数据')

# 1.2 数据预处理
# 获取地形因子和经纬度列
terrain_factor_columns = ['lon', 'lat', 'DEM', 'slope', 'aspect']
terrain_factor = precip_data_year[terrain_factor_columns]
# 循环每年数据
for year in precip_data_year.columns[~precip_data_year.columns.isin(terrain_factor_columns)]:
    precip_data = precip_data_year[year]
    ndvi_data = ndvi_data_year[year]
    temperature_data = temperature_data_year[year]
    soil_moisture_data = soil_moisture_data_year[year]
    # 1.2.5 合并数据
    # 将年降水、NDVI、地表温度、土壤水分数据合并
    data = pd.concat([precip_data, ndvi_data, temperature_data, soil_moisture_data], axis=1)
    data.columns = [column_name + '_' + year for column_name in ['precip', 'ndvi', 'temperature', 'soil_moisture']]
    # 将经纬度和地形因子与上述数据合并
    data = pd.concat([terrain_factor, data], axis=1)
    # 1.2.6 去除缺失值
    # 去除缺失值-只要有一个特征缺失，就去除该样本
    data.dropna(axis=0, how='any', inplace=True)
    # 将
    # 1.2.7 保存数据
    data.to_excel(r'E:\PRCP\table\model_train_data\\'+year+'.xlsx', index=False, sheet_name=year)

