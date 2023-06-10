# @炒茄子  2023-04-09
import pandas as pd
from bin.func import *

# 03 统计分析
# 3.1 相关性分析
print('正在进行相关性分析······')
# 3.1.1 读取数据和基本处理
# 读取年平均降水数据
precip_data_year = pd.read_excel(r'E:\PRCP\table\kinds_aver\precipitation_sc_year.xlsx', sheet_name='降水年平均值数据')
# 读取年平均NDVI数据
ndvi_data_year = pd.read_excel(r'E:\PRCP\table\kinds_aver\ndvi_sc_year.xlsx', sheet_name='NDVI年平均值数据')
# 读取年平均地表温度数据
temp_data_year = pd.read_excel(r'E:\PRCP\table\kinds_aver\temperature_sc_year.xlsx', sheet_name='地表温度年平均值数据')
# 读取土地利用数据
landuse_data_year = pd.read_excel(r'E:\PRCP\table\kinds_aver\landuse_sc_year.xlsx', sheet_name='土地利用和地形因子年数据')
# 读取年平均土壤水分数据
soil_moisture_data_year = pd.read_excel(r'E:\PRCP\table\kinds_aver\soil_moisture_sc_year.xlsx', sheet_name='土壤水分年平均值数据')
# 使用map将data_list中每一类数据的缺失值替换为np.nan
precip_data_year, ndvi_data_year, temp_data_year, landuse_data_year, soil_moisture_data_year = map(
    replace_nodata_value_with_nan,
    [precip_data_year, ndvi_data_year,
     temp_data_year, landuse_data_year,
     soil_moisture_data_year])
# 读取月平均降水数据
precip_data_month = pd.read_excel(r'E:\PRCP\table\kinds_aver\precipitation_sc_month.xlsx', sheet_name='降水月平均值数据')
# 读取月平均NDVI数据
ndvi_data_month = pd.read_excel(r'E:\PRCP\table\kinds_aver\ndvi_sc_month.xlsx', sheet_name='NDVI月平均值数据')
# 读取月平均地表温度数据
temp_data_month = pd.read_excel(r'E:\PRCP\table\kinds_aver\temperature_sc_month.xlsx', sheet_name='地表温度月平均值数据')
# 读取月平均土壤水分数据
soil_moisture_data_month = pd.read_excel(r'E:\PRCP\table\kinds_aver\soil_moisture_sc_month.xlsx',
                                         sheet_name='土壤水分月平均值数据')
# 使用map将data_list中每一类数据的缺失值替换为np.nan
precip_data_month, ndvi_data_month, temp_data_month, soil_moisture_data_month = map(replace_nodata_value_with_nan,
                                                                                    [precip_data_month, ndvi_data_month,
                                                                                     temp_data_month,
                                                                                     soil_moisture_data_month])
# 读取季平均降水数据
precip_data_season = pd.read_excel(r'E:\PRCP\table\kinds_aver\precipitation_sc_season.xlsx', sheet_name='降水季平均值数据')
# 读取季平均NDVI数据
ndvi_data_season = pd.read_excel(r'E:\PRCP\table\kinds_aver\ndvi_sc_season.xlsx', sheet_name='NDVI季平均值数据')
# 读取季平均地表温度数据
temp_data_season = pd.read_excel(r'E:\PRCP\table\kinds_aver\temperature_sc_season.xlsx', sheet_name='地表温度季平均值数据')
# 读取季平均土壤水分数据
soil_moisture_data_season = pd.read_excel(r'E:\PRCP\table\kinds_aver\soil_moisture_sc_season.xlsx',
                                          sheet_name='土壤水分季平均值数据')
# 使用map将data_list中每一类数据的缺失值替换为np.nan
precip_data_season, ndvi_data_season, temp_data_season, soil_moisture_data_season = map(replace_nodata_value_with_nan,
                                                                                        [precip_data_season,
                                                                                         ndvi_data_season,
                                                                                         temp_data_season,
                                                                                         soil_moisture_data_season])
# 读取年季平均降水数据
precip_data_year_season = pd.read_excel(r'E:\PRCP\table\kinds_aver\precipitation_sc_year_season.xlsx',
                                        sheet_name='降水年季平均值数据')
