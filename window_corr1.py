# @炒茄子  2023-05-18

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

"""
------------------------------------------------------------
当前程序拓展性差
------------------------------------------------------------
# 注意: 此处使用皮尔逊系数进行相关系数的计算, 但是皮尔逊系数要求数据满足正态分布, 但是实际上很多数据并不满足正态分布, 因此在此处尝试使用斯皮尔曼系数进行相关系数的计算
# 注意: 斯皮尔曼系数要求数据必须是有序的, 即数据具有可比较的大小关系
当前程序用计算不同空间窗口下两两变量之间的相关系数，探索二者之间在空间上是否存在一定的关联。


# 读取年平均降水量和 NDVI 数据、地表温度数据、土壤水分数据
precip_data_year = pd.read_excel(r'E:\PRCP\table\kinds_aver\precipitation_sc_year.xlsx', sheet_name='降水年平均值数据')
ndvi_data_year = pd.read_excel(r'E:\PRCP\table\kinds_aver\ndvi_sc_year.xlsx', sheet_name='NDVI年平均值数据')
temperature_data_year = pd.read_excel(r'E:\PRCP\table\kinds_aver\temperature_sc_year.xlsx', sheet_name='地表温度年平均值数据')
soil_moisture_data_year = pd.read_excel(r'E:\PRCP\table\kinds_aver\soil_moisture_sc_year.xlsx', sheet_name='土壤水分年平均值数据')
# 读取降水量数据和NDVI等数据(不读取地形因子和经纬度列)
_precip_data_year = precip_data_year.iloc[:, 5:]
_ndvi_data_year = ndvi_data_year.iloc[:, 5:]
_temperature_data_year = temperature_data_year.iloc[:, 5:]
_soil_moisture_data_year = soil_moisture_data_year.iloc[:, 5:]
# 创建空的三维数组，用于维度转换后的结果(83, 113, number_of_years)
precip_data_year = np.zeros((83, 113, len(_precip_data_year.columns)), dtype=np.float32)
ndvi_data_year = np.zeros((83, 113, len(_ndvi_data_year.columns)), dtype=np.float32)
temperature_data_year = np.zeros((83, 113, len(_temperature_data_year.columns)), dtype=np.float32)
soil_moisture_data_year = np.zeros((83, 113, len(_soil_moisture_data_year.columns)), dtype=np.float32)
# 将二维数组转换为三维数组
for i in range(len(_precip_data_year.columns)):
    precip_data_year[:, :, i] = _precip_data_year.iloc[:, i].values.reshape(83, 113)
    ndvi_data_year[:, :, i] = _ndvi_data_year.iloc[:, i].values.reshape(83, 113)
    temperature_data_year[:, :, i] = _temperature_data_year.iloc[:, i].values.reshape(83, 113)
    soil_moisture_data_year[:, :, i] = _soil_moisture_data_year.iloc[:, i].values.reshape(83, 113)

# 窗口大小列表
window_sizes = [5, 7, 9, 11, 13, 15, 17, 19, 21]
# 初始化相关系数DataFrame
correlation_dict = {}

for window_size in window_sizes:
    # 初始化相关系数矩阵(np.nan初始化)
    correlation_matrix = np.zeros((precip_data_year.shape[0], precip_data_year.shape[1], 3), dtype=np.float32)
    correlation_matrix[:] = np.nan

    # 对于每个窗口，计算斯皮尔曼相关系数
    for i in range(precip_data_year.shape[0] - window_size):
        for j in range(precip_data_year.shape[1] - window_size):
            # 提取窗口中的数据
            window_precipitation = precip_data_year[i:i + window_size, j:j + window_size, :]
            window_ndvi = ndvi_data_year[i:i + window_size, j:j + window_size, :]
            window_temperature = temperature_data_year[i:i + window_size, j:j + window_size, :]
            window_soil_moisture = soil_moisture_data_year[i:i + window_size, j:j + window_size, :]

            # 在窗口中的每个像素上计算相关系数
            corr_per_pixel = np.zeros((window_size, window_size, 3), dtype=np.float32)
            for k in range(window_size):
                for l in range(window_size):
                    corr_per_pixel[k, l, 0], _ = spearmanr(window_precipitation[k, l, :], window_ndvi[k, l, :])
                    corr_per_pixel[k, l, 1], _ = spearmanr(window_precipitation[k, l, :], window_temperature[k, l, :])
                    corr_per_pixel[k, l, 2], _ = spearmanr(window_precipitation[k, l, :], window_soil_moisture[k, l, :])

            # 计算窗口内的平均相关系数
            correlation_matrix[i, j, 0] = np.mean(corr_per_pixel[:, :, 0])
            correlation_matrix[i, j, 1] = np.mean(corr_per_pixel[:, :, 1])
            correlation_matrix[i, j, 2] = np.mean(corr_per_pixel[:, :, 2])

    # 将相关系数矩阵添加到correlation_matrices中
    correlation_dict['precipitation_ndvi_' + str(window_size)] = pd.Series(
        correlation_matrix[:, :, 0][~np.isnan(correlation_matrix[:, :, 0])].flatten())
    correlation_dict['precipitation_temperature_' + str(window_size)] = pd.Series(
        correlation_matrix[:, :, 1][~np.isnan(correlation_matrix[:, :, 1])].flatten())
    correlation_dict['precipitation_soil_moisture_' + str(window_size)] = pd.Series(
        correlation_matrix[:, :, 2][~np.isnan(correlation_matrix[:, :, 2])].flatten())

# 将相关系数矩阵保存到Excel文件中
df = pd.concat(correlation_dict, axis=1)
df.to_excel(r'E:\PRCP\table\window_corr\correlation_matrices.xlsx', index=False, sheet_name='年平均相关系数')
"""


