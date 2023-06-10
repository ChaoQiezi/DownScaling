# @炒茄子  2023-04-05
import pandas as pd
from bin.func import *

"""说明
1. 本脚本用于计算各种时间序列的均值, 包括: 月均值、季节均值、年均值、年季均值
2. 本脚本用到的数据包括: 降水数据、NDVI数据、地表温度数据, 注意不包含土地利用数据(因为其仅有年尺度数据无需进行均值运算)
"""


# 02 整理数据
# 2.2 进行各种时间序列的均值计算
print("2.2 正在进行时间序列的均值计算······")
# 读取降水数据、NDVI、地表温度数据
precipitation_data = pd.read_excel(r"E:\PRCP\table\unified_date\precip_topo_sc_monthly.xlsx", sheet_name="降水和地形因子月数据")
ndvi_data = pd.read_excel(r"E:\PRCP\table\unified_date\NDVI_topo_sc_monthly.xlsx", sheet_name="NDVI和地形因子月数据")
temperature_data = pd.read_excel(r"E:\PRCP\table\unified_date\temp_topo_sc_monthly.xlsx", sheet_name="地表温度和地形因子月数据")
soil_moisture_data = pd.read_excel(r"E:\PRCP\table\unified_date\soil_moisture_topo_sc_monthly.xlsx", sheet_name="土壤水分和地形因子月数据")
# 2.2.1 年均值 ==> 每一年的平均值计算
# 降水数据的年平均值计算
# 在最开头新建一行
precipitation_data = pd.concat(
    [pd.DataFrame(np.nan, index=['year'], columns=precipitation_data.columns), precipitation_data], axis=0)
# 获取year行的数据
for i in range(precipitation_data.shape[1]):
    if (precipitation_data.columns[i]).startswith('20'):
        precipitation_data.loc['year', precipitation_data.columns[i]] = precipitation_data.columns[i][:4]
# 计算月降水数据的年平均值
precipitation_data_year = precipitation_data.T.groupby('year').mean().T
precipitation_data_year.columns.name = None  # 去掉列名的name
# 为年平均值添加经纬度信息、DEM、slope、aspect数据
precipitation_data_year.insert(0, 'lon', precipitation_data['lon'])
precipitation_data_year.insert(1, 'lat', precipitation_data['lat'])
precipitation_data_year.insert(2, 'DEM', precipitation_data['DEM'])
precipitation_data_year.insert(3, 'slope', precipitation_data['slope'])
precipitation_data_year.insert(4, 'aspect', precipitation_data['aspect'])
precipitation_data.drop('year', axis=0, inplace=True)  # 删除year行, 为了方便后续其它类型的均值计算时好继续使用该降水数据
# NDVI数据的年平均值计算
# 在最开头新建一行
ndvi_data = pd.concat([pd.DataFrame(np.nan, index=['year'], columns=ndvi_data.columns), ndvi_data])
# 获取year行的数据
for i in range(ndvi_data.shape[1]):
    if (ndvi_data.columns[i]).startswith('20'):
        ndvi_data.loc['year', ndvi_data.columns[i]] = ndvi_data.columns[i][:4]
# 计算月NDVI数据的年平均值
ndvi_data_year = ndvi_data.T.groupby('year').mean().T
ndvi_data_year.columns.name = None  # 去掉列名的name
# 为年平均值添加经纬度信息、DEM、slope、aspect数据
ndvi_data_year.insert(0, 'lon', ndvi_data['lon'])
ndvi_data_year.insert(1, 'lat', ndvi_data['lat'])
ndvi_data_year.insert(2, 'DEM', ndvi_data['DEM'])
ndvi_data_year.insert(3, 'slope', ndvi_data['slope'])
ndvi_data_year.insert(4, 'aspect', ndvi_data['aspect'])
ndvi_data.drop('year', axis=0, inplace=True)  # 删除year行, 为了方便后续其它类型的均值计算时好继续使用该NDVI数据
# 地表温度数据的年平均值计算
# 在最开头新建一行
temperature_data = pd.concat([pd.DataFrame(np.nan, index=['year'], columns=temperature_data.columns), temperature_data])
# 获取year行的数据
for i in range(temperature_data.shape[1]):
    if (temperature_data.columns[i]).startswith('20'):
        temperature_data.loc['year', temperature_data.columns[i]] = temperature_data.columns[i][:4]
