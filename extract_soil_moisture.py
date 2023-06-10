# @炒茄子  2023-05-15

from bin.func import *  # 导入自定义函数
import numpy as np
import pandas as pd

# 读取土壤水分数据
print('正在读取土壤水分数据集······')

# 输入路径
in_soil_moisture_path = r"E:\PRCP\Soil_Moisture_monthly_2002_2018"
# 输出路径
out_soil_moisture_path = r"E:\PRCP\table\before_unified_date\soil_moisture_monthly.xlsx"

# 获取输入路径中所有tiff文件路径
soil_moisture_tiffs_path = files_search(in_soil_moisture_path, end_str=".tif")
# 创建存储所有tiff文件数据的矩阵
soil_moisture_tiff_shape = read_raster(soil_moisture_tiffs_path[0]).shape  # 获取第一个tiff文件的shape, shape为二元数组，存储行数和列数
soil_moisture_tiffs_data = np.zeros([soil_moisture_tiff_shape[0] * soil_moisture_tiff_shape[1], len(soil_moisture_tiffs_path)])  # 创建存储所有tiff文件数据的矩阵
# 获取tiff文件的nodata值
soil_moisture_nodata_value = get_nodata_value(soil_moisture_tiffs_path[0])
# 获取tiff文件的经纬度信息
soil_moisture_lon_lat_array = get_lon_lat(soil_moisture_tiffs_path[0])
# 将经纬度数组中所有元素保留三位小数
soil_moisture_lon_lat_array = np.round(soil_moisture_lon_lat_array, 3)

# 循环处理每一个tiff文件
for tiff_index, tiff_path in enumerate(soil_moisture_tiffs_path):
    tiff_data = read_raster(tiff_path)  # 获取栅格阵列
    soil_moisture_tiffs_data[:, tiff_index] = tiff_data.reshape(-1)  # 将tiff文件的数据转换为一维数组并存储到soil_moisture_tiffs_data中

# 处理
col_index = [''.join(os.path.basename(tiff_path)[3:10].split('_')) for tiff_path in soil_moisture_tiffs_path]  # 获取tiff文件名中的年月信息
soil_moisture_tiffs_data = pd.DataFrame(soil_moisture_tiffs_data, columns=col_index)
# 为soil_moisture_tiffs_data添加经纬度信息
soil_moisture_tiffs_data = append_lon_lat(soil_moisture_tiffs_data, soil_moisture_lon_lat_array)

# 将土壤水分数据输出为Excel
soil_moisture_tiffs_data.to_excel(out_soil_moisture_path, index=False, header=True, sheet_name='土壤水分月数据')
print('土壤水分数据集处理完毕！')


