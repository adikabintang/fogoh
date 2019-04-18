import cv2
import numpy
import os

class ObjectDetection:
    conf_threshold = 0.5  #Confidence threshold
    nms_threshold = 0.4   #Non-maximum suppression threshold
    inp_width = 256       #Width of network's input image, used in main.py
    inp_height = 256      #Height of network's input image, used in main.py
    
    classes_file = os.path.join(os.path.dirname(__file__), "coco.names")
    classes = None

    # Give the configuration and weight files for the model 
    # and load the network using them.
    model_configuration = os.path.join(os.path.dirname(__file__), "yolov3.cfg")
    model_weights = os.path.join(os.path.dirname(__file__), "yolov3.weights")
    net = None

    def __init__(self):
        with open(self.classes_file, 'rt') as f:
            self.classes = f.read().rstrip('\n').split('\n')
        
        self.net = cv2.dnn.readNetFromDarknet(
            self.model_configuration, self.model_weights)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
    
    # Get the names of the output layers
    def getOutputsNames(self):
        # Get the names of all the layers in the network
        layersNames = self.net.getLayerNames()
        # Get the names of the output layers,
        # i.e. the layers with unconnected outputs
        return [layersNames[i[0] - 1] \
            for i in self.net.getUnconnectedOutLayers()]

    def draw_pred(self, frame, class_id, conf, left, top, right, bottom):
        cv2.rectangle(
            frame, (left, top), (right, bottom), (255, 178, 50), 3)
    
        label = '%.2f' % conf
            
        # Get the label for the class name and its confidence
        if self.classes:
            assert(class_id < len(self.classes))
            label = '%s:%s' % (self.classes[class_id], label)

        #Display the label at the top of the bounding box
        label_size, base_line = cv2.getTextSize(
            label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        top = max(top, label_size[1])
        cv2.rectangle(
            frame,
            (left, top - round(1.5*label_size[1])), 
            (left + round(1.5*label_size[0]), top + base_line), 
            (255, 255, 255), cv2.FILLED)
        cv2.putText(
            frame, label, (left, top),
            cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 1)
    
    def preprocess(self, jpg_original):
        jpg_as_np = numpy.frombuffer(jpg_original, dtype=numpy.uint8)
        image_buffer = cv2.imdecode(jpg_as_np, flags=-1)
        #cv2.imshow("oo", image_buffer)

        # Create a 4D blob from a frame.
        blob = cv2.dnn.blobFromImage(
            image_buffer, 1/255,
            (self.inp_width, self.inp_height),
            [0, 0, 0], 1, crop=False)
        
        # Sets the input to the network
        self.net.setInput(blob)
        
        # Runs the forward pass to get output of the output layers
        outs_layer = self.net.forward(
            self.getOutputsNames())
        
        return image_buffer, outs_layer
    
    # Remove the bounding boxes with low confidence using non-maxima suppression
    def postprocess(self, frame, outs):
        frame_height = frame.shape[0]
        frame_width = frame.shape[1]

        # Scan through all the bounding boxes output from the network 
        # and keep only the ones with high confidence scores. Assign the box's 
        # class label as the class with the highest score.
        class_id_list = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = numpy.argmax(scores)
                confidence = scores[class_id]
                if confidence > self.conf_threshold:
                    center_x = int(detection[0] * frame_width)
                    center_y = int(detection[1] * frame_height)
                    width = int(detection[2] * frame_width)
                    height = int(detection[3] * frame_height)
                    left = int(center_x - width / 2)
                    top = int(center_y - height / 2)
                    class_id_list.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([left, top, width, height])

        # Perform non maximum suppression to eliminate redundant overlapping 
        # boxes with lower confidences.
        indices = cv2.dnn.NMSBoxes(
            boxes, confidences, self.conf_threshold, self.nms_threshold)
        for i in indices:
            i = i[0]
            box = boxes[i]
            left = box[0]
            top = box[1]
            width = box[2]
            height = box[3]
            self.draw_pred(
                frame, class_id_list[i],
                confidences[i], left, top, left + width, top + height)
            