# 读取年季平均NDVI数据
ndvi_data_year_season = pd.read_excel(r'E:\PRCP\table\kinds_aver\ndvi_sc_year_season.xlsx', sheet_name='NDVI年季平均值数据')
# 读取年季平均地表温度数据
temp_data_year_season = pd.read_excel(r'E:\PRCP\table\kinds_aver\temperature_sc_year_season.xlsx',
                                      sheet_name='地表温度年季平均值数据')
# 读取年季平均土壤水分数据
soil_moisture_data_year_season = pd.read_excel(r'E:\PRCP\table\kinds_aver\soil_moisture_sc_year_season.xlsx',
                                               sheet_name='土壤水分年季平均值数据')
# 使用map将data_list中每一类数据的缺失值替换为np.nan
precip_data_year_season, ndvi_data_year_season, temp_data_year_season, soil_moisture_data_year_season = map(
    replace_nodata_value_with_nan,
    [precip_data_year_season,
     ndvi_data_year_season,
     temp_data_year_season,
     soil_moisture_data_year_season])

"""
数据说明:
年平均降水数据的列索引:lon	lat	DEM	slope	aspect	2001	2002	2003	2004	2005	2006	2007	2008	2009	2010	2011	2012	2013	2014	2015,
年平均NDVI数据的列索引:lon	lat	DEM	slope	aspect	2001	2002	2003	2004	2005	2006	2007	2008	2009	2010	2011	2012	2013	2014	2015
年平均地表温度的列索引:lon	lat	DEM	slope	aspect	2001	2002	2003	2004	2005	2006	2007	2008	2009	2010	2011	2012	2013	2014	2015
年平均土地利用的列索引:lon	lat	DEM	slope	aspect	2001	2002	2003	2004	2005	2006	2007	2008	2009	2010	2011	2012	2013	2014	2015
在上述所有数据中，每一行表示四川省某一像元点的因子变量数据和各个年份的降水数据
相关性分析的基本思路:
# 统计分析3.1.2
对于每一个像元点(即每一行)，均有2001~2015年的年平均值降水数据和年平均值NDVI数据，那么我们可以计算出每一像元点2001~2015年的相关系数,并将这些相关系数存储在一个列表中
对于每一个像元点(即每一行)，均有2001~2015值降水数据和年平均值地表温度数据，那么我们可以计算出每一像元点2001~2015年的相关系数,并将这些相关系数存储在一个列表中
最后，将这些列表全部放在一个矩阵中，即可得到一个相关系数矩阵

------------------------------------------------------------------------------------------------------------------------
---------------上述说明已经过时，因为数据发生了变化，主要是在日期方面以及新数据的添加例如土壤水分，后续还会有数据添加。------------------
------------------------------------------------------------------------------------------------------------------------
"""
# 3.1.2 计算相关系数矩阵
# 创建一个DataFrame数据结构用于存储相关系数矩阵
corr_list = pd.DataFrame()
# 3.1.2.1 计算年尺度的相关系数矩阵
# 计算年平均降水数据和年平均NDVI数据的相关系数矩阵
corr_precip_ndvi, p_precip_ndvi = corr_matrix(precip_data_year, ndvi_data_year)
# 计算年平均降水数据和年平均地表温度数据的相关系数矩阵
corr_precip_temp, p_precip_temp = corr_matrix(precip_data_year, temp_data_year)
# 计算年平均降水数据和年土地利用数据的相关系数矩阵
corr_precip_landuse, p_precip_landuse = corr_matrix(precip_data_year, landuse_data_year)
# 计算年平均降水数据和年土壤水分数据的相关系数矩阵
corr_precip_soil_moisture, p_precip_soil_moisture = corr_matrix(precip_data_year, soil_moisture_data_year)
# 将相关系数矩阵添加到列表中
corr_list['corr_precip_ndvi_year'] = corr_precip_ndvi
corr_list['p_precip_ndvi_year'] = p_precip_ndvi
corr_list['corr_precip_temp_year'] = corr_precip_temp
corr_list['p_precip_temp_year'] = p_precip_temp
corr_list['corr_precip_landuse_year'] = corr_precip_landuse
corr_list['p_precip_landuse_year'] = p_precip_landuse
corr_list['corr_precip_soil_moisture_year'] = corr_precip_soil_moisture
corr_list['p_precip_soil_moisture_year'] = p_precip_soil_moisture
# 3.1.2.2 计算月尺度的相关系数矩阵
# 计算月平均降水数据和月平均NDVI数据的相关系数矩阵
corr_precip_ndvi, p_precip_ndvi = corr_matrix(precip_data_month, ndvi_data_month)
# 计算月平均降水数据和月平均地表温度数据的相关系数矩阵
corr_precip_temp, p_precip_temp = corr_matrix(precip_data_month, temp_data_month)
# 计算月平均降水数据与月平均土壤水分数据的相关系数矩阵(后续相关矩阵<如季均值年均值等>的计算均不会涉及土地利用数据,因为其只有年尺度的数据)
corr_precip_soil_moisture, p_precip_soil_moisture = corr_matrix(precip_data_month, soil_moisture_data_month)
# 将相关系数矩阵添加到列表中
corr_list['corr_precip_ndvi_month'] = corr_precip_ndvi
corr_list['p_precip_ndvi_month'] = p_precip_ndvi
corr_list['corr_precip_temp_month'] = corr_precip_temp
corr_list['p_precip_temp_month'] = p_precip_temp
corr_list['corr_precip_soil_moisture_month'] = corr_precip_soil_moisture
corr_list['p_precip_soil_moisture_month'] = p_precip_soil_moisture
# 3.1.2.3 计算季尺度的相关系数矩阵
# 计算季平均降水数据和季平均NDVI数据的相关系数矩阵
corr_precip_ndvi, p_precip_ndvi = corr_matrix(precip_data_season, ndvi_data_season)
# 计算季平均降水数据和季平均地表温度数据的相关系数矩阵
corr_precip_temp, p_precip_temp = corr_matrix(precip_data_season, temp_data_season)
# 计算季平均降水数据和季平均土壤水分数据的相关系数矩阵
corr_precip_soil_moisture, p_precip_soil_moisture = corr_matrix(precip_data_season, soil_moisture_data_season)
# 将相关系数矩阵添加到列表中
corr_list['corr_precip_ndvi_season'] = corr_precip_ndvi
corr_list['p_precip_ndvi_season'] = p_precip_ndvi
corr_list['corr_precip_temp_season'] = corr_precip_temp
corr_list['p_precip_temp_season'] = p_precip_temp
corr_list['corr_precip_soil_moisture_season'] = corr_precip_soil_moisture
corr_list['p_precip_soil_moisture_season'] = p_precip_soil_moisture
# 3.1.2.4 计算年季尺度的相关系数矩阵
# 计算年季平均降水数据和年季平均NDVI数据的相关系数矩阵
corr_precip_ndvi, p_precip_ndvi = corr_matrix(precip_data_year_season, ndvi_data_year_season)
# 计算年季平均降水数据和年季平均地表温度数据的相关系数矩阵
corr_precip_temp, p_precip_temp = corr_matrix(precip_data_year_season, temp_data_year_season)
# 计算年季平均降水数据和年季平均土壤水分数据的相关系数矩阵
corr_precip_soil_moisture, p_precip_soil_moisture = corr_matrix(precip_data_year_season, soil_moisture_data_year_season)
# 将相关系数矩阵添加到列表中
corr_list['corr_precip_ndvi_year_season'] = corr_precip_ndvi
corr_list['p_precip_ndvi_year_season'] = p_precip_ndvi
corr_list['corr_precip_temp_year_season'] = corr_precip_temp
corr_list['p_precip_temp_year_season'] = p_precip_temp
corr_list['corr_precip_soil_moisture_year_season'] = corr_precip_soil_moisture
corr_list['p_precip_soil_moisture_year_season'] = p_precip_soil_moisture

