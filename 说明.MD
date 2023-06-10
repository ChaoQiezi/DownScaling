# 01 这是关于降水降尺度的文件和处理说明
## 1.1 文件组成
### 1.1.1 数据预处理
* 提取数据(FileFolder): 地形因子.tif\气象因子.tif等的提取 ==> Excel表格  
  
        |-----> extract_aspect.py(从四川省坡向tif影像中提取栅格阵列转化为Excel)  
        |-----> extract_dem.py(从四川省DEMtif影像中提取栅格阵列转化为Excel)  
        |-----> extract_landuse.py(从四川省土地利用类型tif影像中提取栅格阵列转化为Excel)  
        |-----> extract_ndvi.py(从四川省ndvi tif影像中提取栅格阵列转化为Excel)  
        |-----> extract_precip.py(从四川省降水tif影像中提取栅格阵列转化为Excel)  
        |-----> extract_slope.py(从四川省坡度tif影像中提取栅格阵列转化为Excel)
        |-----> extract_temp.py(从四川省地表温度tif影像中提取栅格阵列转化为Excel)  
  
* 整理数据(FilerFoler): 日期的统一(过滤日期)\各类均值处理以及其它一些细节处理
  
        |-----> unified_date.py(过滤日期)  
        |-----> aver_season_year.py(各类均值处理)  

### 1.1.2 统计分析
* Analysis(FileFolder): 进行统计计算

        |-----> corr.py(相关系数分析<斯皮尔曼系数>)
        |-----> window_corr1.py(滑动窗口的相关系数分析<皮尔逊系数>)
        |-----> window_corr2.py(滑动窗口的相关系数分析<斯皮尔曼系数>)

* Plot(FileFolder): 进行统计计算的结果绘图
  
        |-----> corr_plot.py(各类均值处理)

### 1.1.3 模型
* Model(FileFolder): 模型的建立

        |-----> model.py(模型的建立和训练)

## 1.2 数据处理