# 计算月地表温度数据的年平均值
temperature_data_year = temperature_data.T.groupby('year').mean().T
temperature_data_year.columns.name = None  # 去掉列名的name
# 为年平均值添加经纬度信息、DEM、slope、aspect数据
temperature_data_year.insert(0, 'lon', temperature_data['lon'])
temperature_data_year.insert(1, 'lat', temperature_data['lat'])
temperature_data_year.insert(2, 'DEM', temperature_data['DEM'])
temperature_data_year.insert(3, 'slope', temperature_data['slope'])
temperature_data_year.insert(4, 'aspect', temperature_data['aspect'])
temperature_data.drop('year', axis=0, inplace=True)  # 删除year行, 为了方便后续其它类型的均值计算时好继续使用该地表温度数据
# 土壤水分数据的年平均值计算
# 在最开头新建一行
soil_moisture_data = pd.concat(
    [pd.DataFrame(np.nan, index=['year'], columns=soil_moisture_data.columns), soil_moisture_data])
# 获取year行的数据
for i in range(soil_moisture_data.shape[1]):
    if (soil_moisture_data.columns[i]).startswith('20'):
        soil_moisture_data.loc['year', soil_moisture_data.columns[i]] = soil_moisture_data.columns[i][:4]
# 计算月土壤水分数据的年平均值
soil_moisture_data_year = soil_moisture_data.T.groupby('year').mean().T
soil_moisture_data_year.columns.name = None  # 去掉列名的name
# 为年平均值添加经纬度信息、DEM、slope、aspect数据
soil_moisture_data_year.insert(0, 'lon', soil_moisture_data['lon'])
soil_moisture_data_year.insert(1, 'lat', soil_moisture_data['lat'])
soil_moisture_data_year.insert(2, 'DEM', soil_moisture_data['DEM'])
soil_moisture_data_year.insert(3, 'slope', soil_moisture_data['slope'])
soil_moisture_data_year.insert(4, 'aspect', soil_moisture_data['aspect'])
soil_moisture_data.drop('year', axis=0, inplace=True)  # 删除year行, 为了方便后续其它类型的均值计算时好继续使用该土壤水分数据

# 2.2.2 季均值 ==> 每一季度的平均值计算
# 降水数据的季平均值计算
# 在最开头新建一行
precipitation_data = pd.concat(
    [pd.DataFrame(np.nan, index=['season'], columns=precipitation_data.columns), precipitation_data])
# 获取season行的数据
season_index = {'01': 'DJF', '02': 'DJF', '03': 'MAM', '04': 'MAM', '05': 'MAM', '06': 'JJA', '07': 'JJA', '08': 'JJA',
                '09': 'SON', '10': 'SON', '11': 'SON', '12': 'DJF'}
"""DJF: 01 02 12 MAM: 03 04 05  JJA: 06 07 08  SON: 09 10 11"""
for i in range(precipitation_data.shape[1]):
    if (precipitation_data.columns[i]).startswith('20'):
        precipitation_data.loc['season', precipitation_data.columns[i]] = season_index[
            precipitation_data.columns[i][4:6]]
