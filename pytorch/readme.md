# Overview

```bash
# 对onnx模型做基线检查
trtexec --onnx=deploy.onnx --verbose --minShapes=input:1x10 --optShapes=input:10x10 --maxShapes=input:100x10

# 将onnx模型转换成tensorRT模型
trtexec --onnx=/mnt/workspace/cgz_workspace/Exercise/python_example/pytorch/deploy.onnx --saveEngine=deploy.engine  --verbose --minShapes=input:1x10 --optShapes=input:10x10 --maxShapes=input:100x10

# 执行下列命令，不报错就证明模型和当前平台是适配的
trtexec --loadEngine=xxx.engine --verbose

```

# netron
这个工具可以对onnx模型进行可视化。对于可视化中显示的一些东西：

Cast：算子节点名，表示类型转换。对应x.float()或者x.to(torch.float32)
Conv：算子节点名，表示卷积层，对应nn.Conv2d或者torch.nn.functional.conv2d(...)
ConvTranspose：表示反卷积，用于方法特征图，经过改算子后，H和W一般都会变大。等价nn.ConvTranspose2d()
BatchNormalization：批归一化层，对每个一通道的特征做归一化
Relu：算子节点名，表示激活函数，等价nn.ReLU(等价于max(0,x))
Mul：算子节点名，表示乘法，通常是逐元素乘，等价于torch.mul(x,y)
Sigmoid：算子节点名，表示sigmoid，等价于nn.Sigmoid()
Gemm：算子节点名，等价于nn.Linear
Add：等价于x+y
Reshape：等价于x.view或者x.reshape
Transpose：等价于x.permute或者transpose()
Concat：等价于torch.cat()
Slice：表示从一个张量按照某个范围截取一部分数据，类似x[start:end]