# 将上述内容写成函数形式
def window_corr(data1, data2, window_sizes, data1_name='X', data2_name='Y'):
    # 过滤地形因子和经纬度列
    _data1 = data1.iloc[:, 5:]
    _data2 = data2.iloc[:, 5:]

    # 创建空的三维数组，用于维度转换后的结果(83, 113, number_of_years)
    data1 = np.zeros((83, 113, len(_data1.columns)), dtype=np.float32)
    data2 = np.zeros((83, 113, len(_data2.columns)), dtype=np.float32)

    # 存储相关系数的字典
    correlation_dict = {}

    # 将二维数组转换为三维数组
    for date in range(len(_data1.columns)):
        data1[:, :, date] = _data1.iloc[:, date].values.reshape(83, 113)
        data2[:, :, date] = _data2.iloc[:, date].values.reshape(83, 113)

    for window_size in window_sizes:
        # 初始化相关系数矩阵(np.nan初始化)
        correlation_matrix = np.zeros((data1.shape[0], data1.shape[1]), dtype=np.float32)
        correlation_matrix[:] = np.nan  # 将矩阵中的所有元素设置为np.nan

        # 对于每个窗口，计算斯皮尔曼相关系数
        for i in range(data1.shape[0] - window_size):
            for j in range(data1.shape[1] - window_size):
                # 提取窗口中的数据
                window_data1 = data1[i:i + window_size, j:j + window_size, :]
                window_data2 = data2[i:i + window_size, j:j + window_size, :]

                # 在窗口中的每个像素上计算相关系数
                corr_per_pixel = np.zeros((window_size, window_size), dtype=np.float32)
                for k in range(window_size):
                    for l in range(window_size):
                        corr_per_pixel[k, l], _ = spearmanr(window_data1[k, l, :], window_data2[k, l, :])

                # 计算窗口内的平均相关系数
                correlation_matrix[i, j] = np.mean(corr_per_pixel[:, :])

        # 将相关系数矩阵存储到字典中
        correlation_dict[data1_name + '_' + data2_name + '_' + str(window_size)] = pd.Series(
            correlation_matrix[~np.isnan(correlation_matrix)].flatten())

    return correlation_dict


