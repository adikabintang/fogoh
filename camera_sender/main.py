import cv2
import logging
import socket
import pickle
import struct
import time

def send_video():
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    vid = cv2.VideoCapture(0) # 0 -> webcam, default: 30 fps
    vid.set(cv2.CAP_PROP_FPS, 10)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("127.0.0.1", 8080))
        
        i = 0
        while i < 300:
            status, frame = vid.read()
            status, frame = cv2.imencode('.jpg', frame, encode_param)
            #status, frame = cv2.imencode('.jpg', frame)
            if not status:
                logging.error("read frame error")
                return
            else:
                data = pickle.dumps(frame, 0)
                size = len(data)
                s.sendall(struct.pack(">L", size) + data)
                time.sleep(0.1)
                cv2.waitKey(1000)
            
            i += 1

    vid.release()

def main():
    send_video()
    
if __name__ == "__main__":
    main()