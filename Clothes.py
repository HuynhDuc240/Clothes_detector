from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import pickle
import cv2
mlb = pickle.loads(open("models_trained/labelbin.pickle", "rb").read())
class Clothes():
    def __init__(self):
        self.model = load_model("models_trained/clothes.h5")
        self.color = ""
        self.type = ""
    def predict(self):
        self.color = ""
        self.type = ""
        colors = ['red','black','yellow','white','gray','blue','green']
        types = ['Tshirt','shirt','coat']
        image = cv2.resize(self.image, (96, 96))
        image = image.astype("float") / 255.0
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        proba = self.model.predict(image)[0]
        # print(proba)
        idxs = np.argsort(proba)[::-1][:2]
        # for i in range(len(idxs)):
        #     print(mlb.classes_[idxs[i]])
        if mlb.classes_[idxs[1]] in types:
            color = [mlb.classes_[idxs[0]],round(proba[idxs[0]] * 100,2)]
            type_ = [mlb.classes_[idxs[1]],round(proba[idxs[1]] * 100,2)]
        else:
            color = [mlb.classes_[idxs[1]],round(proba[idxs[1]] * 100,2)]
            type_ = [mlb.classes_[idxs[0]],round(proba[idxs[0]] * 100,2)]
        if color[0] in colors and type_[0] in types:
            if color == 'red':
                color == 'blue'
            elif color == 'blue':
                color == 'yellow'
            elif color == 'yellow':
                color == 'blue'
            self.color = color
            self.type = type_


    def set_image_by_filename(self, fileName):
        image = cv2.imread(fileName)
        self.image = image
    def set_image(self, image):
        self.image = image
# if __name__ == "__main__":
#     clothes = Clothes()
#     clothes.set_image_by_filename('Shirt_black_16.jpg')
#     clothes.predict()
#     print(clothes.color,clothes.type)
#     pass