# 3.1.3 相关系数和P值处理
# 基于P值对相关系数,只保留P值小于0.05的相关系数,其余的相关系数赋值为np.nan
p_value = 0.05
# 年尺度的p值处理
corr_list['corr_precip_ndvi_year'] = corr_list['corr_precip_ndvi_year'].where(corr_list['p_precip_ndvi_year'] < p_value)
corr_list['corr_precip_temp_year'] = corr_list['corr_precip_temp_year'].where(corr_list['p_precip_temp_year'] < p_value)
corr_list['corr_precip_landuse_year'] = corr_list['corr_precip_landuse_year'].where(
    corr_list['p_precip_landuse_year'] < p_value)
corr_list['corr_precip_soil_moisture_year'] = corr_list['corr_precip_soil_moisture_year'].where(
    corr_list['p_precip_soil_moisture_year'] < p_value)
# 月尺度的p值处理
corr_list['corr_precip_ndvi_month'] = corr_list['corr_precip_ndvi_month'].where(
    corr_list['p_precip_ndvi_month'] < p_value)
corr_list['corr_precip_temp_month'] = corr_list['corr_precip_temp_month'].where(
    corr_list['p_precip_temp_month'] < p_value)
corr_list['corr_precip_soil_moisture_month'] = corr_list['corr_precip_soil_moisture_month'].where(
    corr_list['p_precip_soil_moisture_month'] < p_value)
