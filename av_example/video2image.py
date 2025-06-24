import av
import sys

def using_av(video_path: str, output_path: str):
    """
    Extract frames from a video file using PyAV and save them as images.
    
    :param video_path: Path to the input video file.
    :param output_path: Directory where the extracted images will be saved.
    """
    container = av.open(video_path)
    print("format: ", container.format)
    print("format.name: ", container.format.name)
    print("format.long_name: ", container.format.long_name)
    print("duration: ", container.duration)  # Duration in microseconds
    print("bit_rate: ", container.bit_rate)  # Bit rate in bits per second
    print("size: ", container.size)  # Size in bytes
    print("streams: ", len(container.streams))  # Number of streams in the container
    print("metadata: ", container.metadata)  # Metadata dictionary
    print("start_time: ", container.start_time)  # Start time in microseconds

    for stream in container.streams:
        print("----------stream info----------")
        print("stream.index: ", stream.index)
        print("stream.type: ", stream.type)  # Stream type (video, audio, etc.)
        print("stream.codec: ", stream.codec)
        print("stream.codec.name: ", stream.codec.name)  # Codec name
        print("stream.codec.long_name: ", stream.codec.long_name)  # Codec long name
        print("stream.codec.type: ", stream.codec.type)  # Codec type (video, audio, etc.)
        print("duration: ", stream.duration)  # Duration in time base units
        print("time_base: ", stream.time_base)  # Time base of the stream
        print("start_time: ", stream.start_time)  # Start time in time base units
        print("frames: ", stream.frames)  # Number of frames in the stream
    
    frame_count = 0    
    for frame in container.decode(video=0):
        if frame_count == 10:
            break
        frame_count += 1
        print("----------frame {}----------".format(frame_count))
        print("frame.pts: ", frame.pts) # presentation timestamp
        print("frame.dts: ", frame.dts) # decode timestamp
        print("frame.time: ", frame.time) # time in seconds
        print("frame.width: ", frame.width)
        print("frame.height: ", frame.height)
        print("frame.format: ", frame.format)
        print("frame.format.name: ", frame.format.name)
        print("frame.format.bits_per_pixel: ", frame.format.bits_per_pixel)
        print("frame.key_frame: ", frame.key_frame)
        
        # I帧：intra frame，关键帧，完整保存图像数据，不依赖其他帧
        # P帧：predicted frame，预测帧，保留与前帧的差异数据，依赖前一帧来解码
        # B帧：bidirectional frame，双向预测帧，依赖前后两帧来解码
        print("frame.pict_type: ", frame.pict_type)
        
        image = frame.to_image()
        print("image.mode: ", image.mode)  # 图像模式，如RGB, L等
        print("image.size: ", image.size)  # 图像尺寸 (width, height)
        print("image.format: ", image.format)  # 图像格式，如JPEG, PNG。通常为NODE，除非直接文件打开
        if frame_count <= 10:
            image.save(f"{output_path}/frame_{frame_count}.jpg")
        gray_image = image.convert("L")
        if frame_count <= 10:
            gray_image.save(f"{output_path}/frame_{frame_count}_gray.jpg")
    
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python video2image.py <video_path> <output_path>")
    else:
        video_path = sys.argv[1]
        output_path = sys.argv[2]
        print("video_path: ", video_path)
        print("output_path: ", output_path)
        using_av(video_path, output_path)