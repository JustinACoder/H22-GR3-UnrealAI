# Converted to ue4 use from: https://www.tensorflow.org/get_started/mnist/beginners
# mnist_softmax.py: https://github.com/tensorflow/tensorflow/blob/r1.1/tensorflow/examples/tutorials/mnist/mnist_softmax.py

# Import data
from . import myFunctions as mf
import numpy as np
import tensorflow as tf
import unreal_engine as ue
from mlpluginapi import MLPluginAPI
import math


class EmnistLoad(MLPluginAPI):

    # expected api: storedModel and session, json inputs
    def on_json_input(self, json_data):
        # expect an image struct in json format
        ue.log('image len: ' + str(len(json_data)))

        np_pixels = np.array(json_data)
        img_size = int(math.sqrt(np_pixels.shape[0]))
        np_pixels = np_pixels.reshape((img_size, img_size, 1))
        np_pixels = mf.auto_crop_image_nolabel(np_pixels)
        np_pixels = np_pixels.numpy().reshape((-1, 28, 28, 1))

        # embedd the input image pixels as 'x'
        output = self.model.predict(np_pixels)

        # set the prediction result in our json
        letter_prediction = chr(np.argmax(output) + 64)
        ue.log('Letter prediction: ' + letter_prediction)
        json_output = {'inputData': output.flatten().tolist()}
        return json_output

    # expected api: no params forwarded for training? TBC
    def on_begin_training(self):
        model_path = 'emnist_model'
        self.model = tf.keras.models.load_model(model_path)
        ue.log("Loaded model from location " + model_path)


# required function to get our api
def get_api():
    # return CLASSNAME.get_instance()
    return EmnistLoad.get_instance()
