import onnx
import onnxruntime
import torch
import torch.nn as nn

onnx_file_name = "deploy.onnx"
onnx_model = onnx.load(onnx_file_name)

# ----------------------------检验onnx模型的可用性------------------#
# 我们可以使用异常处理的方法进行检验
try:
    # 当我们的模型不可用时，将会报出异常
    onnx.checker.check_model(onnx_model)
except onnx.checker.ValidationError as e:
    print("The model is invalid: %s"%e)
else:
    # 模型可用时，将不会报出异常，并会输出“The model is valid!”
    print("The model is valid!")
    
# -----------------------------查看onnx模型的输入输出信息------------------#
print("ORT Device: %s" % onnxruntime.get_device())
print("ORT Providers: %s" % onnxruntime.get_available_providers())
print("ONNX Model Inputs:")
for input in onnx_model.graph.input:
    print(input.name, [dim.dim_value for dim in input.type.tensor_type.shape.dim])
print("ONNX Model Outputs:")
for output in onnx_model.graph.output:
    print(output.name, [dim.dim_value for dim in output.type.tensor_type.shape.dim])
    
# ----------------------------使用onnxruntime进行推理------------------#
# 需要进行推理的onnx模型文件名称
onnx_file_name = "deploy.onnx"

# onnxruntime.InferenceSession用于获取一个 ONNX Runtime 推理器
ort_session = onnxruntime.InferenceSession(onnx_file_name)  

# 构建字典的输入数据，字典的key需要与我们构建onnx模型时的input_names相同
# 定义输入层大小、隐藏层大小、输出层大小和批量大小
n_in, n_h, n_out, batch_size = 10, 5, 1, 10
deploy_input = torch.randn(batch_size, n_in)
# ptorch模型的输入是tensor，而onnxruntime的输入需要是numpy数组，因此我们需要将tensor转换为numpy数组
ort_inputs = {'input': deploy_input.numpy()} 

# run是进行模型的推理，第一个参数为输出张量名的列表，一般情况可以设置为None
# 第二个参数为构建的输入值的字典
# 由于返回的结果被列表嵌套，因此我们需要进行[0]的索引
ort_output = ort_session.run(None,ort_inputs)[0]
# output = {ort_session.get_outputs()[0].name}
# ort_output = ort_session.run([output], ort_inputs)[0]
print("ONNX Runtime Output:\n", ort_output)
