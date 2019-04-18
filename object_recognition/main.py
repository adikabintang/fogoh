from video_processing.object_detection import ObjectDetection
import cv2
import asyncio
import pickle
import numpy
from nats.aio.client import Client as NATS
from stan.aio.client import Client as STAN
import base64
import time
import sys
import os
import uvloop

obj_detection = ObjectDetection()
process_time_avg = 0
counter = 0

async def run(loop):
    nats_endpoint = os.environ['NATS_ENDPOINT'] \
        if "NATS_ENDPOINT" in os.environ else "192.168.0.101:4222"
    nats_cluster_name = os.environ['NATS_CLUSTER_NAME'] \
        if "NATS_CLUSTER_NAME" in os.environ else "test-cluster"
    nats_client_id = os.environ['NATS_CLIENT_ID'] \
        if "NATS_CLIENT_ID" in os.environ else "object-recognition"
        
    nc = NATS()
    await nc.connect(nats_endpoint, loop=loop)
    sc = STAN()
    await sc.connect(nats_cluster_name, nats_client_id, nats=nc)
    
    async def message_handler(msg):
        global process_time_avg, counter
        try:
            data = msg.data #data
            before_ms = int(round(time.time() * 1000))
            
            jpg_original = base64.b64decode(data)
            
            # Runs the forward pass to get output of the output layers
            image_buffer, outs_layer = obj_detection.preprocess(jpg_original)
            
            # Remove the bounding boxes with low confidence
            obj_detection.postprocess(image_buffer, outs_layer)
            
            #cv2.imshow("oi", frame)
            ret, buff = cv2.imencode('.jpg', image_buffer)
            jpg_as_text = base64.b64encode(buff)
            
            await sc.publish("res.vid", jpg_as_text)
            
            after_ms = int(round(time.time() * 1000))
            process_time = after_ms - before_ms
            counter += 1
            process_time_avg = (process_time_avg * (counter - 1) \
                + process_time) / counter
            print("process time: %d" % process_time)
            print("counter: %d, avg: %d" % (counter, process_time))
            
        except:
            print("Unexpected error:", sys.exc_info()[0])

    await sc.subscribe("raw.video", \
        start_at='last_received', cb=message_handler)

if __name__ == '__main__':
    loop = uvloop.new_event_loop()
    #loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run(loop))
    loop.run_forever()