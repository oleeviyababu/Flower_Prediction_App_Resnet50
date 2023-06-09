from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import tensorflow as tf
import numpy as np

# Keras
from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
#from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()
#MODEL_PATH =r'C:\Users\oleev\Desktop\PORTFOLIO\f1\model_resnet50.h5'

# Load your trained model
#model = load_model(MODEL_PATH)

model=tf.keras.models.load_model('model_resnet50.h5')
tf.saved_model.save(model, 'saved_model')

#model_path = os.path.join(os.getcwd(), 'model_resnet50.h5')
#model = tf.keras.models.load_model(model_path)






def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))

    # Preprocessing the image
    x = image.img_to_array(img)
    # x = np.true_divide(x, 255)
    ## Scaling
    x=x/255
    x = np.expand_dims(x, axis=0)
   

   

    preds = model.predict(x)
    preds=np.argmax(preds, axis=1)
    if preds==0:
        preds="The flower is daisy"
    elif preds==1:
        preds="The flower is dandelion"
    elif preds==2:
        preds="The flower is rose"
    elif preds==3:
        preds="The flower is sunflower"
    else:
        preds="The flower Is tulip"
    
    
    return preds


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        
        print("Filename:", f.filename)
        print("File path:", file_path)

        # Make prediction
        preds = model_predict(file_path, model)
        result=preds
        return result
    return None


if __name__ == '__main__':
    app.run(debug=True)# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

