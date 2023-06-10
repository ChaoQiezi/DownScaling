# @炒茄子  2023-06-02
import pandas as pd
from sklearn.ensemble import RandomForestRegressor  # 随机森林回归
from sklearn.model_selection import train_test_split  # 数据集划分
from sklearn.preprocessing import StandardScaler  # 数据标准化
from sklearn.metrics import mean_squared_error  # 均方误差
import joblib  # 模型保存
from bin.func import cv  # 交叉验证的函数

# 1.1 数据预处理
# 读取数据
in_path = r'E:\PRCP\table\model_train_data\2015.xlsx'
data = pd.read_excel(in_path, sheet_name='2015')

# 1.2 特征工程
# 提取特征和标签
y_name = 'precip_2015'
x = data.drop(y_name, axis=1).values
y = data[y_name].values
# 对特征项进行标准化
scaler = StandardScaler()  # 生成一个scaler对象
x = scaler.fit_transform(x)
# 划分训练集和测试集
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)


# 1.3 训练模型
# 构建随机森林模型
rf = RandomForestRegressor(n_jobs=-1, random_state=42)
# 超参数调优(交叉验证)和模型训练
flag = False  # 是否进行超参数调优
if flag:
    # 超参数调优(可选)
    param_grid = {'n_estimators': [300, 400, 500],  # 决策树的个数
                  'max_depth': [5, 7, 9],  # 决策树的深度
                  'min_samples_split': [3, 5, 7],  # 内部节点再划分所需最小样本数
                  'min_samples_leaf': [3, 5, 7],  # 叶子节点最少样本数
                  'max_features': [0.3, 0.5, 0.7, 0.9]  # 最大特征数
                  }
    info = cv(rf, x_train, y_train, param_grid=param_grid)
    print(info['best_params'])
    rf = info['best_model']
else:
    # 若不进行超参数调优，则直接使用默认参数进行模型的训练
    rf.fit(x_train, y_train)

# 评估模型
print('训练集R2：', rf.score(x_train, y_train))  # 这里的score实际上是R2,而不是正确率之类的
print('测试集R2：', rf.score(x_test, y_test))
print('训练集MSE：', mean_squared_error(y_train, rf.predict(x_train)))
print('测试集MSE：', mean_squared_error(y_test, rf.predict(x_test)))
# 输出特征重要性
print('特征重要性：', rf.feature_importances_)
importance_df = pd.DataFrame({'feature': data.drop(y_name, axis=1).columns,
                                'importance': rf.feature_importances_})
importance_df.sort_values(by='importance', ascending=False, inplace=True)
# 输出模型的参数
print(rf.get_params())
# 保存模型
# out_path = r'D:\pycharm_storage\DownScaling\achievement\RF.pkl'
# joblib.dump(rf, out_path)  # 保存模型
