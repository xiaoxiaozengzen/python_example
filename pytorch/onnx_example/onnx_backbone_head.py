import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset

# 1.定义bacbone
class Backbone(nn.Module):
    def __init__(self, out_dim=128):
        super(Backbone, self).__init__()
        self.net = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1),  # 输入通道数为3，输出通道数为32，卷积核大小为3x3，padding为1
            nn.ReLU(),
            nn.MaxPool2d(2),  # 最大池化，池化窗口大小为2x2
            nn.Conv2d(32, 64, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.AdaptiveAvgPool2d(1),  # 自适应平均池化，将特征图大小调整为1x1
            nn.Flatten(),  # 将多维输入一维化
            nn.Linear(64, out_dim)  # 全连接层，将特征维度从64映射到out_dim
        ) 
    
    def forward(self, x):
        return self.net(x)
    
# 2.定义head
class Head(nn.Module):
    def __init__(self, in_dim=128, out_dim=10):
        super(Head, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, 64),  # 全连接层，将特征维度从in_dim映射到64
            nn.ReLU(),
            nn.Linear(64, out_dim)  # 全连接层，将特征维度从64映射到out_dim
        )
    
    def forward(self, x):
        return self.net(x)
    
# 3.训练
backbone = Backbone(out_dim=128)
head = Head(in_dim=128, out_dim=10)
opt = torch.optim.Adam(list(backbone.parameters()) + list(head.parameters()), lr=0.001)  # 使用Adam优化器，学习率为0.001
loss_fn = nn.CrossEntropyLoss()  # 使用交叉熵损失函数

for _ in range(5):
    x = torch.randn(32, 3, 32, 32)  # 随机生成输入数据，批量大小为32，图像大小为32x32，通道数为3
    y = torch.randint(0, 10, (32,))  # 随机生成目标标签，范围为0到9，批量大小为32
    features = backbone(x)  # 通过backbone提取特征
    logits = head(features)
    loss = loss_fn(logits, y)  # 计算损失
    opt.zero_grad()  # 清零梯度
    loss.backward()  # 反向传播，计算梯度
    opt.step()  # 更新模型参数
    
# 4.导出onnx
backbone.eval()  # 设置backbone为评估模式
head.eval()  # 设置head为评估模式

dump_image = torch.randn(1, 3, 32, 32)  # 随机生成一个输入图像，批量大小为1，图像大小为32x32，通道数为3
dump_feat = torch.randn(1, 128)  # 随机生成一个特征向量，批量大小为1，特征维度为128

torch.onnx.export(
    backbone,  # 导出的模型为backbone
    dump_image,  # 输入数据为dump_image
    "backbone.onnx",  # 导出的onnx文件名为backbone.onnx
    input_names=["input"],  # 输入张量的名称为input
    output_names=["feature"],  # 输出张量的名称为feature
    dynamic_axes={"input": {0: "batch_size"}, "feature": {0: "batch_size"}},  # 动态轴，支持不同批量大小的输入输出
    opset_version=11  # ONNX算子集版本为11
)

torch.onnx.export(
    head,  # 导出的模型为head
    dump_feat,  # 输入数据为dump_feat
    "head.onnx",  # 导出的onnx文件名为head.onnx
    input_names=["feature"],  # 输入张量的名称为feature
    output_names=["logits"],  # 输出张量的名称为logits
    dynamic_axes={"feature": {0: "batch_size"}, "logits": {0: "batch_size"}},  # 动态轴，支持不同批量大小的输入输出
    opset_version=11  # ONNX算子集版本为11
)

# # 4.1.导出onnx(整合backbone和head)
# class CombinedModel(nn.Module):
#     def __init__(self, backbone, head):
#         super(CombinedModel, self).__init__()
#         self.backbone = backbone
#         self.head = head

#     def forward(self, x):
#         features = self.backbone(x)
#         logits = self.head(features)
#         return logits
# combined_model = CombinedModel(backbone, head)
# combined_model.eval()  # 设置combined_model为评估模式
# torch.onnx.export(
#     combined_model,  # 导出的模型为combined_model
#     dump_image,  # 输入数据为dump_image
#     "combined_model.onnx",  # 导出的onnx文件名为combined_model.onnx
#     input_names=["input"],  # 输入张量的名称为input
#     output_names=["logits"],  # 输出张量的名称为logits
#     dynamic_axes={"input": {0: "batch_size"}, "logits": {0: "batch_size"}},  # 动态轴，支持不同批量大小的输入输出
#     opset_version=11  # ONNX算子集版本为11
# )