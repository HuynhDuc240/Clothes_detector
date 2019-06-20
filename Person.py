from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau, TerminateOnNaN, CSVLogger
from keras import backend as K
from keras.models import load_model
from math import ceil
import numpy as np
from matplotlib import pyplot as plt
from keras_loss_function.keras_ssd_loss import SSDLoss
from keras_layers.keras_layer_AnchorBoxes import AnchorBoxes
from keras_layers.keras_layer_DecodeDetections import DecodeDetections
from keras_layers.keras_layer_DecodeDetectionsFast import DecodeDetectionsFast

from ssd_encoder_decoder.ssd_input_encoder import SSDInputEncoder
from ssd_encoder_decoder.ssd_output_decoder import decode_detections, decode_detections_fast


import cv2
ssd_loss = SSDLoss(neg_pos_ratio=3, alpha=1.0)
img_height = 300
img_width = 300
normalize_coords = True
class Person():
    def __init__(self):
        self.model = load_model('models_trained/person.h5', custom_objects={'AnchorBoxes': AnchorBoxes,
                                               'compute_loss': ssd_loss.compute_loss})
        self.object_detected = []
    
    def predict(self):
        rate_x = self.image.shape[0]/img_width
        rate_y = self.image.shape[1]/img_height
        img = np.array(self.image)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        img = cv2.resize(img, (img_height,img_width))
        img = img.reshape(1,img_width,img_height,3)
        y_pred = self.model.predict(img)
        y_pred_decoded = decode_detections(y_pred,
                                   confidence_thresh=0.6,
                                   iou_threshold=0.45,
                                   top_k=200,
                                   normalize_coords=normalize_coords,
                                   img_height=img_height,
                                   img_width=img_width)
        i=0
        n=0
        for box in y_pred_decoded[i]:
            print(box)
            xmin = int(box[-4] * rate_y)
            if xmin < 0:
                xmin = 0
            ymin = int(box[-3] * rate_x)
            if ymin < 0:
                ymin = 0
            xmax = int(box[-2] * rate_y)
            if xmax < 0:
                xmax = 0
            ymax = int(box[-1] * rate_x)
            if ymax < 0:
                ymax = 0
            image = self.image[ymin:ymax,xmin:xmax,:]
            self.object_detected.append(box)
            cv2.imwrite('images/person'+ str(n)+ '.jpg',image)
            n+=1
    def set_image_by_filename(self, filename):
        image = cv2.imread(filename)
        self.image = image
    def clear(self):
        self.image = None
        self.object_detected = []

# if __name__ == "__main__":
#     person = Person()
#     person.set_image('images/sisterhood-concept-happy-children.jpg')
#     cv2.imshow('image',person.image)
#     cv2.waitKey()
#     person.predict()
#     for i in person.image_detected:
#         cv2.imshow('image',i)
#         cv2.waitKey()
#     pass