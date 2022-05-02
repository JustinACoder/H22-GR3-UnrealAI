#Converted to ue4 use from: https://www.tensorflow.org/get_started/mnist/beginners
#mnist_softmax.py: https://github.com/tensorflow/tensorflow/blob/r1.1/tensorflow/examples/tutorials/mnist/mnist_softmax.py

# Import data
import numpy as np
import tensorflow as tf
import unreal_engine as ue
from mlpluginapi import MLPluginAPI

import operator


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
    image = tf.image.resize(image, (28, 28))

    # return as tensorflow tensor
    return image


class MnistSave(MLPluginAPI):
	
	#expected api: storedModel and session, json inputs
	def on_json_input(self, json_data):
		#expect an image struct in json format
		ue.log('image len: ' + str(len(json_data)))

		#prepare the image to be processed
		np_pixels = np.array(json_data)
		img_size = int(math.sqrt(np_pixels.shape[0]))
		np_pixels = np_pixels.reshape((img_size, img_size, 1))
		np_pixels = auto_crop_image_nolabel(np_pixels)
		np_pixels = np_pixels.numpy().reshape((-1, 28, 28, 1))

		#predict the class of the image
		output = self.model.predict(np_pixels)

		#return an output
		json_output = {}
		json_output['inputData'] = output.flatten().tolist()
		return json_output

	#expected api: no params forwarded for training? TBC
	def on_begin_training(self):

		ue.log("starting mnist keras training with save!")

		(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
		# Normalize images
		x_train = x_train.astype("float32") / 255
		x_test = x_test.astype("float32") / 255
		# Add extra dimension
		x_train = np.expand_dims(x_train, -1)
		x_test = np.expand_dims(x_test, -1)

		# ue.log(x_train.shape[0] + " train samples")
		# ue.log(x_test.shape[0] + " test samples")

		num_classes = 10
		input_shape = (28, 28, 1)
		y_train = tf.keras.utils.to_categorical(y_train, num_classes)
		y_test = tf.keras.utils.to_categorical(y_test, num_classes)

		# Create the model
		self.model = tf.keras.models.Sequential([
			tf.keras.layers.Input(shape=input_shape),
			tf.keras.layers.Conv2D(32, kernel_size=(3, 3), activation='relu'),
			tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
			tf.keras.layers.Conv2D(64, kernel_size=(3, 3), activation='relu'),
			tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
			tf.keras.layers.Flatten(),
			tf.keras.layers.Dropout(0.5),
			tf.keras.layers.Dense(num_classes, activation='softmax')
		])

		batch_size = 128
		epochs = 15

		self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

		self.model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_split=0.1)
		score = self.model.evaluate(x_test, y_test, verbose=0)
		ue.log("Final loss: " + str(score[0]))
		ue.log("Final accuracy: " + str(score[1]))
		
		model_path = 'mnist_model'
		tf.keras.models.save_model(self.model, model_path)
		ue.log("Model saved at location " + model_path)
		


#required function to get our api
def get_api():
	#return CLASSNAME.get_instance()
	return MnistSave.get_instance()
