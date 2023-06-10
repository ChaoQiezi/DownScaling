# @炒茄子  2023-03-29

from bin.func import *  # 导入自定义函数
import numpy as np
import pandas as pd

# 01 提取数据
# 1.1 读取多个降水tiff文件生成csv文件(每一行为单个像元数据)
print("正在读取多个降水tiff文件······")

# 输入路径
in_precipitation_path = r"E:\PRCP\PRCP_monthly_GPM_SC"
# 输出路径
out_precipitation_path = r"E:\PRCP\table\before_unified_date\precip_sc_monthly.xlsx"
# 获取输入路径中所有tiff文件路径
precip_tiffs_path = files_search(in_precipitation_path, end_str=".tif")
# 创建存储所有tiff文件数据的矩阵
precip_tiff_shape = read_raster(precip_tiffs_path[0]).shape
precip_tiffs_data = np.zeros([precip_tiff_shape[0] * precip_tiff_shape[1], len(precip_tiffs_path)])
# 获取tiff文件的nodata值
precip_nodata_value = get_nodata_value(precip_tiffs_path[0])
# 获取tiff文件的经纬度信息
precipitation_lon_lat_array = get_lon_lat(precip_tiffs_path[0])
# 将经纬度数组中所有元素保留三位小数
precipitation_lon_lat_array = np.round(precipitation_lon_lat_array, 3)

# 循环处理每一个tiff文件
for tiff_index, tiff_path in enumerate(precip_tiffs_path):
    tiff_data = read_raster(tiff_path)  # 获取栅格阵列
    precip_tiffs_data[:, tiff_index] = tiff_data.reshape(-1)

# 处理
col_index = [os.path.basename(tiff_path).split('.')[0] for tiff_path in precip_tiffs_path]
precip_tiffs_data = pd.DataFrame(precip_tiffs_data, columns=col_index)
# 为tiffs_data每一行(每一像元)传入经纬度信息
precip_tiffs_data = append_lon_lat(precip_tiffs_data, precipitation_lon_lat_array)

# 将降水数据输出为excel
precip_tiffs_data.to_excel(out_precipitation_path, header=True, index=False, sheet_name="降水月数据")
print("已读取多个降水tiff文件并输出为excel文件(每列为单个降水文件数据)<sheet=降水数据>")
# 1.1 end