# 季尺度的p值处理
corr_list['corr_precip_ndvi_season'] = corr_list['corr_precip_ndvi_season'].where(
    corr_list['p_precip_ndvi_season'] < p_value)
corr_list['corr_precip_temp_season'] = corr_list['corr_precip_temp_season'].where(
    corr_list['p_precip_temp_season'] < p_value)
corr_list['corr_precip_soil_moisture_season'] = corr_list['corr_precip_soil_moisture_season'].where(
    corr_list['p_precip_soil_moisture_season'] < p_value)
# 年季尺度的p值处理
corr_list['corr_precip_ndvi_year_season'] = corr_list['corr_precip_ndvi_year_season'].where(
    corr_list['p_precip_ndvi_year_season'] < p_value)
corr_list['corr_precip_temp_year_season'] = corr_list['corr_precip_temp_year_season'].where(
    corr_list['p_precip_temp_year_season'] < p_value)
corr_list['corr_precip_soil_moisture_year_season'] = corr_list['corr_precip_soil_moisture_year_season'].where(
    corr_list['p_precip_soil_moisture_year_season'] < p_value)
# 将相关系数矩阵中的每一列转化为二维数组(113行83列共计9379个元素)
# 年尺度的二维转一维处理
corr_precip_ndvi_year = corr_list['corr_precip_ndvi_year'].values.reshape(83, 113)
corr_precip_temp_year = corr_list['corr_precip_temp_year'].values.reshape(83, 113)
corr_precip_landuse_year = corr_list['corr_precip_landuse_year'].values.reshape(83, 113)
corr_precip_soil_moisture_year = corr_list['corr_precip_soil_moisture_year'].values.reshape(83, 113)
# 月尺度的二维转一维处理
corr_precip_ndvi_month = corr_list['corr_precip_ndvi_month'].values.reshape(83, 113)
corr_precip_temp_month = corr_list['corr_precip_temp_month'].values.reshape(83, 113)
corr_precip_soil_moisture_month = corr_list['corr_precip_soil_moisture_month'].values.reshape(83, 113)
# 季尺度的二维转一维处理
corr_precip_ndvi_season = corr_list['corr_precip_ndvi_season'].values.reshape(83, 113)
corr_precip_temp_season = corr_list['corr_precip_temp_season'].values.reshape(83, 113)
corr_precip_soil_moisture_season = corr_list['corr_precip_soil_moisture_season'].values.reshape(83, 113)
# 年季尺度的二维转一维处理
corr_precip_ndvi_year_season = corr_list['corr_precip_ndvi_year_season'].values.reshape(83, 113)
corr_precip_temp_year_season = corr_list['corr_precip_temp_year_season'].values.reshape(83, 113)
corr_precip_soil_moisture_year_season = corr_list['corr_precip_soil_moisture_year_season'].values.reshape(83, 113)

