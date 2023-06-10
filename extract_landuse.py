# @炒茄子  2023-04-25

from bin.func import *  # 导入自定义函数
import numpy as np
import pandas as pd

# 1.7 读取土地利用数据并处理
print("正在读取土地利用数据······")

# 输入路径
in_landuse_path = r"E:\PRCP\landuse_2001_2020\HeZehuang_landuse"
# 输出路径
out_landuse_path = r"E:\PRCP\table\before_unified_date\landuse_sc_yearly.xlsx"  # 土地利用数据只有年尺度的数据

# 获取输入路径中所有tiff文件路径
landuse_tiffs_path = files_search(in_landuse_path, end_str=".tif")
# 创建存储所有landuse tiff文件数据的矩阵
landuse_tiff_shape = read_raster(landuse_tiffs_path[0]).shape  # shape[0]为行数, shape[1]为列数
landuse_tiffs_data = np.zeros([landuse_tiff_shape[0] * landuse_tiff_shape[1], len(landuse_tiffs_path)])
# 获取landuse的经纬度信息
landuse_lon_lat_array = get_lon_lat(landuse_tiffs_path[0])
# 将经纬度数组中所有元素保留三位小数
landuse_lon_lat_array = np.round(landuse_lon_lat_array, 3)

# 循环处理每一个tiff文件
for tiff_index, tiff_path in enumerate(landuse_tiffs_path):
    tiff_data = read_raster(tiff_path)  # 获取栅格阵列
    landuse_tiffs_data[:, tiff_index] = tiff_data.reshape(-1)  # 将二维数组转换为一维数组

# 通过路径名获取landuse_tiffs_data的列标签值
col_index = [os.path.basename(tiff_path)[5:9] for tiff_path in landuse_tiffs_path]
# 将landuse_tiffs_data转换为pd的Dataframe
landuse_tiffs_data = pd.DataFrame(landuse_tiffs_data, columns=col_index)

# 为landuse_tiffs_data每一行(每一像元)传入经纬度信息
landuse_tiffs_data = append_lon_lat(landuse_tiffs_data, landuse_lon_lat_array)

# 将landuse_tiffs_data写入excel文件
landuse_tiffs_data.to_excel(out_landuse_path, sheet_name='土地利用数据', index=False, header=True)  # index=False表示不写入行索引, header=True表示写入列索引

print("土地利用数据读取完成！")

