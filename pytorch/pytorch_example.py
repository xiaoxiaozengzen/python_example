import torch
import numpy as np

def base():
    # 当前安装的 PyTorch 库的版本
    print(torch.__version__)
    # 检查 CUDA 是否可用，即你的系统有 NVIDIA 的 GPU
    print(torch.cuda.is_available())
    
    x = torch.rand(5, 3)
    print(x)  # 输出一个 5x3 的随机张量
    
    num_array = np.array([[1, 2, 3], [4, 5, 6]])
    tensor_from_array = torch.from_numpy(num_array)
    print(tensor_from_array)  # 输出从 NumPy 数组转换来的张量
    
    # 在指定设备（CPU/GPU）上创建张量
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    d = torch.randn(2, 3, device=device)
    print(d)
    print(d.shape)  # 输出张量的形状
    print(d.t())     # 输出张量的转置
    
    tensor_required_gard = torch.tensor([1.0], requires_grad=True)
    print(tensor_required_gard)  # 输出一个需要梯度计算的张量
    tensoe_result = tensor_required_gard * 2
    tensoe_result.backward()
    print(tensor_required_gard.grad)  # 输出梯度值
    
    y = torch.zeros(2, 3)
    print(y)  # 输出一个 2x3 的零张量
    
def linear_layer():
    import torch.nn as nn
    # 演示 nn.Linear 中神经元的数量与参数形状
    linear1 = nn.Linear(2, 3)  # in_features=2, out_features=3（可视为 3 个神经元）
    print('weight shape:', linear1.weight.shape)  # (out_features, in_features)
    print('bias shape:  ', linear1.bias.shape)    # (out_features,)
    linear2 = nn.Linear(3, 1)  # in_features=3, out_features=1（可视为 1 个神经元）
    print('weight shape:', linear2.weight.shape)  # (out_features, in_features)
    print('bias shape:  ', linear2.bias.shape)    # (out_features,)
    
    # 用一个小输入看输出维度：
    x = torch.randn(4, 2)  # batch=4, in_features=2
    y = linear1(x)
    print("y shape:", y.shape)  # (batch_size, out_features)
    print("output y:", y)
    z = linear2(y)
    print("z shape:", z.shape)  # (batch_size, out_features)
    print("output z:", z)
    
def conv2d_layer():
    import torch.nn as nn
    # batch_size=10, channels=3, height=32, width=32
    in_data = torch.randn(10, 3, 32, 32)
    # 卷积层示例：out_channels 相当于卷积层的“神经元数”
    conv = nn.Conv2d(in_channels=3, out_channels=8, kernel_size=3)
    print('conv weight shape:', conv.weight.shape)  # (out_channels, in_channels, kernel_H, kernel_W)
    out_data = conv(in_data)
    print('output shape:', out_data.shape)  # (batch_size, out_channels, out_height, out_width)

if __name__ == "__main__":
    base()
    linear_layer()
    conv2d_layer()