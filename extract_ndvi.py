# @炒茄子  2023-03-29
from bin.func import *  # 导入自定义函数
import numpy as np
import pandas as pd

# 1.3 读取NDVI并处理
print("正在读取NDVI数据······")

# 输入路径
in_ndvi_path = r"E:\PRCP\MODND1M_NDVI_SC"
# 输出路径
out_ndvi_path = r"E:\PRCP\table\before_unified_date\NDVI_sc_monthly.xlsx"

# 获取输入路径中所有tiff文件路径
ndvi_tiffs_path = files_search(in_ndvi_path, end_str=".tif")
# 创建存储所有ndvi tiff文件数据的矩阵
ndvi_tiff_shape = read_raster(ndvi_tiffs_path[0]).shape  # shape[0]为行数, shape[1]为列数
ndvi_tiffs_data = np.zeros([ndvi_tiff_shape[0] * ndvi_tiff_shape[1], len(ndvi_tiffs_path)])
# 获取ndvi的经纬度信息
ndvi_lon_lat_array = get_lon_lat(ndvi_tiffs_path[0])
# 将经纬度数组中所有元素保留三位小数
ndvi_lon_lat_array = np.round(ndvi_lon_lat_array, 3)

# 循环处理每一个tiff文件
for tiff_index, tiff_path in enumerate(ndvi_tiffs_path):
    tiff_data = read_raster(tiff_path)  # 获取栅格阵列
    ndvi_tiffs_data[:, tiff_index] = tiff_data.reshape(-1)  # 将二维数组转换为一维数组

# 通过路径名获取ndvi_tiffs_data的列标签值
col_index = [os.path.basename(tiff_path)[8:14] for tiff_path in ndvi_tiffs_path]
# 将ndvi_tiffs_data转换为pd的Dataframe
ndvi_tiffs_data = pd.DataFrame(ndvi_tiffs_data, columns=col_index)

"""# 判断ndvi与Precipitation的经纬度信息是否一致
diff = sum(np.square(precipitation_data['lon'] - ndvi_lon_lat_array[0])) + \
    sum(np.square(precipitation_data['lat'] - ndvi_lon_lat_array[1]))
# 判断diff是否为十分接近0的数
if abs(diff) < 1e-10:
    print("降水数据与NDVI数据经纬度信息一致")
else:
    print("降水数据与NDVI数据经纬度信息不一致")"""

# 为ndvi_tiffs_data每一行(每一像元)传入经纬度信息
ndvi_tiffs_data = append_lon_lat(ndvi_tiffs_data, ndvi_lon_lat_array)
# 将ndvi数据输出为excel文件
ndvi_tiffs_data.to_excel(out_ndvi_path, header=True, index=False, sheet_name="NDVI月数据")
print("已读取NDVI并输出为excel文件<sheet=NDVI月数据>")
# 1.3 end
