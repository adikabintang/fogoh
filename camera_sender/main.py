import cv2
import logging
import socket
import pickle
import struct
import time
import base64
import sys
import one_frame_pb2

def send_video():
    print("s: {}", sys.argv[1])
    video_source = 0 if sys.argv[1] == "cam" else "bakso.mp4"
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    vid = cv2.VideoCapture(video_source) # 0 -> webcam, default: 30 fps
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            #s.connect(("192.168.0.102", 31123))
            s.connect(("192.168.0.101", 3000))

            i = 0
            while i < 1100:
                status, frame_asli = vid.read()
                
                print("frame: %d" % i)
                status, frame = cv2.imencode('.jpg', frame_asli, encode_param)
                if not status:
                    logging.error("read frame error")
                    return
                else:
                    # jpg_as_text = base64.b64encode(frame)
                    single_frame = one_frame_pb2.OneFrame()
                    single_frame.frame_jpg_in_base64 = base64.b64encode(frame)
                    single_frame.video_source_id = "cam" \
                        if sys.argv[1] == "cam" else "bakso"
                    single_frame.millis = cv2.CAP_PROP_POS_MSEC
                    single_frame.frame_order_nth = i

                    s.sendall(
                        base64.b64encode(single_frame.SerializeToString()))

                    # https://stackoverflow.com/questions/16681007/base64-encrypted-allowed-characters
                    s.send(b':')
                    
                time.sleep(0.06)
                
                i += 1
        except KeyboardInterrupt:
            s.close()
    
    vid.release()

if __name__ == "__main__":
    send_video()