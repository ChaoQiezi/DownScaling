# @炒茄子  2023-04-04
import numpy as np
import pandas as pd

# 02 整理数据
print("正在进行细节处理以及时间序列统一······")
# 2.1 将所有因子和目标数据(DEM\坡度\坡向\NDVI\地表温度\降水)进行年月份的整理(全部统一为2000~2016年)
# 读取DEM数据(excel文件)，并将其转换为Dataframe
dem_data = pd.read_excel(r"E:\PRCP\table\before_unified_date\DEM_sc.xlsx", sheet_name="DEM数据")
# 读取降水数据(excel文件)，并将其转换为Dataframe
precipitation_data = pd.read_excel(r"E:\PRCP\table\before_unified_date\precip_sc_monthly.xlsx", sheet_name="降水月数据")
# 读取坡度数据(excel文件)，并将其转换为Dataframe
slope_data = pd.read_excel(r"E:\PRCP\table\before_unified_date\slope_sc.xlsx", sheet_name="坡度数据")
# 读取坡向数据(excel文件)，并将其转换为Dataframe
aspect_data = pd.read_excel(r"E:\PRCP\table\before_unified_date\aspect_sc.xlsx", sheet_name="坡向数据")
# 读取NDVI数据(excel文件)，并将其转换为Dataframe
ndvi_data = pd.read_excel(r"E:\PRCP\table\before_unified_date\NDVI_sc_monthly.xlsx", sheet_name="NDVI月数据")
# 读取地表温度数据(excel文件)，并将其转换为Dataframe
temperature_data = pd.read_excel(r"E:\PRCP\table\before_unified_date\temp_sc_monthly.xlsx", sheet_name="地表温度月数据")
# 读取土地利用数据(excel文件), 并将其转换为Dataframe
landuse_data = pd.read_excel(r"E:\PRCP\table\before_unified_date\landuse_sc_yearly.xlsx", sheet_name="土地利用数据")
# 读取土壤水分数据(excel文件), 并将其转换为Dataframe
soilmoisture_data = pd.read_excel(r"E:\PRCP\table\before_unified_date\soil_moisture_monthly.xlsx", sheet_name="土壤水分月数据")

