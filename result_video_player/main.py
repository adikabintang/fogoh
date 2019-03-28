# 192.168.0.101
import cv2
import asyncio
import pickle
import numpy
from nats.aio.client import Client as NATS
from stan.aio.client import Client as STAN
import sys
import base64

vid_writer = cv2.VideoWriter(
        "res.avi",
        cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
        10, # fps
        (640, 480))

async def run(loop):
    nc = NATS()
    await nc.connect("192.168.0.101:4222", loop=loop)
    sc = STAN()
    await sc.connect("test-cluster", "client-3", nats=nc)

    async def message_handler(msg):
        global vid_writer
        data = msg.data
        try:
            jpg_original = base64.b64decode(data)
            jpg_as_np = numpy.frombuffer(jpg_original, dtype=numpy.uint8)
            image_buffer = cv2.imdecode(jpg_as_np, flags=-1)
            
            vid_writer.write(image_buffer.astype(numpy.uint8))
            #cv2.imshow("oo", image_buffer)
            cv2.waitKey(1)
        except:
            print("Unexpected error:", sys.exc_info())
            cv2.destroyAllWindows()

    await sc.subscribe("res.vid", start_at='last_received', cb=message_handler)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    loop.run_forever()