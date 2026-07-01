import onnx
import onnxruntime
import torch
import torch.nn as nn
import argparse
import sys
from os.path import exists    
      

# ----------------------------使用onnxruntime进行推理------------------#
# 需要进行推理的onnx模型文件名称
onnx_file_name = "../model/deploy.onnx"

# onnxruntime.InferenceSession用于获取一个 ONNX Runtime 推理器
ort_session = onnxruntime.InferenceSession(onnx_file_name)

ort_inputs = ort_session.get_inputs()
print("ORT Session Inputs:")
for input in ort_inputs:
    print(input.name, input.shape, input.type)
ort_outputs = ort_session.get_outputs()
print("ORT Session Outputs:")
for output in ort_outputs:
    print(output.name, output.shape, output.type) 

# 构建字典的输入数据，字典的key需要与我们构建onnx模型时的input_names相同
# 定义输入层大小、隐藏层大小、输出层大小和批量大小
n_in, n_h, n_out, batch_size = 10, 5, 1, 10
deploy_input = torch.randn(batch_size, n_in)
# ptorch模型的输入是tensor，而onnxruntime的输入需要是numpy数组，因此我们需要将tensor转换为numpy数组
ort_inputs = {'input': deploy_input.numpy()} 

# run是进行模型的推理，第一个参数为输出张量名的列表，一般情况可以设置为None
# 第二个参数为构建的输入值的字典
ort_output_all = ort_session.run(None,ort_inputs)
print("ONNX Runtime Output:\n", ort_output_all)

# 由于返回的结果被列表嵌套，因此我们需要进行[0]的索引
output_0 =ort_output_all[0]
print("ONNX Runtime Output[0]:\n", output_0)
print("ONNX Runtime Output[0] with 0.5:\n", output_0[:, 0] > 0.5)