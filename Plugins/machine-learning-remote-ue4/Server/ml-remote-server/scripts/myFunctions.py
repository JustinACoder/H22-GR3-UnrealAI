import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import unreal_engine as ue


def auto_crop_image_nolabel(image, offsetpercent=0.065, resizemethod='bilinear'):
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
    offset_percent = offsetpercent  # additional percentage of the biggest side
    offset = int(tf.math.round(float(biggest_side) * offset_percent))
    top_border = tf.math.maximum(tf.math.add((middle_y - biggest_side // 2), -offset), 0)
    bottom_border = tf.math.minimum(tf.math.add((middle_y + biggest_side // 2), offset), image.shape[0])
    left_border = tf.math.maximum(tf.math.add((middle_x - biggest_side // 2), -offset), 0)
    right_border = tf.math.minimum(tf.math.add((middle_x + biggest_side // 2), offset), image.shape[1])

    # crop the image
    image = image[top_border:bottom_border, left_border:right_border, :]

    # resize the image
    image = tf.image.resize(image, (28, 28), method=resizemethod, antialias=True)

    # return as tensorflow tensor
    return image


def showImage(np_pixels: np.ndarray):
    # show the image
    plt.imshow(np_pixels[0, :, :, 0], cmap='gray')
    plt.show()
