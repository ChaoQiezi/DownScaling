from bin.func import plot_correlation_map, subplot_correlation_maps

# 相关系数图绘制
tif_file_paths = [
    # r'E:\PRCP\Statistical_chart\corr_precip_ndvi_delay1.tif',  # 滞后一月
    # r'E:\PRCP\Statistical_chart\corr_precip_ndvi_delay2.tif',  # 滞后两月
    # r'E:\PRCP\Statistical_chart\corr_precip_ndvi_delay3.tif',  # 滞后三月
    # r'E:\PRCP\Statistical_chart\corr_precip_ndvi_month.tif',  # 月尺度ndvi
    # r'E:\PRCP\Statistical_chart\corr_precip_ndvi_year.tif',  # 年尺度ndvi
    # r'E:\PRCP\Statistical_chart\corr_precip_ndvi_year_season.tif',  # 年尺度季节ndvi
    # r'E:\PRCP\Statistical_chart\corr_precip_ndvi_original.tif',  # 原始ndvi数据
    # r'E:\PRCP\Statistical_chart\corr_precip_temp_month.tif',  # 月尺度温度
    # r'E:\PRCP\Statistical_chart\corr_precip_temp_year.tif',  # 年尺度温度
    # r'E:\PRCP\Statistical_chart\corr_precip_temp_year_season.tif',  # 年尺度季节温度
    # r'E:\PRCP\Statistical_chart\corr_precip_temp_original.tif',  # 原始温度数据
    # r'E:\PRCP\Statistical_chart\corr_precip_landuse_year.tif',  # 年尺度土地利用(土地利用只有年尺度)
    # r'E:\PRCP\Statistical_chart\corr_precip_soil_moisture_month.tif',  # 月尺度土壤水分
    # r'E:\PRCP\Statistical_chart\corr_precip_soil_moisture_year.tif',  # 年尺度土壤水分
    # r'E:\PRCP\Statistical_chart\corr_precip_soil_moisture_year_season.tif',  # 年尺度季节土壤水分
    # r'E:\PRCP\Statistical_chart\corr_precip_soil_original.tif',  # 原始土壤水分数据
]

shp_file_paths = [r'E:\PRCP\basic\sc-sheng-A_wgs84.shp' for i in range(len(tif_file_paths))]
subplot_correlation_maps(tif_file_paths, shp_file_paths=None, ncols=2)
# plot_correlation_map(tif_file_paths[0], shp_file_paths[0])