# 计算月降水数据的季平均值
precipitation_data_season = precipitation_data.T.groupby('season').mean().T
precipitation_data_season.columns.name = None  # 去掉列名的name
# 为季平均值添加经纬度信息、DEM、slope、aspect数据
precipitation_data_season.insert(0, 'lon', precipitation_data['lon'])
precipitation_data_season.insert(1, 'lat', precipitation_data['lat'])
precipitation_data_season.insert(2, 'DEM', precipitation_data['DEM'])
precipitation_data_season.insert(3, 'slope', precipitation_data['slope'])
precipitation_data_season.insert(4, 'aspect', precipitation_data['aspect'])
precipitation_data.drop('season', axis=0, inplace=True)  # 删除season行, 为了方便后续其它类型的均值计算时好继续使用该降水数据
# NDVI数据的季平均值计算
# 在最开头新建一行
ndvi_data = pd.concat([pd.DataFrame(np.nan, index=['season'], columns=ndvi_data.columns), ndvi_data])
# 获取season行的数据
for i in range(ndvi_data.shape[1]):
    if (ndvi_data.columns[i]).startswith('20'):
        ndvi_data.loc['season', ndvi_data.columns[i]] = season_index[ndvi_data.columns[i][4:6]]
# 计算月NDVI数据的季平均值
ndvi_data_season = ndvi_data.T.groupby('season').mean().T
ndvi_data_season.columns.name = None  # 去掉列名的name
# 为季平均值添加经纬度信息、DEM、slope、aspect数据
ndvi_data_season.insert(0, 'lon', ndvi_data['lon'])
ndvi_data_season.insert(1, 'lat', ndvi_data['lat'])
ndvi_data_season.insert(2, 'DEM', ndvi_data['DEM'])
ndvi_data_season.insert(3, 'slope', ndvi_data['slope'])
ndvi_data_season.insert(4, 'aspect', ndvi_data['aspect'])
ndvi_data.drop('season', axis=0, inplace=True)  # 删除season行, 为了方便后续其它类型的均值计算时好继续使用该NDVI数据
# 地表温度数据的季平均值计算
# 在最开头新建一行
temperature_data = pd.concat(
    [pd.DataFrame(np.nan, index=['season'], columns=temperature_data.columns), temperature_data])
# 获取season行的数据
for i in range(temperature_data.shape[1]):
    if (temperature_data.columns[i]).startswith('20'):
        temperature_data.loc['season', temperature_data.columns[i]] = season_index[temperature_data.columns[i][4:6]]
# 计算月地表温度数据的季平均值
temperature_data_season = temperature_data.T.groupby('season').mean().T
temperature_data_season.columns.name = None  # 去掉列名的name
# 为季平均值添加经纬度信息、DEM、slope、aspect数据
temperature_data_season.insert(0, 'lon', temperature_data['lon'])
temperature_data_season.insert(1, 'lat', temperature_data['lat'])
temperature_data_season.insert(2, 'DEM', temperature_data['DEM'])
temperature_data_season.insert(3, 'slope', temperature_data['slope'])
temperature_data_season.insert(4, 'aspect', temperature_data['aspect'])
temperature_data.drop('season', axis=0, inplace=True)  # 删除season行, 为了方便后续其它类型的均值计算时好继续使用该地表温度数据
# 土壤水分数据的季平均值计算
# 在最开头新建一行
soil_moisture_data = pd.concat(
    [pd.DataFrame(np.nan, index=['season'], columns=soil_moisture_data.columns), soil_moisture_data])
# 获取season行的数据
for i in range(soil_moisture_data.shape[1]):
    if (soil_moisture_data.columns[i]).startswith('20'):
        soil_moisture_data.loc['season', soil_moisture_data.columns[i]] = season_index[
            soil_moisture_data.columns[i][4:6]]
