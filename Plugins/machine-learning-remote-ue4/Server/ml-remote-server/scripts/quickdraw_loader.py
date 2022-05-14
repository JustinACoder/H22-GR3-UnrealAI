# Loader of the quickdraw ai

# Import data
from . import myFunctions as mf
import numpy as np
import tensorflow as tf
import unreal_engine as ue
from mlpluginapi import MLPluginAPI
import math
import pathlib


class QuickdrawLoad(MLPluginAPI):

    # expected api: storedModel and session, json inputs
    def on_json_input(self, json_data):
        
        # prepare the image for the ai
        np_pixels = np.array(json_data)
        img_size = int(math.sqrt(np_pixels.shape[0]))
        np_pixels = np_pixels.reshape((img_size, img_size, 1))
        np_pixels = mf.auto_crop_image_nolabel(np_pixels, offsetpercent=0.1, resizemethod='area')
        np_pixels = np_pixels.numpy().reshape((-1, 28, 28, 1))

        # np_pixels = tf.clip_by_value(np_pixels, clip_value_min=0, clip_value_max=1).numpy()

        # make a prediction
        output = self.model(np_pixels, training=False).numpy()

        # mf.showImage(np_pixels)

        # set the prediction result in our json
        return {'inputData':output.flatten().tolist()}

    # Load the model
    def on_begin_training(self):
        model_path = str(pathlib.Path(__file__).parent.resolve()) + '\..\quickdraw_model'
        self.model = tf.keras.models.load_model(model_path)
        ue.log("Loaded model from location " + model_path)


# required function to get our api
def get_api():
    # return CLASSNAME.get_instance()
    return QuickdrawLoad.get_instance()
