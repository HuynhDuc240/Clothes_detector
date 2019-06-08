
import PyQt5
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau, TerminateOnNaN, CSVLogger
from keras import backend as K
from keras.models import load_model
from math import ceil
import numpy as np
from matplotlib import pyplot as plt

from models.keras_ssd7 import build_model
from keras_loss_function.keras_ssd_loss import SSDLoss
from keras_layers.keras_layer_AnchorBoxes import AnchorBoxes
from keras_layers.keras_layer_DecodeDetections import DecodeDetections
from keras_layers.keras_layer_DecodeDetectionsFast import DecodeDetectionsFast

from ssd_encoder_decoder.ssd_input_encoder import SSDInputEncoder
from ssd_encoder_decoder.ssd_output_decoder import decode_detections, decode_detections_fast

import cv2

model_path = 'models_trained/ssd7_epoch-100_loss-1.9248_val_loss-1.9250.h5'
normalize_coords = True
img_height = 300
img_width = 300
n_classes = 3
# We need to create an SSDLoss object in order to pass that to the model loader.
ssd_loss = SSDLoss(neg_pos_ratio=3, alpha=1.0)
model = load_model(model_path, custom_objects={'AnchorBoxes': AnchorBoxes,
                                               'compute_loss': ssd_loss.compute_loss})
image = cv2.imread('person.png')
rate_x = image.shape[1]/img_width
rate_y = image.shape[0]/img_height
print(rate_x,rate_y)
img = np.array(image)
# img = cv2.resize(img, (480,300))
# img = img.reshape(1,300,480,3)
img = cv2.resize(img, (300,300))
img = img.reshape(1,300,300,3)
y_pred = model.predict(img)
# cv2.imshow('image',image)
# cv2.waitKey()
y_pred_decoded = decode_detections(y_pred,
                                   confidence_thresh=0.5,
                                   iou_threshold=0.45,
                                   top_k=200,
                                   normalize_coords=normalize_coords,
                                   img_height=img_height,
                                   img_width=img_width)
current_axis = plt.gca()

colors = plt.cm.hsv(np.linspace(0, 1, n_classes+1)).tolist() # Set the colors for the bounding boxes
classes = ['background', 'Shirt', 'T_Shirt', 'Coat']

i=0
for box in y_pred_decoded[i]:
    print(box)
    xmin = int(box[-4] * rate_y)
    ymin = int(box[-3] * rate_x)
    xmax = int(box[-2] * rate_y)
    ymax = int(box[-1] * rate_x)
    cv2.rectangle(image, (xmin,ymin),(xmax,ymax),(0,255,0),3)
    # color = colors[int(box[0])]
    # label = '{}: {:.2f}'.format(classes[int(box[0])], box[1])
    # current_axis.add_patch(plt.Rectangle((xmin, ymin), xmax-xmin, ymax-ymin, color=color, fill=False, linewidth=2))  
    # current_axis.text(xmin, ymin, label, size='x-large', color='white', bbox={'facecolor':color, 'alpha':1.0})

cv2.imshow("image",image)
cv2.waitKey()
