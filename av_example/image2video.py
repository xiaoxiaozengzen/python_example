import av
import sys
import os
from PIL import Image

def using_av(image_path: str, output_path: str):
    container = av.open(output_path, mode='w')
    
    img = Image.open(f"{image_path}/frame_1.jpg")
    
    # 时间戳的精度，帧的pts跟dts都是依照这个time_base为单位计算的
    print("time_base: ", av.time_base)  # 默认时间基准，通常为1/1000000秒
    
    # codec_name，编码器名称：h264, h265, mpeg4, avc等
    # rate，帧率：1表示每秒1帧
    stream = container.add_stream(codec_name='h264', rate=24)
    stream.width = img.width
    stream.height = img.height
    stream.pix_fmt = 'yuv420p'  # 设置像素格式为 YUV 4:2:0 JPEG格式
    # stream.time_base = av.time_base
    stream.bit_rate = 1024 * 1024 * 8 # 编码目标码率，编码器会尽量控制输出码率在这个范围内
    
    frame_count = 0
    packet_count = 0
    while True:
        frame_count += 1
        image_file = f"{image_path}/frame_{frame_count}.jpg"
        if os.path.exists(image_file) is False:
            print(f"No more images found at {image_file}. Stopping processing.")
            break
        
        img = Image.open(image_file)
        if img.size != (stream.width, stream.height):
            img = img.resize((stream.width, stream.height))
            
        # 编码时：frame(原始帧) -> 编码器 -> packet(压缩后的数据块)
        # 解码时：packet(压缩数据块) -> 解码器 -> frame
            
        # 帧：解码后的原始数据，对视频来说是图像帧，对音频来说是音频帧
        # 特点：未压缩，适合直接处理
        video_frame = av.VideoFrame.from_image(img)
        
        # packet：是编码后的数据块，例如压缩后的码流片段(h264, h265等)
        # 特点：已压缩，适合传输和存储，不能直接处理
        for packet in stream.encode(video_frame):
            packet_count += 1
            print(f"============ frame: {frame_count} packet {packet_count}============")
            print("pts: ", packet.pts)
            print("dts: ", packet.dts)
            print("duration: ", packet.duration / av.time_base)  # duration in seconds
            print("size: ", packet.size)  # size in bytes
            print("time_base: ", packet.time_base)  # time base of the packet
            print("is_keyframe: ", packet.is_keyframe)
            
            
            # 将编码后的数据块写入容器
            container.mux(packet)
            
    # Flush the stream to ensure all packets are written
    for packet in stream.encode():
        container.mux(packet)
    container.close()
    
    
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python video2image.py <image_path> <output_path>")
    else:
        image_path = sys.argv[1]
        output_path = sys.argv[2]
        print("image_path: ", image_path)
        print("output_path: ", output_path)
        using_av(image_path, output_path)