# 将ndvi 地表温度 降水数据的年份进行统一
"""
ndvi: 200002-201605
地表温度: 200003-201605
降水: 200006-202109
土地利用: 2001-2016
土壤水分: 200207-201812
故统一在2003年01月~2015年12月
"""
# 进行
# 将各个数据的-3.402823e+38/65535(ArcGIS的nodata)设置为nan
dem_nodata = dem_data.loc[0, 'DEM']  # 获取dem_data的无效值
dem_data = dem_data.replace(dem_nodata, np.nan)
precipitation_nodata = precipitation_data.loc[0, '200301']  # 获取precipitation_data的无效值
precipitation_data = precipitation_data.replace(precipitation_nodata, np.nan)
slope_nodata = slope_data.loc[0, 'slope']  # 获取slope_data的无效值
slope_data = slope_data.replace(slope_nodata, np.nan)
aspect_nodata = aspect_data.loc[0, 'aspect']  # 获取aspect_data的无效值
aspect_data = aspect_data.replace(aspect_nodata, np.nan)
ndvi_nodata = ndvi_data.loc[0, '200301']  # 获取ndvi_data的无效值
ndvi_data = ndvi_data.replace(ndvi_nodata, np.nan)
temperature_nodata = temperature_data.loc[0, '200301']  # 获取temperature_data的无效值
temperature_data = temperature_data.replace(temperature_nodata, np.nan)
landuse_noata = landuse_data.loc[0, '2003']  # 获取landuse_data的无效值
landuse_data = landuse_data.replace(landuse_noata, np.nan)
soilmoisture_nodata = soilmoisture_data.loc[0, '200301']  # 获取soilmoisture_data的无效值
soilmoisture_data = soilmoisture_data.replace(soilmoisture_nodata, np.nan)
# # 先新建一行，用于存放date型的日期(该代码块疑似无用, 过一段时间检验删除)
# precipitation_data.loc['date'] = np.nan
# ndvi_data.loc['date'] = np.nan
# temperature_data.loc['date'] = np.nan
# landuse_data.loc['date'] = np.nan
# 对降水、NDVI、地表温度数据进行细节处理(这里指在有一些列标签具有相同时间，需要对相同月份列进行求取平均值)
precipitation_data.columns = [i[:6] for i in precipitation_data.columns]
precipitation_data = precipitation_data.groupby(precipitation_data.columns, axis=1).mean()
ndvi_data.columns = [i[:6] for i in ndvi_data.columns]
ndvi_data = ndvi_data.groupby(ndvi_data.columns, axis=1).mean()
temperature_data.columns = [i[:6] for i in temperature_data.columns]
temperature_data = temperature_data.groupby(temperature_data.columns, axis=1).mean()
soilmoisture_data.columns = [i[:6] for i in soilmoisture_data.columns]
soilmoisture_data = soilmoisture_data.groupby(soilmoisture_data.columns, axis=1).mean()
# 将降水、ndvi、地表温度, 土地利用数据的2003年01月~2015年12月的列月份保留，其余的月份列全部删除, lat和lon保留
precipitation_data = pd.concat([precipitation_data.loc[:, ['lon', 'lat']], precipitation_data.loc[:, '200301':'201512']], axis=1)
ndvi_data = pd.concat([ndvi_data.loc[:, ['lon', 'lat']], ndvi_data.loc[:, '200301':'201512']], axis=1)
temperature_data = pd.concat([temperature_data.loc[:, ['lon', 'lat']], temperature_data.loc[:, '200301':'201512']], axis=1)
landuse_data = pd.concat([landuse_data.loc[:, ['lon', 'lat']], landuse_data.loc[:, '2003':'2015']], axis=1)  # 注意土地利用数据只有年尺度
soilmoisture_data = pd.concat([soilmoisture_data.loc[:, ['lon', 'lat']], soilmoisture_data.loc[:, '200301':'201512']], axis=1)
# 将坡度、坡向、DEM数据都合并到降水、ndvi、地表温度数据中(基于经纬度信息进行合并)
# 先合并坡度、坡向、DEM数据
slope_aspect_data = pd.merge(slope_data, aspect_data, on=['lon', 'lat'], how='left')
slope_aspect_dem_data = pd.merge(dem_data, slope_aspect_data, on=['lon', 'lat'], how='left')
precipitation_data = pd.merge(slope_aspect_dem_data, precipitation_data, on=['lon', 'lat'], how='left')
ndvi_data = pd.merge(slope_aspect_dem_data, ndvi_data, on=['lon', 'lat'], how='left')
temperature_data = pd.merge(slope_aspect_dem_data, temperature_data, on=['lon', 'lat'], how='left')
landuse_data = pd.merge(slope_aspect_dem_data, landuse_data, on=['lon', 'lat'], how='left')
soilmoisture_data = pd.merge(slope_aspect_dem_data, soilmoisture_data, on=['lon', 'lat'], how='left')
# 将统一月份后的NDVI、降水、地表温度数据输出为excel文件
precipitation_data.to_excel(r"E:\PRCP\table\unified_date\precip_topo_sc_monthly.xlsx", sheet_name="降水和地形因子月数据", header=True, index=False)
ndvi_data.to_excel(r"E:\PRCP\table\unified_date\NDVI_topo_sc_monthly.xlsx", sheet_name="NDVI和地形因子月数据", header=True, index=False)
temperature_data.to_excel(r"E:\PRCP\table\unified_date\temp_topo_sc_monthly.xlsx", sheet_name="地表温度和地形因子月数据", header=True, index=False)
landuse_data.to_excel(r"E:\PRCP\table\unified_date\landuse_topo_sc_yearly.xlsx", sheet_name="土地利用和地形因子年数据", header=True, index=False)
soilmoisture_data.to_excel(r"E:\PRCP\table\unified_date\soil_moisture_topo_sc_monthly.xlsx", sheet_name="土壤水分和地形因子月数据", header=True, index=False)
print("数据处理完成！")
# 2.1 End

