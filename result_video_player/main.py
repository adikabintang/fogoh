# 192.168.0.101
import cv2
import asyncio
import pickle
import numpy
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers

async def run(loop):
    nc = NATS()
    await nc.connect("192.168.0.101:4222", loop=loop)

    vid_writer = cv2.VideoWriter(
        "res.avi",
        cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
        10, # fps
        (640, 480))

    async def message_handler(msg):
        subject = msg.subject # topic
        data = msg.data #data
        frame = cv2.imdecode(
            numpy.frombuffer(data, dtype=numpy.uint8),
            cv2.IMREAD_COLOR)
        
        cv2.imshow("jir", frame)
        vid_writer.write(frame.astype(numpy.uint8))
        cv2.waitKey(1)

    # Simple publisher and async subscriber via coroutine.
    sid = await nc.subscribe("res.*", cb=message_handler)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    loop.run_forever()