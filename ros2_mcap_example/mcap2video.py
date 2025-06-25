import fractions
import os
import sys

import av
import cv2
from mcap_ros2.decoder import DecoderFactory
from mcap.reader import make_reader

clock_rate = 1_000_000_000
time_base = fractions.Fraction(1, clock_rate)


def main(file_path: "str", output_path: "str"):
    codecs = {}
    frame_count = 0
    with open(file_path, "rb") as f:
        reader = make_reader(f, decoder_factories=[DecoderFactory()])
        for schema, channel, _, ros_msg in reader.iter_decoded_messages():
            if not schema or schema.name != "foxglove_msgs/msg/CompressedVideo":
                continue
            frame_count += 1
            if frame_count == 1:
                print("ros_msg.timestamp:", ros_msg.timestamp)
                print("ros_msg.frame_id:", ros_msg.frame_id)
                print("ros_msg.format:", ros_msg.format)
            print(f"Processing {channel.topic} at {ros_msg.timestamp.sec}.{ros_msg.timestamp.nanosec}")
            assert ros_msg.format == "h265"
            d = os.path.join(output_path, channel.topic.split("/")[-2])
            if channel.topic not in codecs:
                os.makedirs(d, exist_ok=True)
                codec = av.CodecContext.create("hevc", "r")
                codecs[channel.topic] = codec
            else:
                codec = codecs[channel.topic]

            pts = ros_msg.timestamp.sec * clock_rate + ros_msg.timestamp.nanosec
            packet = av.Packet(len(ros_msg.data))
            packet.update(ros_msg.data)
            packet.pts = pts
            packet.time_base = time_base
            new_frames = list(codec.decode(packet))
            if not new_frames:
                continue
            assert len(new_frames) == 1
            assert new_frames[0].pts == packet.pts
            img = new_frames[0].to_ndarray(format="bgr24")
            assert cv2.imwrite(os.path.join(d, f"{pts}.jpg"), img)


if __name__ == "__main__":
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    main(input_path, output_path)