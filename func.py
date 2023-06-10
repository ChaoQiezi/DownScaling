# @炒茄子  2023-03-26
from osgeo import gdal
import os
from scipy.stats import pearsonr, spearmanr
import rasterio
import geopandas as gpd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np

from sklearn.model_selection import GridSearchCV  # 网格搜索-超参数调优


def read_raster(raster_path):
    """
    获取栅格文件的栅格阵列
    参数说明:
    raster_path: 读取的tiff文件的绝对路径(分隔符为/)
    """

    # 获取raster文件对象
    dataset = gdal.Open(raster_path)

    # 获取栅格阵列
    band = dataset.GetRasterBand(1)  # GDAL中, 波段的索引从1开始
    raster_array = band.ReadAsArray()  # 获取该raster文件的栅格阵列

    return raster_array


def files_search(in_path, start_str="", end_str=""):
    """
    检索满足要求的文件, 将以列表形式返回每个文件路径
    参数说明:
    in_path: 检索的文件夹的绝对路径
    start_str: 文件名的起始字符串
    end_str: 文件名的结尾字符串
    """

    # 初始化存储满足要求的文件路径的列表
    dirs_list = []

    # 遍历文件夹中的所有文件
    for file_name in os.listdir(in_path):
        # 判断文件是否满足要求
        if file_name.startswith(start_str) and file_name.endswith(end_str):
            dirs_list.append(os.path.join(in_path, file_name))

    # 返回文件路径列表
    return dirs_list


def get_nodata_value(raster_path):
    """
    获取栅格文件中的缺失值NoData的实际值
    参数说明:
    raster_path: 读取的tiff文件的绝对路径(分隔符为/)
    """

    # 获取raster文件对象
    dataset = gdal.Open(raster_path)

    # 获取栅格阵列
    band = dataset.GetRasterBand(1)  # GDAL中, 波段的索引从1开始
    # 获取nodata的数值
    nodata_value = band.GetNoDataValue()

    return nodata_value


def get_lon_lat(raster_path):
    """
    输入一个栅格图像的路径, 获取该栅格图像的经纬度信息
    :param raster_path: 输入栅格文件的绝对路径
    :return: 返回含经纬度信息的列表
    """

    # 打开栅格影像文件
    ds = gdal.Open(raster_path)

    # 获取地理变换参数
    geotransform = ds.GetGeoTransform()  # 一个包含6个元素的元组，分别表示左上角像元的x坐标、像元宽度、0、左上角像元的y坐标、0、像元高度。

    # 获取栅格影像的行列数
    rows = ds.RasterYSize
    cols = ds.RasterXSize

    # 生成行列号矩阵
    x, y = np.meshgrid(np.arange(cols), np.arange(rows))

    # 将行列号矩阵转换为经纬度矩阵
    lon = geotransform[0] + x * geotransform[1] + y * geotransform[2]
    lat = geotransform[3] + x * geotransform[4] + y * geotransform[5]

    # 将经纬度矩阵转化为一维列表
    lon = lon.reshape(-1)
    lat = lat.reshape(-1)

    return np.vstack((lat, lon))  # np.array也可, 位置不可换, 否则会出错(衔接append_lon_lat)


def append_lon_lat(array, lon_lat_array):
    """
    将传入的矩阵新左侧新添加2列，将经纬度信息存入
    :param array: 需要添加经纬度信息的矩阵
    :param lon_lat_array: 传入经纬度矩阵
    :return: 返回添加经纬度信息的矩阵
    """

    array.insert(0, "lat", lon_lat_array[0])
    array.insert(0, "lon", lon_lat_array[1])

    return array


