import keras
from numpy import loadtxt
from keras.models import load_model
import tensorflow as tf
import cv2
import matplotlib.pyplot as plt
import numpy as np
import time

model = tf.keras.models.load_model('model.h5')

gtLabels = ["airplane", "automobile", "bird", "cat", "deer", "dog", "frog", "horse",
			"ship", "truck"]

model.summary()

def prediction(image):
		image = cv2.imread(image)
		Xn = cv2.resize(image, (32, 32))
		Xn = cv2.cvtColor(Xn , cv2.COLOR_BGR2RGB)
		cv2.imshow("window", Xn)
		Xnew = Xn[np.newaxis, ...]
		ynew = model.predict_classes(Xnew)
		print('uncertain',ynew[0])
		prediction = ynew.argmax()
		print(gtLabels[ynew[0]])
		time.sleep(0.4)
		# cv2.destroyAllWindows()


