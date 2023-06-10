# @炒茄子  2023-04-04

# Path: 数据预处理\提取数据\extract_temp.py

from bin.func import *  # 导入自定义函数
import numpy as np
import pandas as pd

# 1.5 读取坡向数据
print("正在读取坡度和降水数据······")

# 输入路径
in_slope_path = r"E:\PRCP\basic\Slope_sc_11km.tif"
# 输出路径
out_slope_path = r"E:\PRCP\table\before_unified_date\slope_sc.xlsx"

# 读取坡度数据
slope_data = read_raster(in_slope_path)  # 获取栅格阵列
# 获取tiff文件的nodata值
slope_nodata_value = get_nodata_value(in_slope_path)
# 获取tiff文件的经纬度信息
slope_lon_lat_array = get_lon_lat(in_slope_path)
# 将经纬度数组中所有元素保留三位小数
slope_lon_lat_array = np.round(slope_lon_lat_array, 3)

# 将坡度栅格阵列转换为一维数组
slope_data = slope_data.reshape(-1)
# 将坡度栅格阵列转换为dataframe
slope_data = pd.DataFrame(slope_data, columns=["slope"])
# 为tiffs_data每一行(每一像元)传入经纬度信息
slope_data = append_lon_lat(slope_data, slope_lon_lat_array)

# 将坡度数据输出为excel
slope_data.to_excel(out_slope_path, header=True, index=False, sheet_name="坡度数据")
print("已读取坡度数据并输出为excel文件<sheet=坡度数据>")
# 1.5 end