def corr_matrix(matrix_x, matrix_y):
    """
    计算两个矩阵的相关系数(对应行求取)
    :param matrix_x: DataFrame
    :param matrix_y: DataFrame
    :return: 返回相关系数列表
    """
    corr_s = []
    p_s = []
    for i in range(0, matrix_x.shape[0]):
        # 计算每一行的相关系数
        # 计算之前, 判断两行元素是否为常数数列 ==> 这里主要是针对土地利用数据, 因为有可能出现所有年份某一行(某一像元)的土地利用类型没有
        # 发生变化, 这样的话, 该行的标准差为0, 会导致相关系数计算出错
        if matrix_x.iloc[i, 5:].std() == 0 or matrix_y.iloc[i, 5:].std() == 0:
            # 若具有常数数列, 则相关系数为nan
            corr_s.append(np.nan)
            p_s.append(np.nan)
            continue
        corr, p = spearmanr(matrix_x.iloc[i, 5:], matrix_y.iloc[i, 5:])
        # 将相关系数添加到列表中
        corr_s.append(corr)
        p_s.append(p)

    return corr_s, p_s


def corr_matrix_delay(matrix_x, matrix_y, delay_month):
    """
    计算两个矩阵的相关系数(对应行求取)
    :param matrix_x: DataFrame
    :param matrix_y: DataFrame
    :param delay_month: 延迟的月份
    :return:
    """
    corr_s = []
    p_s = []
    for i in range(0, matrix_x.shape[0]):
        # 计算每一行的相关系数
        corr, p = spearmanr(matrix_x.iloc[i, 5:-delay_month], matrix_y.iloc[i, 5 + delay_month:])
        # 将相关系数添加到列表中
        corr_s.append(corr)
        p_s.append(p)
    return corr_s, p_s


def write_tiff(array, out_path, template_tif_path):
    """
    将array输出为tiff文件
    :param array: 写入的数组(二维)
    :param out_path: 输出路径
    :param template_tif_path: 模板文件路径
    :return:
    """
    # 先读取一个tif文件作为模板
    pattern_tif = gdal.Open(template_tif_path)
    # 读取模板文件的投影信息
    proj = pattern_tif.GetProjection()
    # 读取模板文件的地理信息
    geotrans = pattern_tif.GetGeoTransform()
    # 获取模板文件的行列数
    rows = pattern_tif.RasterXSize
    cols = pattern_tif.RasterYSize
    # 基于模板文件的投影信息和地理信息创建输出文件
    out_tif = gdal.GetDriverByName('GTiff').Create(out_path, rows, cols, 1, gdal.GDT_Float32)  # GTiff表示输出为tif文件

    # 将投影信息和地理信息写入输出文件
    out_tif.SetProjection(proj)  # 设置投影信息
    out_tif.SetGeoTransform(geotrans)  # 设置地理信息
    # 将数据写入输出文件
    out_tif.GetRasterBand(1).WriteArray(array)
    # 将缓存数据写入磁盘
    out_tif.FlushCache()


def read_tiff(in_path):
    """
    读取tiff文件, 返回tiff文件的数组
    :param in_path: tiff文件路径
    :return: 返回tiff文件的数组
    """

    tiff = gdal.Open(in_path)
    return tiff.ReadAsArray()


