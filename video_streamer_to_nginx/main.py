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

async def run(loop):
    nats_endpoint = os.environ['NATS_ENDPOINT'] \
        if "NATS_ENDPOINT" in os.environ else "192.168.0.101:4222"
    nats_cluster_name = os.environ['NATS_CLUSTER_NAME'] \
        if "NATS_CLUSTER_NAME" in os.environ else "test-cluster"
    nats_client_id = os.environ['NATS_CLIENT_ID'] \
        if "NATS_CLIENT_ID" in os.environ else "streamer-to-nginx"
    rtmp_endpoint = os.environ['RTMP_ENDPOINT'] \
        if "RTMP_ENDPOINT" in os.environ \
            else "rtmp://192.168.0.101:1935/live/live"

    nc = NATS()
    await nc.connect(nats_endpoint, loop=loop)
    sc = STAN()
    await sc.connect(nats_cluster_name, nats_client_id, nats=nc)
    
    p = subprocess.Popen(
        ['ffmpeg', '-f', 'image2pipe', '-r', '8', \
            '-i', '-', '-f', 'flv', rtmp_endpoint],
        stdin=subprocess.PIPE)

    async def message_handler(msg):
        nonlocal p
        data = msg.data
        try:
            jpg_original = base64.b64decode(data)
            jpg_as_np = numpy.frombuffer(jpg_original, dtype=numpy.uint8)
            image_buffer = cv2.imdecode(jpg_as_np, flags=-1)
            
            correct_img = cv2.cvtColor(image_buffer, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(correct_img)
            im.save(p.stdin, 'JPEG')
        except:
            print("Unexpected error:", sys.exc_info())
            # cv2.destroyAllWindows()

    await sc.subscribe("res.vid", start_at='last_received', cb=message_handler)
    
if __name__ == '__main__':
    loop = uvloop.new_event_loop()
    loop.run_until_complete(run(loop))
    loop.run_forever()