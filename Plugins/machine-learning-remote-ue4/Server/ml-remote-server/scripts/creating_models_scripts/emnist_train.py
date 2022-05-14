import datetime
import random
import tensorflow_datasets as tfds  # pip install tensorflow-datasets
import numpy as np
from myFunctions import *

# comment out to use GPU
# os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
if tf.test.gpu_device_name():
    print('GPU found')
else:
    print("No GPU found")

(ds_train, ds_test), ds_info = tfds.load(
    'emnist/letters',
    split=["train", "test"],
    shuffle_files=True,
    as_supervised=True,
    with_info=True,
)

ds_train = prepareSet(ds_train, auto_crop=True)
ds_test = prepareSet(ds_test, auto_crop=True)

model = tf.keras.models.Sequential([
    # randomly rotate images
    tf.keras.layers.RandomRotation(0.075, fill_mode='constant'),

    # randomly contrast images
    tf.keras.layers.RandomContrast(0.2),

    # Used to make the important features more important
    tf.keras.layers.Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(28, 28, 1)),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),

    tf.keras.layers.Dropout(0.35),

    # flatten the image to a vector
    tf.keras.layers.Flatten(),

    # add a hidden layer
    tf.keras.layers.Dense(256, activation='relu'),

    # prevent overfitting (accuracy >> val_accuracy)
    tf.keras.layers.Dropout(0.5),

    # add hidden layer
    tf.keras.layers.Dense(128, activation='relu'),

    # prevent overfitting (accuracy >> val_accuracy)
    tf.keras.layers.Dropout(0.5),

    # output layer with 27 units (one for each letter + one for unknown)
    tf.keras.layers.Dense(27, activation='softmax')  # output layer
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(0.001),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# *** loggin with tensorboard *** #
rnd_id = random.randint(1, 100000)
log_dir = "logs/fit/" + str(rnd_id) + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
file_writer = tf.summary.create_file_writer(log_dir)
with file_writer.as_default():
    nbImagesToShow = 15
    images, labels = tuple(zip(*ds_train))
    images = np.reshape(images[0:nbImagesToShow], (-1, 28, 28, 1))
    tf.summary.image(str(nbImagesToShow) + " training data examples", images, max_outputs=nbImagesToShow, step=0)
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

model.fit(
    ds_train,
    epochs=50,
    validation_data=ds_test,
    callbacks=[tensorboard_callback]
)

# saving the model
if True:
    name = 'modelEmnist_' + str(rnd_id)
    path = 'saved_model/' + name
    model.save(path)
