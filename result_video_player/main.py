# 192.168.0.101
import cv2
import asyncio
import pickle
import numpy
from nats.aio.client import Client as NATS
from stan.aio.client import Client as STAN
import sys
import base64
import one_frame_pb2
import time

vid_writer = cv2.VideoWriter(
        "res.avi",
        cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
        12, # fps
        (640, 480))

t0 = int(round(time.time() * 1000))
counter = 0
latency = 0
avg = 1

async def run(loop):
    nc = NATS()
    await nc.connect("192.168.0.101:4222", loop=loop)
    sc = STAN()
    await sc.connect("test-cluster", 
        "player" + str((round(time.time() * 1000))), nats=nc)

    async def message_handler(msg):
        global vid_writer, t0, counter, avg
        # data = msg.data
        counter += 1
        if counter > 1:
            now = int(round(time.time() * 1000))
            latency = now - t0
            t0 = now
            avg = (avg * (counter - 1) \
                + latency) / counter
        else:
            t0 = int(round(time.time() * 1000))
            
        try:
            # jpg_original = base64.b64decode(data)
            proto_data = base64.b64decode(msg.data)
            single_frame_data = one_frame_pb2.OneFrame()
            single_frame_data.ParseFromString(proto_data)
            if sys.argv[1] == single_frame_data.video_source_id:
                jpg_original = base64.b64decode(
                    single_frame_data.frame_jpg_in_base64)

                jpg_as_np = numpy.frombuffer(jpg_original, dtype=numpy.uint8)
                image_buffer = cv2.imdecode(jpg_as_np, flags=-1)
                
                #vid_writer.write(image_buffer.astype(numpy.uint8))
                # displaying fps
                cv2.putText(image_buffer, "fps: " + str(1000 / avg),
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (125, 255, 51), 2)
                cv2.imshow("oo", image_buffer)
                cv2.waitKey(1)

        except:
            print("Unexpected error:", sys.exc_info())
            cv2.destroyAllWindows()

    await sc.subscribe("res.vid", start_at='last_received',
         queue="video_player", cb=message_handler)
    #await nc.subscribe("res.vid", cb=message_handler)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    loop.run_forever()