# 计算月土壤水分数据的季平均值
soil_moisture_data_season = soil_moisture_data.T.groupby('season').mean().T
soil_moisture_data_season.columns.name = None  # 去掉列名的name
# 为季平均值添加经纬度信息、DEM、slope、aspect数据
soil_moisture_data_season.insert(0, 'lon', soil_moisture_data['lon'])
soil_moisture_data_season.insert(1, 'lat', soil_moisture_data['lat'])
soil_moisture_data_season.insert(2, 'DEM', soil_moisture_data['DEM'])
soil_moisture_data_season.insert(3, 'slope', soil_moisture_data['slope'])
soil_moisture_data_season.insert(4, 'aspect', soil_moisture_data['aspect'])
soil_moisture_data.drop('season', axis=0, inplace=True)  # 删除season行, 为了方便后续其它类型的均值计算时好继续使用该土壤水分数据

# 2.2.3 年季均值 ==> 每一年的每一季度的平均值计算
# 降水数据的年季平均值计算
# 在最开头新建一行
precipitation_data = pd.concat(
    [pd.DataFrame(np.nan, index=['year_season'], columns=precipitation_data.columns), precipitation_data])
# 获取year_season行的数据
for i in range(precipitation_data.shape[1]):
    if (precipitation_data.columns[i]).startswith('20'):
        precipitation_data.loc['year_season', precipitation_data.columns[i]] = precipitation_data.columns[i][:4] + '_' + \
                                                                               season_index[
                                                                                   precipitation_data.columns[i][4:6]]
# 计算月降水数据的年季平均值
precipitation_data_year_season = precipitation_data.T.groupby('year_season').mean().T
precipitation_data_year_season.columns.name = None  # 去掉列名的name
# 为年季平均值添加经纬度信息、DEM、slope、aspect数据
precipitation_data_year_season.insert(0, 'lon', precipitation_data['lon'])
precipitation_data_year_season.insert(1, 'lat', precipitation_data['lat'])
precipitation_data_year_season.insert(2, 'DEM', precipitation_data['DEM'])
precipitation_data_year_season.insert(3, 'slope', precipitation_data['slope'])
precipitation_data_year_season.insert(4, 'aspect', precipitation_data['aspect'])
precipitation_data.drop('year_season', axis=0, inplace=True)  # 删除year_season行, 为了方便后续其它类型的均值计算时好继续使用该降水数据
# NDVI数据的年季平均值计算
# 在最开头新建一行
ndvi_data = pd.concat([pd.DataFrame(np.nan, index=['year_season'], columns=ndvi_data.columns), ndvi_data])
# 获取year_season行的数据
for i in range(ndvi_data.shape[1]):
    if (ndvi_data.columns[i]).startswith('20'):
        ndvi_data.loc['year_season', ndvi_data.columns[i]] = ndvi_data.columns[i][:4] + '_' + season_index[
            ndvi_data.columns[i][4:6]]
# 计算月NDVI数据的年季平均值
ndvi_data_year_season = ndvi_data.T.groupby('year_season').mean().T
ndvi_data_year_season.columns.name = None  # 去掉列名的name
# 为年季平均值添加经纬度信息、DEM、slope、aspect数据
ndvi_data_year_season.insert(0, 'lon', ndvi_data['lon'])
ndvi_data_year_season.insert(1, 'lat', ndvi_data['lat'])
ndvi_data_year_season.insert(2, 'DEM', ndvi_data['DEM'])
ndvi_data_year_season.insert(3, 'slope', ndvi_data['slope'])
ndvi_data_year_season.insert(4, 'aspect', ndvi_data['aspect'])
ndvi_data.drop('year_season', axis=0, inplace=True)  # 删除year_season行, 为了方便后续其它类型的均值计算时好继续使用该NDVI数据
# 地表温度数据的年季平均值计算
# 在最开头新建一行
temperature_data = pd.concat(
    [pd.DataFrame(np.nan, index=['year_season'], columns=temperature_data.columns), temperature_data])
# 获取year_season行的数据
for i in range(temperature_data.shape[1]):
    if (temperature_data.columns[i]).startswith('20'):
        temperature_data.loc['year_season', temperature_data.columns[i]] = temperature_data.columns[i][:4] + '_' + \
                                                                           season_index[
                                                                               temperature_data.columns[i][4:6]]
