"""
inspiration: 
https://github.com/spmallick/learnopencv/tree/master/ObjectDetection-YOLO
"""
from video_processing.object_detection import ObjectDetection
import cv2
import asyncio
import pickle
import numpy
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers

obj_detection = ObjectDetection()

async def run(loop):
    nc = NATS()
    await nc.connect("192.168.0.101:4222", loop=loop)

    async def message_handler(msg):
        # subject = msg.subject # topic
        data = msg.data # data
        
        frame = cv2.imdecode(
            numpy.frombuffer(data, dtype=numpy.uint8),
            cv2.IMREAD_COLOR)
        
        ####
        # Create a 4D blob from a frame.
        blob = cv2.dnn.blobFromImage(
            frame, 1/255, 
            (obj_detection.inp_width, obj_detection.inp_height), 
            [0, 0, 0], 1, crop=False)
        
        # Sets the input to the network
        obj_detection.net.setInput(blob)
        
        # Runs the forward pass to get output of the output layers
        outs = obj_detection.net.forward(
            obj_detection.getOutputsNames())
        
        # Remove the bounding boxes with low confidence
        obj_detection.postprocess(frame, outs)
        
        ####
        
        #cv2.imshow("oi", frame)
        ret, buff = cv2.imencode('.jpg', frame)
        await nc.publish("res.vid", buff.tobytes())
        cv2.waitKey(1)

    # Simple publisher and async subscriber via coroutine.
    sid = await nc.subscribe("raw.*", cb=message_handler)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    loop.run_forever()