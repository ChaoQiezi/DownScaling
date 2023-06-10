# @炒茄子  2023-03-29

from bin.func import *  # 导入自定义函数
import numpy as np
import pandas as pd


# 1.2 读取并处理DEM数据
print("正在读取DEM数据······")

# 输入路径
in_DEM_path = r"E:\PRCP\basic\DEM_sc_11km.tif"
# 输出路径
out_DEM_path = r"E:\PRCP\table\before_unified_date\DEM_sc.xlsx"

# 读取DEM数据并读取投影信息
DEM_data = read_raster(in_DEM_path)
# 读取对应像元的经纬度信息
DEM_lon_lat_array = get_lon_lat(in_DEM_path)
# 将经纬度数组中所有元素保留三位小数
DEM_lon_lat_array = np.round(DEM_lon_lat_array, 3)

# 二维转换为一维
DEM_data = DEM_data.reshape(-1)
# 将ndarray数据类型转换为pd的Dataframe
DEM_data = pd.DataFrame(DEM_data, columns=['DEM'])
# 将经纬度信息添加到DEM_data
DEM_data = append_lon_lat(DEM_data, DEM_lon_lat_array)

"""# 判断DEM与Precipitation的经纬度信息是否一致
diff = sum(np.square(precip_tiffs_data['lon'] - DEM_lon_lat_array[0])) + \
    sum(np.square(precip_tiffs_data['lat'] - DEM_lon_lat_array[1]))
# 这里如果降水数据与DEM数据经纬度信息一致，那么理论上diff应该为0，但是实际上程序计算会有误差导致diff为一个十分接近0的数
# 判断diff是否为一个十分接近0的数
if abs(diff) < 1e-10:
    print("降水数据与DEM数据经纬度信息一致, 已合并precipitation_tiffs_data和DEM_data")
else:
    print("降水数据与DEM数据经纬度信息不一致, 合并precipitation_tiffs_data和DEM_data失败")
    exit(1)  # 退出程序
"""

# 将DEM数据输出excel文件
DEM_data.to_excel(out_DEM_path, header=True, index=False, sheet_name="DEM数据")
print("已读取DEM并输出为excel文件<sheet=DEM数据>")
# 1.2 end