# 将每一个相关系数数组输出为tif文件
# 模板tiff文件路径
template_tif_path = r'E:\PRCP\PRCP_monthly_GPM_SC\200006.tif'
# 将相关系数数组输出为tif文件
write_tiff(corr_precip_ndvi_year, r'E:\PRCP\Statistical_chart\corr_precip_ndvi_year.tif', template_tif_path)
write_tiff(corr_precip_temp_year, r'E:\PRCP\Statistical_chart\corr_precip_temp_year.tif', template_tif_path)
write_tiff(corr_precip_landuse_year, r'E:\PRCP\Statistical_chart\corr_precip_landuse_year.tif', template_tif_path)
write_tiff(corr_precip_ndvi_month, r'E:\PRCP\Statistical_chart\corr_precip_ndvi_month.tif', template_tif_path)
write_tiff(corr_precip_temp_month, r'E:\PRCP\Statistical_chart\corr_precip_temp_month.tif', template_tif_path)
write_tiff(corr_precip_ndvi_season, r'E:\PRCP\Statistical_chart\corr_precip_ndvi_season.tif', template_tif_path)
write_tiff(corr_precip_temp_season, r'E:\PRCP\Statistical_chart\corr_precip_temp_season.tif', template_tif_path)
write_tiff(corr_precip_ndvi_year_season, r'E:\PRCP\Statistical_chart\corr_precip_ndvi_year_season.tif',
           template_tif_path)
write_tiff(corr_precip_temp_year_season, r'E:\PRCP\Statistical_chart\corr_precip_temp_year_season.tif',
           template_tif_path)
write_tiff(corr_precip_soil_moisture_year, r'E:\PRCP\Statistical_chart\corr_precip_soil_moisture_year.tif',
           template_tif_path)
write_tiff(corr_precip_soil_moisture_month, r'E:\PRCP\Statistical_chart\corr_precip_soil_moisture_month.tif',
           template_tif_path)
write_tiff(corr_precip_soil_moisture_season, r'E:\PRCP\Statistical_chart\corr_precip_soil_moisture_season.tif',
           template_tif_path)
write_tiff(corr_precip_soil_moisture_year_season,
           r'E:\PRCP\Statistical_chart\corr_precip_soil_moisture_year_season.tif',
           template_tif_path)

# 前面已经完成了年平均、月平均、季平均、年季平均的相关性分析，但是我们这里还可以做一下原始数据的相关性分析
# 3.1.4 计算原始数据的相关性
# 读取降水、地表温度和NDVI的原始数据(2000~2016)
precipitation_data = pd.read_excel(r"E:\PRCP\table\unified_date\precip_topo_sc_monthly.xlsx",
                                   sheet_name="降水和地形因子月数据")
ndvi_data = pd.read_excel(r"E:\PRCP\table\unified_date\NDVI_topo_sc_monthly.xlsx", sheet_name="NDVI和地形因子月数据")
temperature_data = pd.read_excel(r"E:\PRCP\table\unified_date\temp_topo_sc_monthly.xlsx",
                                 sheet_name="地表温度和地形因子月数据")
soil_moisture_data = pd.read_excel(r"E:\PRCP\table\unified_date\soil_moisture_topo_sc_monthly.xlsx", sheet_name="土壤水分和地形因子月数据")
# 计算原始数据中降水和NDVI的相关系数矩阵
corr_precip_ndvi, p_precip_ndvi = corr_matrix(precipitation_data, ndvi_data)
# 计算原始数据中降水和地表温度的相关系数矩阵
corr_precip_temp, p_precip_temp = corr_matrix(precipitation_data, temperature_data)
# 计算原始数据中降水和土壤水分的相关系数矩阵
corr_precip_soil, p_precip_soil = corr_matrix(precipitation_data, soil_moisture_data)
# 将相关系数矩阵添加到列表中
corr_list['corr_precip_ndvi_original'] = corr_precip_ndvi
corr_list['corr_precip_temp_original'] = corr_precip_temp
corr_list['p_precip_ndvi_original'] = p_precip_ndvi
corr_list['p_precip_temp_original'] = p_precip_temp
corr_list['corr_precip_soil_original'] = corr_precip_soil
corr_list['p_precip_soil_original'] = p_precip_soil
# 将相关系数矩阵中的每一个元素与p值进行比较，如果p值大于0.05，则将相关系数矩阵中的该元素置为nan
corr_list['corr_precip_ndvi_original'] = corr_list['corr_precip_ndvi_original'].where(
    corr_list['p_precip_ndvi_original'] < p_value)
corr_list['corr_precip_temp_original'] = corr_list['corr_precip_temp_original'].where(
    corr_list['p_precip_temp_original'] < p_value)
