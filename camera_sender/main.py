import cv2
import logging
import socket
import pickle
import struct
import time
import base64
import sys

def send_video():
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    vid = cv2.VideoCapture(0) # 0 -> webcam, default: 30 fps
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect(("127.0.0.1", 8080))

            i = 0
            while i < 200:
                status, frame_asli = vid.read()
                
                print("frame: %d" % i)
                status, frame = cv2.imencode('.jpg', frame_asli, encode_param)
                if not status:
                    logging.error("read frame error")
                    return
                else:
                    jpg_as_text = base64.b64encode(frame)
                    s.sendall(jpg_as_text)
                    # https://stackoverflow.com/questions/16681007/base64-encrypted-allowed-characters
                    s.send(b':,')

                time.sleep(0.1)
                
                i += 1
        except KeyboardInterrupt:
            s.close()
    
    vid.release()

if __name__ == "__main__":
    send_video()