def plot_correlation_map(tif_file_path, shp_file_path):
    """
    绘制相关性图
    :param tif_file_path: 相关性tif文件路径
    :param shp_file_path: tif文件的边界文件路径
    :return: None
    """
    # 正常显示中文
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    # 读取tif文件
    raster = rasterio.open(tif_file_path)

    # 读取shp文件
    boundary = gpd.read_file(shp_file_path)

    # 将矢量边界数据转换为与栅格数据相同的CRS
    boundary = boundary.to_crs(raster.crs)

    # 获取栅格数据
    raster_data = raster.read(1)

    # 获取栅格数据范围和分辨率
    transform = raster.transform
    extent = raster.bounds
    x_res, y_res = transform.a, -transform.e
    x_min, x_max, y_min, y_max = extent.left, extent.right, extent.bottom, extent.top
    x_ticks = np.arange(x_min, x_max, x_res * 20)
    y_ticks = np.arange(y_min, y_max, y_res * 12)

    # 绘制地图
    fig, ax = plt.subplots(figsize=(12, 10))
    img = ax.imshow(raster_data, cmap='viridis', alpha=0.8,
                    extent=[x_min, x_max, y_min, y_max])  # 使用viridis色带显示栅格数据，设置透明度为0.8
    # img表示栅格数据的句柄，用于绘制图例

    boundary.boundary.plot(ax=ax, color='black', linewidth=0.5)  # 在地图上绘制边界，调整线条宽度为0.5

    # 设置图表标题和坐标轴标签
    ax.set_title('降水与NDVI的相关性分布', fontsize=20, fontweight='bold', color='black')
    ax.set_xlabel('经度', fontsize=18, color='black')
    ax.set_ylabel('纬度', fontsize=18, color='black')

    # 设置坐标轴刻度和字体大小
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)
    ax.tick_params(axis='both', labelsize=16, colors='black')

    # 添加网格线
    ax.grid(True, linestyle='-.', linewidth=0.6, alpha=1, color='gray')

    # 调整边框线宽度
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(1.5)

    # 添加图例
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)  # 设置图例位置, size为图例宽度, pad为图例与图表的间距
    cbar = plt.colorbar(img, cax=cax)  # 设置图例, cax为图例位置
    cbar.ax.tick_params(labelsize=16, colors='black')  # 设置图例刻度字
    cbar.set_label('相关系数', fontsize=18, color='black')

    # 显示图表
    plt.show()


def subplot_correlation_maps(tif_file_paths, shp_file_paths=None, title_names=None, ncols=4):
    """
    绘制多个空间分布图
    :param tif_file_paths: 栅格影像的路径列表
    :param shp_file_paths: 矢量边界文件的路径列表
    :param title_names: 图表标题列表
    :param ncols: 每行显示的图表数量
    :return: None
    """
    # 如果没有传入矢量边界文件路径, 则默认为None
    if shp_file_paths is None:
        shp_file_paths = [None] * len(tif_file_paths)
    # 如果没有传入图表标题, 则默认为None
    title_names = [os.path.basename(tif_file_paths[i]).split('.')[0] for i in range(len(shp_file_paths)) if
                   title_names is None]
    # 正常显示中文
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    nmaps = len(tif_file_paths)  # 计算图表的数量
    nrows = int(np.ceil(nmaps / ncols))  # 计算图表的行数

    fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(12 * ncols, 10 * nrows), constrained_layout=True)
    axs = axs.flatten()

    for idx, (tif_file_path, shp_file_path) in enumerate(zip(tif_file_paths, shp_file_paths)):
        # 读取tif文件
        raster = rasterio.open(tif_file_path)

        # 获取栅格数据
        raster_data = raster.read(1)

        # 获取栅格数据范围和分辨率
        transform = raster.transform  # 获取仿射变换参数
        extent = raster.bounds  # 获取栅格数据范围
        x_res, y_res = transform.a, -transform.e  # 获取栅格数据分辨率
        x_min, x_max, y_min, y_max = extent.left, extent.right, extent.bottom, extent.top  # 获取栅格数据范围
        x_ticks = np.arange(x_min, x_max, x_res * 300)  # 设置x轴刻度
        y_ticks = np.arange(y_min, y_max, y_res * 180)  # 设置y轴刻度

        # 绘制地图
        ax = axs[idx]  # 获取当前图表的句柄
        ax.grid(True, linestyle='-.', linewidth=0.6, alpha=1, color='gray')  # 添加网格线
        img = ax.imshow(raster_data, cmap='viridis_r', alpha=0.8,  # viridis_r色带表示viridis色带的反转
                        extent=[x_min, x_max, y_min, y_max])  # 使用viridis色带显示栅格数据，设置透明度为0.8

        # 边界处理
        # 读取shp文件
        if shp_file_path is not None:  # 如果传入了矢量边界文件路径, 那么绘制边界
            boundary = gpd.read_file(shp_file_path)
            # 将矢量边界数据转换为与栅格数据相同的CRS
            boundary = boundary.to_crs(raster.crs)
            # 在地图上绘制边界
            boundary.boundary.plot(ax=ax, color='black', linewidth=0.5)  # 在地图上绘制边界，调整线条宽度为0.5

        # 设置图表标题和坐标轴标签
        ax.set_title(title_names[idx], fontsize=20, fontweight='bold', color='black')
        ax.set_xlabel('经度', fontsize=18, color='black')
        ax.set_ylabel('纬度', fontsize=18, color='black')

        # 设置坐标轴刻度和字体大小
        ax.set_xticks(x_ticks)
        ax.set_yticks(y_ticks)
        ax.tick_params(axis='both', labelsize=16, colors='black')

        # 调整边框线宽度
        for axis in ['top', 'bottom', 'left', 'right']:
            ax.spines[axis].set_linewidth(1.5)

        # 添加图例
        divider = make_axes_locatable(ax)  # 获取当前图表的句柄
        cax = divider.append_axes("right", size="5%", pad=0.1)  # 设置图例的位置和大小
        cbar = plt.colorbar(img, cax=cax) # 绘制图例
        cbar.ax.tick_params(labelsize=16, colors='black')  # 设置图例刻度字体大小
        cbar.set_label('臭氧浓度(mol/m2)', fontsize=18, color='black')  # 设置图例标签

        # 如果子图数量不是完整的网格，删除多余的子图
    for idx in range(nmaps, nrows * ncols):  # 删除多余的子图
        fig.delaxes(axs[idx])

        # 显示图表
    plt.tight_layout()  # 调整子图间距
    plt.show()  # 显示图表