corr_list['corr_precip_soil_original'] = corr_list['corr_precip_soil_original'].where(
    corr_list['p_precip_soil_original'] < p_value)
# 将相关系数矩阵中的每一列转化为二维数组(113行83列共计9379个元素)
corr_precip_ndvi_original = corr_list['corr_precip_ndvi_original'].values.reshape(83, 113)
corr_precip_temp_original = corr_list['corr_precip_temp_original'].values.reshape(83, 113)
corr_precip_soil_original = corr_list['corr_precip_soil_original'].values.reshape(83, 113)
# 将每一个相关系数数组输出为tif文件
write_tiff(corr_precip_ndvi_original, r'E:\PRCP\Statistical_chart\corr_precip_ndvi_original.tif', template_tif_path)
write_tiff(corr_precip_temp_original, r'E:\PRCP\Statistical_chart\corr_precip_temp_original.tif', template_tif_path)
write_tiff(corr_precip_soil_original, r'E:\PRCP\Statistical_chart\corr_precip_soil_original.tif', template_tif_path)

# 前面是正常的计算相关系数，但是我们查阅文献发现其实NDVI和降水其实是会相互影响的，所以我们需要考虑NDVI的滞后性
# 由于滞后的时间一般在0-3个月之间，所以这里我们只对月平均值数据进行相关性分析
# 3.1.5 计算NDVI原始数据和降水原始数据的滞后相关性
# 3.1.5.1 计算月尺度的相关系数矩阵
# 计算原始的降水数据和NDVI数据的相关系数矩阵
corr_precip_ndvi_delay1, p_precip_ndvi_delay1 = corr_matrix_delay(precipitation_data, ndvi_data, 1)
corr_precip_ndvi_delay2, p_precip_ndvi_delay2 = corr_matrix_delay(precipitation_data, ndvi_data, 2)
corr_precip_ndvi_delay3, p_precip_ndvi_delay3 = corr_matrix_delay(precipitation_data, ndvi_data, 3)
# 将相关系数矩阵添加到列表中
corr_list['corr_precip_ndvi_delay1'] = corr_precip_ndvi_delay1
corr_list['corr_precip_ndvi_delay2'] = corr_precip_ndvi_delay2
corr_list['corr_precip_ndvi_delay3'] = corr_precip_ndvi_delay3
corr_list['p_precip_ndvi_delay1'] = p_precip_ndvi_delay1
corr_list['p_precip_ndvi_delay2'] = p_precip_ndvi_delay2
corr_list['p_precip_ndvi_delay3'] = p_precip_ndvi_delay3
# 将相关系数矩阵中的每一个元素与p值进行比较，如果p值大于0.05，则将相关系数矩阵中的该元素置为nan
corr_list['corr_precip_ndvi_delay1'] = corr_list['corr_precip_ndvi_delay1'].where(
    corr_list['p_precip_ndvi_delay1'] < p_value)
corr_list['corr_precip_ndvi_delay2'] = corr_list['corr_precip_ndvi_delay2'].where(
    corr_list['p_precip_ndvi_delay2'] < p_value)
corr_list['corr_precip_ndvi_delay3'] = corr_list['corr_precip_ndvi_delay3'].where(
    corr_list['p_precip_ndvi_delay3'] < p_value)
# 将相关系数矩阵中的每一列转化为二维数组(113行83列共计9379个元素)
corr_precip_ndvi_delay1 = corr_list['corr_precip_ndvi_delay1'].values.reshape(83, 113)
corr_precip_ndvi_delay2 = corr_list['corr_precip_ndvi_delay2'].values.reshape(83, 113)
corr_precip_ndvi_delay3 = corr_list['corr_precip_ndvi_delay3'].values.reshape(83, 113)
# 将每一个相关系数数组输出为tif文件
write_tiff(corr_precip_ndvi_delay1, r'E:\PRCP\Statistical_chart\corr_precip_ndvi_delay1.tif', template_tif_path)
write_tiff(corr_precip_ndvi_delay2, r'E:\PRCP\Statistical_chart\corr_precip_ndvi_delay2.tif', template_tif_path)
write_tiff(corr_precip_ndvi_delay3, r'E:\PRCP\Statistical_chart\corr_precip_ndvi_delay3.tif', template_tif_path)

print('相关性分析完成！')
