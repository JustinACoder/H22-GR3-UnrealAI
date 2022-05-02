#Converted to ue4 use from: https://www.tensorflow.org/get_started/mnist/beginners
#mnist_softmax.py: https://github.com/tensorflow/tensorflow/blob/r1.1/tensorflow/examples/tutorials/mnist/mnist_softmax.py

# Import data
import numpy as np
import tensorflow as tf
import unreal_engine as ue
from mlpluginapi import MLPluginAPI

import operator
import math


def auto_crop_image_nolabel(image):
    """
    This function remove crop the image in a way that (1) the image is square, (2) the
    image is centered and (3) the letter takes all the space.

    To do this, we crop each border until we hit the first non-zero pixel.
    We then extend the smallest side of the cropped image to the size of the biggest
    side to get a square image. Then we resize the image to make it 28 by 28.
    """
    # Tranform image to numpy array for easier manipulation
    # image =

    # set default values
    top_border = 0
    bottom_border = image.shape[0] - 1
    left_border = 0
    right_border = image.shape[1] - 1

    # Find the first non-zero pixel for top border
    for i in tf.range(image.shape[0]):
        if tf.reduce_sum(image[i, :, :]) > 0:
            top_border = i
            break
    ue.log('found the top border')

    # Find the first non-zero pixel for bottom border
    for i in tf.range(image.shape[0] - 1, -1, -1):
        if tf.reduce_sum(image[i, :, :]) > 0:
            bottom_border = i
            break
    ue.log('found the bottom border')

    # Find the first non-zero pixel for left border
    for i in tf.range(image.shape[1]):
        if tf.reduce_sum(image[:, i, :]) > 0:
            left_border = i
            break
    ue.log('found the left border')

    # Find the first non-zero pixel for right border
    for i in tf.range(image.shape[1] - 1, -1, -1):
        if tf.reduce_sum(image[:, i, :]) > 0:
            right_border = i
            break
    ue.log('found the right border')

    # find the middle of the cropped image
    middle_x = (left_border + right_border) // 2
    middle_y = (top_border + bottom_border) // 2

    # find the biggest side
    biggest_side = tf.math.maximum(right_border - left_border, bottom_border - top_border)

    # crop the image with the middle as (middle_x, middle_y)
    offset = 3  # additional column/row
    top_border = tf.math.maximum(tf.math.add((middle_y - biggest_side // 2), -offset), 0)
    bottom_border = tf.math.minimum(tf.math.add((middle_y + biggest_side // 2), offset), image.shape[0])
    left_border = tf.math.maximum(tf.math.add((middle_x - biggest_side // 2), -offset), 0)
    right_border = tf.math.minimum(tf.math.add((middle_x + biggest_side // 2), offset), image.shape[1])

    # crop the image
    image = image[top_border:bottom_border, left_border:right_border, :]

    # resize the image
    image = tf.image.resize(image, (28, 28), antialias=True)

    # return as tensorflow tensor
    return image


class EmnistLoad(MLPluginAPI):
	
	#expected api: storedModel and session, json inputs
	def on_json_input(self, json_data):
		#expect an image struct in json format
		ue.log('image len: ' + str(len(json_data)))

		np_pixels = np.array(json_data)
		img_size = int(math.sqrt(np_pixels.shape[0]))
		np_pixels = np_pixels.reshape((img_size, img_size, 1))
		np_pixels = auto_crop_image_nolabel(np_pixels)
		np_pixels = np_pixels.numpy().reshape((-1, 28, 28, 1))

		#embedd the input image pixels as 'x'
		output = self.model.predict(np_pixels)

		#set the prediction result in our json
		json_output = {}
		json_output['inputData'] = output.flatten().tolist()
		return json_output

	#expected api: no params forwarded for training? TBC
	def on_begin_training(self):
		
		model_path = 'emnist_model'
		self.model = tf.keras.models.load_model(model_path)
		ue.log("Loaded model from location " + model_path)


#required function to get our api
def get_api():
	#return CLASSNAME.get_instance()
	return EmnistLoad.get_instance()
