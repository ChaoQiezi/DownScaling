# @炒茄子  2023-04-05

# Path: 数据预处理\提取数据\extract_aspect.py

from bin.func import *  # 导入自定义函数
import numpy as np
import pandas as pd

# 1.6 读取坡向数据
print("正在读取坡向和降水数据······")

# 输入路径
in_aspect_path = r"E:\PRCP\basic\Aspect_sc_11km.tif"
# 输出路径
out_aspect_path = r"E:\PRCP\table\before_unified_date\aspect_sc.xlsx"

# 读取坡向数据
aspect_data = read_raster(in_aspect_path)  # 获取栅格阵列
# 获取坡向文件的nodata值
aspect_nodata_value = get_nodata_value(in_aspect_path)
# 获取坡向文件的经纬度信息
aspect_lon_lat_array = get_lon_lat(in_aspect_path)
# 将经纬度数组中所有元素保留三位小数
aspect_lon_lat_array = np.round(aspect_lon_lat_array, 3)

# 将坡向栅格阵列转换为一维数组
aspect_data = aspect_data.reshape(-1)
# 将坡向栅格阵列转换为dataframe
aspect_data = pd.DataFrame(aspect_data, columns=["aspect"])
# 为tiffs_data每一行(每一像元)传入经纬度信息
aspect_data = append_lon_lat(aspect_data, aspect_lon_lat_array)

# 将坡向数据输出为excel
aspect_data.to_excel(out_aspect_path, header=True, index=False, sheet_name="坡向数据")
print("已读取坡向数据并输出为excel文件<sheet=坡向数据>")
# 1.6 end
