import cv2
import asyncio
import pickle
import numpy
from nats.aio.client import Client as NATS
from stan.aio.client import Client as STAN
import sys
import base64
import subprocess
from PIL import Image
import uvloop
import os
import one_frame_pb2
import time

async def run(loop):
    nats_endpoint = os.environ['NATS_ENDPOINT'] \
        if "NATS_ENDPOINT" in os.environ else "192.168.0.101:4222"
    nats_cluster_name = os.environ['NATS_CLUSTER_NAME'] \
        if "NATS_CLUSTER_NAME" in os.environ else "test-cluster"
    nats_client_id = os.environ['NATS_CLIENT_ID'] \
        if "NATS_CLIENT_ID" in os.environ \
            else "streamer" + str((round(time.time() * 1000)))
    streaming_dest_address = os.environ['RTMP_ENDPOINT'] \
        if "RTMP_ENDPOINT" in os.environ \
            else "rtmp://192.168.0.101:1935/show/"

    nc = NATS()
    await nc.connect(nats_endpoint, loop=loop)
    sc = STAN()
    await sc.connect(nats_cluster_name, nats_client_id, nats=nc)

    ffmpeg_process = {}

    async def message_handler(msg):
        nonlocal ffmpeg_process #, p
        #data = msg.data
        try:
            proto_data = base64.b64decode(msg.data)
            single_frame_data = one_frame_pb2.OneFrame()
            single_frame_data.ParseFromString(proto_data)
            jpg_frame = base64.b64decode(
                single_frame_data.frame_jpg_in_base64)

            jpg_as_np = numpy.frombuffer(jpg_frame, dtype=numpy.uint8)
            image_buffer = cv2.imdecode(jpg_as_np, flags=-1)
            
            correct_img = cv2.cvtColor(image_buffer, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(correct_img)

            #streaming_dest_address = "rtmp://localhost:1935/show/"

            video_dest = streaming_dest_address + \
                single_frame_data.video_source_id

            if ffmpeg_process.get(single_frame_data.video_source_id) == None:
                ffmpeg_process[single_frame_data.video_source_id] = \
                    subprocess.Popen(["ffmpeg",
                            "-re",
                            "-i", "-",
                            "-vcodec", "libx264",
                            "-vprofile", "baseline",
                            "-g", "30",
                            "-acodec", "aac",
                            "-strict", "-2",
                            "-f", "flv",
                            video_dest], \
                            stdin=subprocess.PIPE)

            p = ffmpeg_process[single_frame_data.video_source_id]
            im.save(p.stdin, 'JPEG')
        except:
            print("Unexpected error:", sys.exc_info())
            # cv2.destroyAllWindows()

    await sc.subscribe("res.vid", queue="rtmp_stream_send", 
        start_at='last_received', cb=message_handler)
    
if __name__ == '__main__':
    loop = uvloop.new_event_loop()
    loop.run_until_complete(run(loop))
    loop.run_forever()