# 计算月地表温度数据的年季平均值
temperature_data_year_season = temperature_data.T.groupby('year_season').mean().T
temperature_data_year_season.columns.name = None  # 去掉列名的name
# 为年季平均值添加经纬度信息、DEM、slope、aspect数据
temperature_data_year_season.insert(0, 'lon', temperature_data['lon'])
temperature_data_year_season.insert(1, 'lat', temperature_data['lat'])
temperature_data_year_season.insert(2, 'DEM', temperature_data['DEM'])
temperature_data_year_season.insert(3, 'slope', temperature_data['slope'])
temperature_data_year_season.insert(4, 'aspect', temperature_data['aspect'])
temperature_data.drop('year_season', axis=0, inplace=True)  # 删除year_season行, 为了方便后续其它类型的均值计算时好继续使用该地表温度数据
# 土壤水分数据的年季平均值计算
# 在最开头新建一行
soil_moisture_data = pd.concat(
    [pd.DataFrame(np.nan, index=['year_season'], columns=soil_moisture_data.columns), soil_moisture_data])
# 获取year_season行的数据
for i in range(soil_moisture_data.shape[1]):
    if (soil_moisture_data.columns[i]).startswith('20'):
        soil_moisture_data.loc['year_season', soil_moisture_data.columns[i]] = soil_moisture_data.columns[i][:4] + '_' + \
                                                                               season_index[
                                                                                   soil_moisture_data.columns[i][4:6]]
# 计算月土壤水分数据的年季平均值
soil_moisture_data_year_season = soil_moisture_data.T.groupby('year_season').mean().T
soil_moisture_data_year_season.columns.name = None  # 去掉列名的name
# 为年季平均值添加经纬度信息、DEM、slope、aspect数据
soil_moisture_data_year_season.insert(0, 'lon', soil_moisture_data['lon'])
soil_moisture_data_year_season.insert(1, 'lat', soil_moisture_data['lat'])
soil_moisture_data_year_season.insert(2, 'DEM', soil_moisture_data['DEM'])
soil_moisture_data_year_season.insert(3, 'slope', soil_moisture_data['slope'])
soil_moisture_data_year_season.insert(4, 'aspect', soil_moisture_data['aspect'])
soil_moisture_data.drop('year_season', axis=0, inplace=True)  # 删除year_season行, 为了方便后续其它类型的均值计算时好继续使用该土壤水分数据

# 2.2.4 月均值 ==> 每一个月份所有年份的平均值计算
# 降水数据的月平均值计算
# 在最开头新建一行
precipitation_data = pd.concat(
    [pd.DataFrame(np.nan, index=['month'], columns=precipitation_data.columns), precipitation_data])
# 获取month行的数据
for i in range(precipitation_data.shape[1]):
    if (precipitation_data.columns[i]).startswith('20'):
        precipitation_data.loc['month', precipitation_data.columns[i]] = precipitation_data.columns[i][4:6]
# 计算月降水数据的月平均值
precipitation_data_month = precipitation_data.T.groupby('month').mean().T
precipitation_data_month.columns.name = None  # 去掉列名的name
# 为月平均值添加经纬度信息、DEM、slope、aspect数据
precipitation_data_month.insert(0, 'lon', precipitation_data['lon'])
precipitation_data_month.insert(1, 'lat', precipitation_data['lat'])
precipitation_data_month.insert(2, 'DEM', precipitation_data['DEM'])
precipitation_data_month.insert(3, 'slope', precipitation_data['slope'])
precipitation_data_month.insert(4, 'aspect', precipitation_data['aspect'])
precipitation_data.drop('month', axis=0, inplace=True)  # 删除month行, 为了方便后续其它类型的均值计算时好继续使用该降水数据
# NDVI数据的月平均值计算
# 在最开头新建一行
ndvi_data = pd.concat([pd.DataFrame(np.nan, index=['month'], columns=ndvi_data.columns), ndvi_data])
# 获取month行的数据
for i in range(ndvi_data.shape[1]):
    if (ndvi_data.columns[i]).startswith('20'):
        ndvi_data.loc['month', ndvi_data.columns[i]] = ndvi_data.columns[i][4:6]
