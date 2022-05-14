# Loader of the emnist ai

# Import data
from . import myFunctions as mf
import numpy as np
import tensorflow as tf
import unreal_engine as ue
from mlpluginapi import MLPluginAPI
import math
import pathlib


class EmnistLoad(MLPluginAPI):

    # input event
    def on_json_input(self, json_data):

        # prepare the image for the ai
        np_pixels = np.array(json_data)
        img_size = int(math.sqrt(np_pixels.shape[0]))
        np_pixels = np_pixels.reshape((img_size, img_size, 1))
        np_pixels = mf.auto_crop_image_nolabel(np_pixels)
        np_pixels = np_pixels.numpy().reshape((-1, 28, 28, 1))

        # make a prediction
        output = self.model(np_pixels, training=False).numpy()

        # set the prediction result in our json
        return {'inputData': output.flatten().tolist()}

    # this is gonna get called when the client connects (the game starts) and load the model
    def on_begin_training(self):
        model_path = str(pathlib.Path(__file__).parent.resolve()) + '\..\emnist_model'
        self.model = tf.keras.models.load_model(model_path)
        ue.log("Loaded model from location " + model_path)


# required function to get our api
def get_api():
    # return CLASSNAME.get_instance()
    return EmnistLoad.get_instance()
