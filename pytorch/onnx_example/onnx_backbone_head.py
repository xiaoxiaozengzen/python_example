import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from torchvision import datasets, transforms
import os
import numpy as np

"""
    模拟对数字进行区分
"""

# 1.定义bacbone
class Backbone(nn.Module):
    def __init__(self, out_dim=128):
        super(Backbone, self).__init__()
        self.net = nn.Sequential(
            nn.Conv2d(1, 32, 3, padding=1),  # 输入通道数为3，输出通道数为32，卷积核大小为3x3，padding为1
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
    
# 3.加载训练数据集
device = "cuda" if torch.cuda.is_available() else "cpu"
print("train in device: ", device)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
ARTIFACTS_DIR = os.path.join(os.path.dirname(__file__), "articfacts")
MNIST_MEAN=0.1397
MNIST_STD=0.3081
# 图像预处理流水线：
# 1. 图像转换：从PIL的HxWxC,uint8转换到 CxHxW,float32,取值范围[0.0, 1.0]
# 2. 对每个通道做 x = (x - mean) / std
tf = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((MNIST_MEAN,), (MNIST_STD))
])
train_set = datasets.MNIST(DATA_DIR, train=True, download=True, transform=tf)
test_set = datasets.MNIST(DATA_DIR, train=False, download=True, transform=tf)
train_loader = DataLoader(train_set, batch_size=128, shuffle=True, num_workers=2)
test_loader = DataLoader(test_set, batch_size=256, shuffle=False, num_workers=2)

# 4.定义模型跟对应的损失函数
backbone = Backbone(out_dim=128).to(device)
head = Head(in_dim=128, out_dim=10).to(device)
opt = torch.optim.Adam(list(backbone.parameters()) + list(head.parameters()), lr=0.001)  # 使用Adam优化器，学习率为0.001
loss_fn = nn.CrossEntropyLoss()  # 使用交叉熵损失函数

# 5.训练
EPOCHS=3
for epoch in range(EPOCHS):
    # 训练
    backbone.train()
    head.train()
    running = 0.0
    for xb,yb in train_loader:
        xb,yb = xb.to(device),yb.to(device)
        logits = head(backbone(xb))
        loss = loss_fn(logits, yb)
        opt.zero_grad()
        loss.backward()
        opt.step()
        running += loss.item() * xb.size(0)
    train_loss = running / len(train_set)
    
    # 评估
    backbone.eval()
    head.eval()
    correct=0
    with torch.inference_mode():
        for xb,yb in test_loader:
            xb, yb = xb.to(device), yb.to(device)
            pred = head(backbone(xb)).argmax(dim=1)
            correct += (pred == yb).sum().item()
    acc = correct / len(test_set)
    print(f"[train] epoch {epoch+1}/{EPOCHS} loss={train_loss:.4f}  test_acc={acc*100:.2f}%")
    
torch.save(backbone.state_dict(), os.path.join(ARTIFACTS_DIR, "backbone.pt"))
torch.save(head.state_dict(), os.path.join(ARTIFACTS_DIR, "head.pt"))
print(f"[train] save pt to dir={ARTIFACTS_DIR}")

# 6. 简单测试
sample_img, sample_label = test_set[0]
sample_batch = sample_img.unsqueeze(0).to(device)
backbone.eval()
head.eval()
with torch.inference_mode():
    feat = backbone(sample_batch)
    logits = head(feat)
    probs = torch.softmax(logits, dim=1)
    pred = probs.argmax(dim=1).item()
    conf = probs.max(dim=1).values.item()
sample_np = sample_batch.detach().cpu().numpy().astype(np.float32)
assert sample_np.shape == (1, 1, 28, 28), sample_np.shape
assert sample_np.dtype == np.float32
print(f"[train] pred {pred}")
print(f"[train] sample_label {sample_label}")
sample_np.tofile(os.path.join(ARTIFACTS_DIR, "sample_image.bin"))
print(f"[train] save sample_image.bin to dir={ARTIFACTS_DIR}")
img = sample_np[0, 0, :, :]
img = img * MNIST_STD + MNIST_MEAN  # 反归一化
img = np.clip(img, 0.0, 1.0)  # 将像素值限制在[0, 1]范围内
from PIL import Image
img_u8 = (img * 255.0).astype(np.uint8)  # 转换为uint8类型 
pil = Image.fromarray(img_u8, mode="L")  # 创建灰度图像
pil.save(os.path.join(ARTIFACTS_DIR, "sample_image.png"))
    
# 7.导出onnx
export_backbone = Backbone(out_dim=128)
export_head = Head(in_dim=128, out_dim=10)

dump_image = torch.randn(1, 1, 28, 28)  # 随机生成一个输入图像，批量大小为1，图像大小为32x32，通道数为3
dump_feat = torch.randn(1, 128)  # 随机生成一个特征向量，批量大小为1，特征维度为128
export_backbone.load_state_dict(torch.load(os.path.join(ARTIFACTS_DIR, "backbone.pt"), map_location="cpu"))
export_head.load_state_dict(torch.load(os.path.join(ARTIFACTS_DIR, "head.pt"), map_location="cpu"))
export_backbone.eval()  # 设置backbone为评估模式
export_head.eval()  # 设置head为评估模式

torch.onnx.export(
    export_backbone,  # 导出的模型为backbone
    dump_image,  # 输入数据为dump_image
    "backbone.onnx",  # 导出的onnx文件名为backbone.onnx
    input_names=["input"],  # 输入张量的名称为input
    output_names=["feature"],  # 输出张量的名称为feature
    # dynamic_axes={"input": {0: "batch_size"}, "feature": {0: "batch_size"}},  # 动态轴，支持不同批量大小的输入输出
    opset_version=11  # ONNX算子集版本为11
)

torch.onnx.export(
    export_head,  # 导出的模型为head
    dump_feat,  # 输入数据为dump_feat
    "head.onnx",  # 导出的onnx文件名为head.onnx
    input_names=["feature"],  # 输入张量的名称为feature
    output_names=["logits"],  # 输出张量的名称为logits
    # dynamic_axes={"feature": {0: "batch_size"}, "logits": {0: "batch_size"}},  # 动态轴，支持不同批量大小的输入输出
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