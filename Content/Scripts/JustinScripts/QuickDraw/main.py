import datetime
import tensorflow_datasets as tfds
from myFunctions import *

# comment out to use GPU
# os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
if tf.test.gpu_device_name():
    print('GPU found')
else:
    print("No GPU found")

print("Loading data...")

# WARNING: this is a very large dataset (37Gb), it will be downloaded when you run the script #
(ds_train, ds_test), ds_info = tfds.load(
    'quickdraw_bitmap',
    split=["train[:90%]", "train[90%:]"],
    shuffle_files=True,
    as_supervised=True,
    with_info=True,
    data_dir='G:/tensorflow_datasets/'
)

print("Preprocessing data...")

ds_train = prepareSetQuickDraw(ds_train)
ds_test = prepareSetQuickDraw(ds_test)

print("Done!")

model = tf.keras.models.Sequential([
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
    tf.keras.layers.Dropout(0.35),

    # add hidden layer
    tf.keras.layers.Dense(256, activation='relu'),

    # prevent overfitting (accuracy >> val_accuracy)
    tf.keras.layers.Dropout(0.35),

    # output layer with 27 units (one for each letter + one for unknown)
    tf.keras.layers.Dense(345, activation='softmax')  # output layer
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(0.001),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# *** logging with tensorboard *** #
date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_dir = "logs/fit/" + date
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

print("Starting training...")

model.fit(
    ds_train,
    epochs=50,
    validation_data=ds_test,
    callbacks=[tensorboard_callback]
)

# saving the model
if False:
    print("Saving model...")
    name = 'modelEmnist_' + str(date)
    path = 'saved_model/' + name
    model.save(path)
    #os.system('tensorflowjs_converter --input_format=keras ' + path + ' saved_model/tfjs/' + name)
