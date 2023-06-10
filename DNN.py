import pandas as pd
import torch
import torch.nn as nn  # 神经网络模块
import torch.optim as optim  # 优化器模块
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# 读取数据
in_path = r'E:\PRCP\table\model_train_data\2015.xlsx'
data = pd.read_excel(in_path, sheet_name='2015')
# in_path = r'D:\task\engineering_practice2\NTL2012.xlsx'
# data = pd.read_excel(in_path, sheet_name='NTL2012')

# 提取特征和标签
y_name = 'Y'
X = data.drop(y_name, axis=1).values
y = data[y_name].values

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 特征标准化
scaler = StandardScaler()  # 生成一个scaler对象
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 将数据转换为PyTorch的Tensor类型
X_train = torch.Tensor(X_train)
X_test = torch.Tensor(X_test)
y_train = torch.Tensor(y_train).unsqueeze(1)  # 添加一个维度,变成n*1的矩阵而不是一个长度为n的向量
y_test = torch.Tensor(y_test).unsqueeze(1)


# 全连接层
class DNN(nn.Module):
    def __init__(self, input_dim, output_dim):  # 定义模型结构： 输入层 -> 隐藏层 -> 输出层
        super(DNN, self).__init__()
        self.fc1 = nn.Linear(input_dim, 128)
        self.relu = nn.LeakyReLU()  # 激活函数使用Leaky ReLU
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 32)
        self.fc4 = nn.Linear(32, output_dim)

    def forward(self, x):
        out = self.relu(self.fc1(x))
        out = self.relu(self.fc2(out))
        out = self.relu(self.fc3(out))
        out = self.fc4(out)
        return out


# 初始化模型
input_dim = X_train.shape[1]  # 输入层维度
output_dim = 1  # 输出层维度
model = DNN(input_dim, output_dim)
print(model)
# 定义损失函数和优化器
criterion = nn.MSELoss()  # 均方误差
optimizer = optim.Adam(model.parameters(), lr=0.001)  # Adam优化器-用于优化模型参数

# 将数据移动到GPU（如果可用）
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
X_train = X_train.to(device)
X_test = X_test.to(device)
y_train = y_train.to(device)
y_test = y_test.to(device)
model.to(device)

# 训练模型
num_epochs = 50  # 迭代次数
batch_size = 666  # 批次大小

for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    for i in range(0, len(X_train), batch_size):
        optimizer.zero_grad()  # 梯度清零
        outputs = model(X_train[i:i+batch_size])
        loss = criterion(outputs, y_train[i:i + batch_size])
        loss.backward()  # 反向传播以计算梯度
        optimizer.step()  # 根据梯度更新网络参数
        running_loss += loss.item()  # 累加损失

    # 打印训练损失
    plt.plot(epoch + 1, running_loss / (len(X_train) / batch_size), '.-')  # 绘制平均损失曲线
    # print('Epoch {} - Loss: {:.4f}'.format(epoch + 1, running_loss / (len(X_train) / batch_size)))
plt.show()

# 模型预测
model.eval()  # 将模型设置为评估模式
with torch.no_grad():  # 不计算梯度 ==> 表示不更新模型参数
    y_pred = model(X_test).cpu().numpy()

# 计算测试集的均方误差MSE
from sklearn.metrics import mean_squared_error
print('训练集MSE：', mean_squared_error(y_test, y_pred))
print('测试集MSE：', mean_squared_error(y_test, y_pred))

# 绘制预测值与真实值图
# 绘制残差图
plt.scatter(y_test.cpu().numpy(), y_pred - y_test.cpu().numpy())
plt.xlabel('y_test')
plt.ylabel('residuals')
plt.show()
# 绘制分布图
plt.scatter(y_test.cpu().numpy(), y_pred)
plt.xlabel('y_test')
plt.ylabel('y_pred')
plt.show()

# 保存预测数据和真实数据
data = pd.DataFrame(columns=['pred', 'real'])
# 将预测值和真实值添加到data中
data['pred'] = y_pred.reshape(-1)
data['real'] = y_test.cpu().numpy().reshape(-1)
# 保存数据(覆盖原来的数据)
data.to_excel(r'D:\pycharm_storage\DownScaling\achievement\pred.xlsx', index=False)

# 保存模型
torch.save(model.state_dict(), r'D:\pycharm_storage\DownScaling\achievement\model.pth')
