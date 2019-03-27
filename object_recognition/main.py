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

obj_detection = ObjectDetection()
process_time_avg = 0
counter = 0

async def run(loop):
    nc = NATS()
    await nc.connect("192.168.0.101:4222", loop=loop)
    sc = STAN()
    await sc.connect("test-cluster", "client-2", nats=nc)

    async def message_handler(msg):
        global process_time_avg, counter
        try:
            data = msg.data #data
            before_ms = int(round(time.time() * 1000))
            
            jpg_original = base64.b64decode(data)
            jpg_as_np = numpy.frombuffer(jpg_original, dtype=numpy.uint8)
            image_buffer = cv2.imdecode(jpg_as_np, flags=-1)
            #cv2.imshow("oo", image_buffer)

            frame = cv2.imdecode(
                numpy.frombuffer(data, dtype=numpy.uint8),
                cv2.IMREAD_COLOR)
            #vid_writer.write(frame.astype(numpy.uint8))

            ####
            # Create a 4D blob from a frame.
            blob = cv2.dnn.blobFromImage(
                image_buffer, 1/255, 
                (obj_detection.inp_width, obj_detection.inp_height), 
                [0, 0, 0], 1, crop=False)
            
            # Sets the input to the network
            obj_detection.net.setInput(blob)
            
            # Runs the forward pass to get output of the output layers
            outs = obj_detection.net.forward(
                obj_detection.getOutputsNames())
            
            # Remove the bounding boxes with low confidence
            obj_detection.postprocess(image_buffer, outs)
            
            # vid_writer.write(frame.astype(np.uint8))
            ####
            
            #cv2.imshow("oi", frame)
            ret, buff = cv2.imencode('.jpg', image_buffer)
            jpg_as_text = base64.b64encode(buff)
            
            await sc.publish("res.vid", jpg_as_text)
            
            after_ms = int(round(time.time() * 1000))
            process_time = after_ms - before_ms
            counter += 1
            process_time_avg = (process_time_avg * (counter - 1) + process_time) / counter
            print("process time: %d" % process_time)
            print("couter: %d, avg: %d" % (counter, process_time))
            #cv2.waitKey(1)
        except:
            print("Unexpected error:", sys.exc_info()[0])

    await sc.subscribe("raw.video", start_at='last_received', cb=message_handler)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    loop.run_forever()