# 计算月NDVI数据的月平均值
ndvi_data_month = ndvi_data.T.groupby('month').mean().T
ndvi_data_month.columns.name = None  # 去掉列名的name
# 为月平均值添加经纬度信息、DEM、slope、aspect数据
ndvi_data_month.insert(0, 'lon', ndvi_data['lon'])
ndvi_data_month.insert(1, 'lat', ndvi_data['lat'])
ndvi_data_month.insert(2, 'DEM', ndvi_data['DEM'])
ndvi_data_month.insert(3, 'slope', ndvi_data['slope'])
ndvi_data_month.insert(4, 'aspect', ndvi_data['aspect'])
ndvi_data.drop('month', axis=0, inplace=True)  # 删除month行, 为了方便后续其它类型的均值计算时好继续使用该NDVI数据
# 地表温度数据的月平均值计算
# 在最开头新建一行
temperature_data = pd.concat(
    [pd.DataFrame(np.nan, index=['month'], columns=temperature_data.columns), temperature_data])
# 获取month行的数据
for i in range(temperature_data.shape[1]):
    if (temperature_data.columns[i]).startswith('20'):
        temperature_data.loc['month', temperature_data.columns[i]] = temperature_data.columns[i][4:6]
# 计算月地表温度数据的月平均值
temperature_data_month = temperature_data.T.groupby('month').mean().T
temperature_data_month.columns.name = None  # 去掉列名的name
# 为月平均值添加经纬度信息、DEM、slope、aspect数据
temperature_data_month.insert(0, 'lon', temperature_data['lon'])
temperature_data_month.insert(1, 'lat', temperature_data['lat'])
temperature_data_month.insert(2, 'DEM', temperature_data['DEM'])
temperature_data_month.insert(3, 'slope', temperature_data['slope'])
temperature_data_month.insert(4, 'aspect', temperature_data['aspect'])
temperature_data.drop('month', axis=0, inplace=True)  # 删除month行, 为了方便后续其它类型的均值计算时好继续使用该地表温度数据
# 土壤水分数据的月平均值计算
# 在最开头新建一行
soil_moisture_data = pd.concat(
    [pd.DataFrame(np.nan, index=['month'], columns=soil_moisture_data.columns), soil_moisture_data])
# 获取month行的数据
for i in range(soil_moisture_data.shape[1]):
    if (soil_moisture_data.columns[i]).startswith('20'):
        soil_moisture_data.loc['month', soil_moisture_data.columns[i]] = soil_moisture_data.columns[i][4:6]
# 计算月土壤水分数据的月平均值
soil_moisture_data_month = soil_moisture_data.T.groupby('month').mean().T
soil_moisture_data_month.columns.name = None  # 去掉列名的name
# 为月平均值添加经纬度信息、DEM、slope、aspect数据
soil_moisture_data_month.insert(0, 'lon', soil_moisture_data['lon'])
soil_moisture_data_month.insert(1, 'lat', soil_moisture_data['lat'])
soil_moisture_data_month.insert(2, 'DEM', soil_moisture_data['DEM'])
soil_moisture_data_month.insert(3, 'slope', soil_moisture_data['slope'])
soil_moisture_data_month.insert(4, 'aspect', soil_moisture_data['aspect'])
soil_moisture_data.drop('month', axis=0, inplace=True)  # 删除month行, 为了方便后续其它类型的均值计算时好继续使用该土壤水分数据