def replace_nodata_value_with_nan(pd_data):
    """
    将矩阵中的缺失值替换为np.nan
    :param pd_data: 传入的矩阵(PD.DataFrame)
    :return: 替换后的矩阵(PD.DataFrame)
    """
    for i in pd_data.columns:
        if i not in ['lon', 'lat']:
            pd_data.loc[:, i] = pd_data.loc[:, i].replace(pd_data.loc[0, i], np.nan)  # i表示列名
    return pd_data


def cv(model, x_train, y_train, param_grid, cv=5):
    """
    交叉验证, 返回最优模型参数和最优模型
    :param cv: 交叉验证的折数
    :param y_train: 训练集的标签项
    :param x_train:   训练集的特征项
    :param param_grid:  传入的参数网格
    :param model: 传入构建好的模型
    :return: 最优模型参数和最优模型
    """
    # 定义参数网格
    if param_grid is None:
        param_grid = {
            'max_depth': [8],  # 决策树的深度
            'max_features': [0.65, 0.75, 0.85],  # max_features: 每棵树的最大特征数
            # 'min_samples_leaf': [1, 2, 3],  # 叶子节点需要的最小样本数
            # 'min_samples_split': [2, 3, 4],  # 内部节点再划分所需的最小样本数
            'n_estimators': [500]  # 决策树的个数
        }
    # 创建网格搜索对象
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=cv, scoring='neg_mean_squared_error')
    # 在训练集上进行网格搜索
    grid_search.fit(x_train, y_train)
    # 输出最优参数和最优模型
    info = {'best_params': grid_search.best_params_, 'best_model': grid_search.best_estimator_}

    return info

'''def judge_nodata_zero(pd):
    """
    判断传入的矩阵中是否仅缺失值外，其余值都大于等于0
    :param pd: 传入的矩阵(PD.DataFrame)
    :return:
    """

    # 获取矩阵中的值
    values = pd.values

    # 判断是否仅缺失值为负数，其余值都大于0
    if np.all(values[values > 0]) and np.all(values[values < 0] == np.nan):
        # if判断意思是: 如果矩阵中所有大于0的值都为True, 并且矩阵中所有小于0的值都等于nodata_value, 则返回True
        # np.all()函数的意思是: 如果矩阵中所有值都为True, 则返回True
        # 或许你会想，只用np.all(values[values < 0] == nodata_value)就可以了，为什么还要加上np.all(values[values > 0])呢？
        # 这是因为，如果矩阵中所有值都小于0，那么np.all(values[values > 0])就会返回False，而np.all(values[values < 0] == nodata_value)会返回True
        return True
    else:
        return False'''
