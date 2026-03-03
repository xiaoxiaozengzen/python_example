"""
将ONNX模型转换为TensorRT引擎文件,这种转换后有可能对应的trt模型在实际加载的时候报错。
推荐使用trtexec命令行的方式将ONNX模型转换为TensorRT引擎文件，命令如下：
trtexec --onnx=deploy.onnx --saveEngine=deploy.engine --explicitBatch
"""

import tensorrt as trt

onnx_path = "./deploy.onnx"
engine_path = "./deploy.engine"

print("TensorRT version:", trt.__version__)

logger  = trt.Logger(trt.Logger.VERBOSE)
builder = trt.Builder(logger)
network = builder.create_network(1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH))
parser  = trt.OnnxParser(network, logger)
config  = builder.create_builder_config()

# batch是动态的，所以需要设置优化配置文件
profile = builder.create_optimization_profile()

# 解析ONNX模型
print("Parsing ONNX model...")
with open(onnx_path, "rb") as f:
    parsed = parser.parse(f.read())

if not parsed:
    print("Failed to parse ONNX model.")
    for i in range(parser.num_errors):
        print(parser.get_error(i))
    raise RuntimeError("ONNX parse failed")
print("ONNX model parsed successfully.")

inp = network.get_input(0)
print(f"Input name: {inp.name}, shape: {inp.shape}, dtype: {inp.dtype}")
input_name = network.get_input(0).name
print(f"Input name: {input_name}")
profile.set_shape(input_name, min=(1,10), opt=(10,10), max=(100,10))
config.add_optimization_profile(profile)

engineString = builder.build_serialized_network(network, config)

if engineString is None:
    raise RuntimeError("TensorRT engine build failed, build_serialized_network returned None")

with open(engine_path, "wb") as f:
    f.write(engineString)

print(f"Engine saved to: {engine_path}")