# 2.2.5 保存数据(转化为excel数据)
# 保存年平均值数据
precipitation_data_year.to_excel(r'E:\PRCP\table\kinds_aver\precipitation_sc_year.xlsx', sheet_name='降水年平均值数据',
                                 index=False, header=True)
ndvi_data_year.to_excel(r'E:\PRCP\table\kinds_aver\ndvi_sc_year.xlsx', sheet_name='NDVI年平均值数据', index=False,
                        header=True)
temperature_data_year.to_excel(r'E:\PRCP\table\kinds_aver\temperature_sc_year.xlsx', sheet_name='地表温度年平均值数据',
                               index=False, header=True)
soil_moisture_data_year.to_excel(r'E:\PRCP\table\kinds_aver\soil_moisture_sc_year.xlsx', sheet_name='土壤水分年平均值数据',
                                    index=False, header=True)
# 保存季平均值数据
precipitation_data_season.to_excel(r'E:\PRCP\table\kinds_aver\precipitation_sc_season.xlsx', sheet_name='降水季平均值数据',
                                   index=False, header=True)
ndvi_data_season.to_excel(r'E:\PRCP\table\kinds_aver\ndvi_sc_season.xlsx', sheet_name='NDVI季平均值数据', index=False,
                          header=True)
temperature_data_season.to_excel(r'E:\PRCP\table\kinds_aver\temperature_sc_season.xlsx', sheet_name='地表温度季平均值数据',
                                 index=False, header=True)
soil_moisture_data_season.to_excel(r'E:\PRCP\table\kinds_aver\soil_moisture_sc_season.xlsx', sheet_name='土壤水分季平均值数据',
                                      index=False, header=True)
# 保存年季平均值数据
precipitation_data_year_season.to_excel(r'E:\PRCP\table\kinds_aver\precipitation_sc_year_season.xlsx',
                                        sheet_name='降水年季平均值数据', index=False, header=True)
ndvi_data_year_season.to_excel(r'E:\PRCP\table\kinds_aver\ndvi_sc_year_season.xlsx', sheet_name='NDVI年季平均值数据',
                               index=False, header=True)
temperature_data_year_season.to_excel(r'E:\PRCP\table\kinds_aver\temperature_sc_year_season.xlsx',
                                      sheet_name='地表温度年季平均值数据', index=False, header=True)
soil_moisture_data_year_season.to_excel(r'E:\PRCP\table\kinds_aver\soil_moisture_sc_year_season.xlsx',
                                            sheet_name='土壤水分年季平均值数据', index=False, header=True)
# 保存月平均值数据
precipitation_data_month.to_excel(r'E:\PRCP\table\kinds_aver\precipitation_sc_month.xlsx', sheet_name='降水月平均值数据',
                                  index=False, header=True)
ndvi_data_month.to_excel(r'E:\PRCP\table\kinds_aver\ndvi_sc_month.xlsx', sheet_name='NDVI月平均值数据', index=False,
                         header=True)
temperature_data_month.to_excel(r'E:\PRCP\table\kinds_aver\temperature_sc_month.xlsx', sheet_name='地表温度月平均值数据',
                                index=False, header=True)
soil_moisture_data_month.to_excel(r'E:\PRCP\table\kinds_aver\soil_moisture_sc_month.xlsx', sheet_name='土壤水分月平均值数据',
                                        index=False, header=True)

r"""此处为了后续操作方便，将土地利用数据复制一份, 将放置到E:\PRCP\table\kinds_aver\landuse_sc_year.xlsx"""
# 读取土地利用数据
landuse_data = pd.read_excel(r'E:\PRCP\table\unified_date\landuse_topo_sc_yearly.xlsx', sheet_name='土地利用和地形因子年数据')
# 保存土地利用数据
landuse_data.to_excel(r'E:\PRCP\table\kinds_aver\landuse_sc_year.xlsx', sheet_name='土地利用和地形因子年数据', index=False, header=True)
print('均值数据保存完毕！')
# 2.2 End
