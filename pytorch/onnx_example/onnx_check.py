import onnx
import onnxruntime
import torch
import torch.nn as nn
import argparse
import sys
from os.path import exists

def onnx_load(onnx_file_name):
    if not exists(onnx_file_name):
        print("The onnx file does not exist: %s" % onnx_file_name)
        sys.exit(1)
    
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
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load and check ONNX model")
    parser.add_argument("--onnx_file_name", type=str, default="deploy.onnx", help="Path to the ONNX model file")
    args = parser.parse_args()

    onnx_load(args.onnx_file_name)


