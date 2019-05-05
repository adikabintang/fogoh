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
import one_frame_pb2

obj_detection = ObjectDetection()
process_time_avg = 0
counter = 0

async def run(loop):
    nats_endpoint = os.environ['NATS_ENDPOINT'] \
        if "NATS_ENDPOINT" in os.environ else "192.168.0.101:4222"
    nats_cluster_name = os.environ['NATS_CLUSTER_NAME'] \
        if "NATS_CLUSTER_NAME" in os.environ else "test-cluster"
    nats_client_id = os.environ['NATS_CLIENT_ID'] \
        if "NATS_CLIENT_ID" in os.environ \
            else "obj_recog" + str((round(time.time() * 1000)))
        
    nc = NATS()
    await nc.connect(nats_endpoint, loop=loop)
    sc = STAN()
    await sc.connect(nats_cluster_name, nats_client_id, nats=nc)
    
    async def message_handler(msg):
        global process_time_avg, counter
        try:
            # data = msg.data #data
            before_ms = int(round(time.time() * 1000))
            
            # jpg_original = base64.b64decode(data)

            proto_data = base64.b64decode(msg.data)
            single_frame_data = one_frame_pb2.OneFrame()
            single_frame_data.ParseFromString(proto_data)
            jpg_frame = base64.b64decode(
                single_frame_data.frame_jpg_in_base64)
            
            result_buff_jpg = obj_detection.detec(jpg_frame) 
            jpg_as_text = base64.b64encode(result_buff_jpg)

            single_frame_data.frame_jpg_in_base64 = jpg_as_text
            
            #await sc.publish("res.vid", jpg_as_text)
            await sc.publish("res.vid",
                base64.b64encode(single_frame_data.SerializeToString()))
            
            after_ms = int(round(time.time() * 1000))
            process_time = after_ms - before_ms
            counter += 1
            process_time_avg = (process_time_avg * (counter - 1) \
                + process_time) / counter
            print("process time: %d" % process_time)
            print("nth: %d, counter: %d, avg: %d" 
                % (single_frame_data.frame_order_nth, counter, process_time))
            
        except:
            print("Unexpected error:", sys.exc_info()[0])

    await sc.subscribe("raw.video", \
        start_at='last_received', queue="obj_recog", cb=message_handler)

if __name__ == '__main__':
    loop = uvloop.new_event_loop()
    #loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run(loop))
    loop.run_forever()