# 读取年平均降水量和 NDVI 数据、地表温度数据、土壤水分数据
precip_data_year = pd.read_excel(r'E:\PRCP\table\kinds_aver\precipitation_sc_year.xlsx', sheet_name='降水年平均值数据')
ndvi_data_year = pd.read_excel(r'E:\PRCP\table\kinds_aver\ndvi_sc_year.xlsx', sheet_name='NDVI年平均值数据')
temperature_data_year = pd.read_excel(r'E:\PRCP\table\kinds_aver\temperature_sc_year.xlsx', sheet_name='地表温度年平均值数据')
soil_moisture_data_year = pd.read_excel(r'E:\PRCP\table\kinds_aver\soil_moisture_sc_year.xlsx', sheet_name='土壤水分年平均值数据')
# # 读取月平均降水量和 NDVI 数据、地表温度数据、土壤水分数据
# precip_data_month = pd.read_excel(r'E:\PRCP\table\kinds_aver\precipitation_sc_month.xlsx', sheet_name='降水月平均值数据')
# ndvi_data_month = pd.read_excel(r'E:\PRCP\table\kinds_aver\ndvi_sc_month.xlsx', sheet_name='NDVI月平均值数据')
# temp_data_month = pd.read_excel(r'E:\PRCP\table\kinds_aver\temperature_sc_month.xlsx', sheet_name='地表温度月平均值数据')
# soil_moisture_data_month = pd.read_excel(r'E:\PRCP\table\kinds_aver\soil_moisture_sc_month.xlsx',
#                                          sheet_name='土壤水分月平均值数据')
# # 读取季节平均降水量和 NDVI 数据、地表温度数据、土壤水分数据
# precip_data_season = pd.read_excel(r'E:\PRCP\table\kinds_aver\precipitation_sc_season.xlsx', sheet_name='降水季平均值数据')
# ndvi_data_season = pd.read_excel(r'E:\PRCP\table\kinds_aver\ndvi_sc_season.xlsx', sheet_name='NDVI季平均值数据')
# temp_data_season = pd.read_excel(r'E:\PRCP\table\kinds_aver\temperature_sc_season.xlsx', sheet_name='地表温度季平均值数据')
# soil_moisture_data_season = pd.read_excel(r'E:\PRCP\table\kinds_aver\soil_moisture_sc_season.xlsx',
#                                           sheet_name='土壤水分季平均值数据')
# # 读取年季平均降水量和 NDVI 数据、地表温度数据、土壤水分数据
# precip_data_year_season = pd.read_excel(r'E:\PRCP\table\kinds_aver\precipitation_sc_year_season.xlsx',
#                                         sheet_name='降水年季平均值数据')
# ndvi_data_year_season = pd.read_excel(r'E:\PRCP\table\kinds_aver\ndvi_sc_year_season.xlsx', sheet_name='NDVI年季平均值数据')
# temp_data_year_season = pd.read_excel(r'E:\PRCP\table\kinds_aver\temperature_sc_year_season.xlsx',
#                                       sheet_name='地表温度年季平均值数据')
# soil_moisture_data_year_season = pd.read_excel(r'E:\PRCP\table\kinds_aver\soil_moisture_sc_year_season.xlsx',
#                                                sheet_name='土壤水分年季平均值数据')
precip_ndvi_year_correlation_dict = window_corr(precip_data_year, ndvi_data_year, [11, 13, 15, 17], 'precipitation',
                                                'ndvi_year')
# precip_ndvi_month_correlation_dict = window_corr(precip_data_month, ndvi_data_month, [11, 13, 15, 17], 'precipitation',
#                                                  'ndvi_month')
# precip_ndvi_season_correlation_dict = window_corr(precip_data_season, ndvi_data_season, [11, 13, 15, 17],
#                                                   'precipitation', 'ndvi_season')
# precip_ndvi_year_season_correlation_dict = window_corr(precip_data_year_season, ndvi_data_year_season, [11, 13, 15, 17],
#                                                        'precipitation', 'ndvi_year_season')
precip_temp_year_correlation_dict = window_corr(precip_data_year, temperature_data_year, [11, 13, 15, 17],
                                                'precipitation', 'temperature_year')
# precip_temp_month_correlation_dict = window_corr(precip_data_month, temp_data_month, [11, 13, 15, 17], 'precipitation',
#                                                  'temperature_month')
# precip_temp_season_correlation_dict = window_corr(precip_data_season, temp_data_season, [11, 13, 15, 17],
#                                                   'precipitation', 'temperature_season')
# precip_temp_year_season_correlation_dict = window_corr(precip_data_year_season, temp_data_year_season, [11, 13, 15, 17],
#                                                        'precipitation', 'temperature_year_season')
precip_soil_moisture_year_correlation_dict = window_corr(precip_data_year, soil_moisture_data_year, [11, 13, 15, 17],
                                                         'precipitation', 'soil_moisture_year')
# precip_soil_moisture_month_correlation_dict = window_corr(precip_data_month, soil_moisture_data_month, [11, 13, 15, 17],
#                                                           'precipitation', 'soil_moisture_month')
# precip_soil_moisture_season_correlation_dict = window_corr(precip_data_season, soil_moisture_data_season,
#                                                            [11, 13, 15, 17],
#                                                            'precipitation', 'soil_moisture_season')
# precip_soil_moisture_year_season_correlation_dict = window_corr(precip_data_year_season, soil_moisture_data_year_season,
#                                                                 [11, 13, 15, 17], 'precipitation',
#                                                                 'soil_moisture_year_season')
correlation_dict = {
    **precip_ndvi_year_correlation_dict,
    # **precip_ndvi_month_correlation_dict,
    # **precip_ndvi_season_correlation_dict,
    # **precip_ndvi_year_season_correlation_dict,
    **precip_temp_year_correlation_dict,
    # **precip_temp_month_correlation_dict,
    # **precip_temp_season_correlation_dict,
    # **precip_temp_year_season_correlation_dict,
    **precip_soil_moisture_year_correlation_dict,
    # **precip_soil_moisture_month_correlation_dict,
    # **precip_soil_moisture_season_correlation_dict,
    # **precip_soil_moisture_year_season_correlation_dict
    }

df = pd.concat(correlation_dict, axis=1)
df.to_excel(r'E:\PRCP\table\window_corr\_correlation_matrices.xlsx', index=False, sheet_name='年平均相关系数')
