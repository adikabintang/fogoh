# Taken from: https://github.com/spmallick/learnopencv/blob/master/ObjectDetection-YOLO/getModels.sh
wget https://pjreddie.com/media/files/yolov3.weights -O ./video_processing/yolov3.weights
wget https://github.com/pjreddie/darknet/blob/master/cfg/yolov3.cfg?raw=true -O ./video_processing/yolov3.cfg
wget https://github.com/pjreddie/darknet/blob/master/data/coco.names?raw=true -O ./video_processing/coco.names