# @炒茄子  2023-04-04

from bin.func import *  # 导入自定义函数
import numpy as np
import pandas as pd

# 1.4 提取地表温度数据(白天平均温度)
print("正在读取多个地表温度tiff文件······")

# 输入路径
in_temperature_path = r"E:\PRCP\Temp_SC"
# 输出路径
out_temperature_path = r"E:\PRCP\table\before_unified_date\temp_sc_monthly.xlsx"

# 获取输入路径中所有tiff文件路径
temp_tiffs_path = files_search(in_temperature_path, end_str=".tif")
# 创建存储所有tiff文件数据的矩阵
temp_tiff_shape = read_raster(temp_tiffs_path[0]).shape  # 获取第一个tiff文件的shape, shape为二元数组，存储行数和列数
temp_tiffs_data = np.zeros([temp_tiff_shape[0] * temp_tiff_shape[1], len(temp_tiffs_path)])  # 创建存储所有tiff文件数据的矩阵
# 获取tiff文件的nodata值
temp_nodata_value = get_nodata_value(temp_tiffs_path[0])
# 获取tiff文件的经纬度信息
temp_lon_lat_array = get_lon_lat(temp_tiffs_path[0])
# 将经纬度数组中所有元素保留三位小数
temp_lon_lat_array = np.round(temp_lon_lat_array, 3)

# 循环处理每一个tiff文件
for tiff_index, tiff_path in enumerate(temp_tiffs_path):
    tiff_data = read_raster(tiff_path)  # 获取栅格阵列
    temp_tiffs_data[:, tiff_index] = tiff_data.reshape(-1)  # 将tiff文件的数据转换为一维数组并存储到temp_tiffs_data中

# 处理
col_index = [os.path.basename(tiff_path)[8:14] for tiff_path in temp_tiffs_path]  # 获取tiff文件名中的年月信息
temp_tiffs_data = pd.DataFrame(temp_tiffs_data, columns=col_index)
# 为tiffs_data每一行(每一像元)传入经纬度信息
temp_tiffs_data = append_lon_lat(temp_tiffs_data, temp_lon_lat_array)

# 将降水数据输出为excel
temp_tiffs_data.to_excel(out_temperature_path, header=True, index=False, sheet_name="地表温度月数据")
print("已读取多个地表温度tiff文件并输出为excel文件(每列为单个地表温度文件数据)<sheet=地表温度月数据>")
# 1.4 end
