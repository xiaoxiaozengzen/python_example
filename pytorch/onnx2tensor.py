import tensorrt as trt

onnx_path = "./deploy.onnx"
engine_path = "./deploy.engine"

logger  = trt.Logger(trt.Logger.VERBOSE)
builder = trt.Builder(logger)
network = builder.create_network(1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH))
parser  = trt.OnnxParser(network, logger)
config  = builder.create_builder_config()

with open(onnx_path, "rb") as f:
    parsed = parser.parse(f.read())

if not parsed:
    print("Failed to parse ONNX model.")
    for i in range(parser.num_errors):
        print(parser.get_error(i))
    raise RuntimeError("ONNX parse failed")

engineString = builder.build_serialized_network(network, config)

if engineString is None:
    raise RuntimeError("TensorRT engine build failed, build_serialized_network returned None")

with open(engine_path, "wb") as f:
    f.write(engineString)

print(f"Engine saved to: {engine_path}")