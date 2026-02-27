# 导入PyTorch库
import torch
import torch.nn as nn

# 定义输入层大小、隐藏层大小、输出层大小和批量大小
n_in, n_h, n_out, batch_size = 10, 5, 1, 10

# 创建虚拟输入数据和目标数据
x = torch.randn(batch_size, n_in)  # 随机生成输入数据
y = torch.tensor([[1.0], [0.0], [0.0], 
                 [1.0], [1.0], [1.0], [0.0], [0.0], [1.0], [1.0]])  # 目标输出数据

# 创建顺序模型，包含线性层、ReLU激活函数和Sigmoid激活函数
model = nn.Sequential(
   nn.Linear(n_in, n_h),  # 输入层到隐藏层的线性变换
   nn.ReLU(),            # 隐藏层的ReLU激活函数
   nn.Linear(n_h, n_out),  # 隐藏层到输出层的线性变换
   nn.Sigmoid()           # 输出层的Sigmoid激活函数
)

# 等价的模型定义方式
# class SimpleNN(nn.Module):
#     def __init__(self):
#         super(SimpleNN, self).__init__()
#         self.fc1 = nn.Linear(n_in, n_h)
#         self.relu = nn.ReLU()
#         self.fc2 = nn.Linear(n_h, n_out)
#         self.sigmoid = nn.Sigmoid()
#     
#     def forward(self, x):
#         x = self.relu(self.fc1(x))
#         x = self.sigmoid(self.fc2(x))
#         return x

# 定义均方误差损失函数和随机梯度下降优化器
criterion = torch.nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)  # 学习率为0.01

model.train()
# 执行梯度下降算法进行模型训练
for epoch in range(100):  # 迭代50次
   y_pred = model(x)  # 前向传播，计算预测值
   loss = criterion(y_pred, y)  # 计算损失
   print('epoch: ', epoch, 'loss: ', loss.item())  # 打印损失值

   optimizer.zero_grad()  # 清零梯度
   loss.backward()  # 反向传播，计算梯度
   optimizer.step()  # 更新模型参数
   
print("y_pred after training:", model(x).detach().numpy())
# 预测结果是概率，输出大于0.5的为1，否则为0
y_result = (model(x)[:, 0] > 0.5).float().unsqueeze(1)
print("y result after training:", y_result.numpy())
print("y true:", y.numpy())

import torch.onnx 
# 转换的onnx格式的名称，文件后缀需为.onnx
onnx_file_name = "deploy.onnx"
# 我们需要转换的模型，将torch_model设置为自己的模型
deploy_model = model
# # 加载权重，将model.pth转换为自己的模型权重
# # 如果模型的权重是使用多卡训练出来，我们需要去除权重中多的module. 具体操作可以见5.4节
# deploy_model = deploy_model.load_state_dict(torch.load("model.pth"))
# 导出模型前，必须调用model.eval()或者model.train(False)
deploy_model.eval()
# dummy_input就是一个输入的实例，仅提供输入shape、type等信息 
dummy_input = torch.randn(batch_size, n_in, requires_grad=True) 
# 这组输入对应的模型输出
output = deploy_model(dummy_input)
# 导出模型
torch.onnx.export(deploy_model,        # 模型的名称
                  dummy_input,   # 一组实例化输入
                  onnx_file_name,   # 文件保存路径/名称
                  export_params=True,        #  如果指定为True或默认, 参数也会被导出. 如果你要导出一个没训练过的就设为 False.
                  opset_version=10,          # ONNX 算子集的版本，当前已更新到15
                  do_constant_folding=True,  # 是否执行常量折叠优化
                  input_names = ['input'],   # 输入模型的张量的名称
                  output_names = ['output'], # 输出模型的张量的名称
                  # dynamic_axes将batch_size的维度指定为动态，
                  # 后续进行推理的数据可以与导出的dummy_input的batch_size不同
                  dynamic_axes={'input' : {0 : 'batch_size'},    
                                'output' : {0 : 'batch_size'}})