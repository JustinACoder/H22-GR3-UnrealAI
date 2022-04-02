import tensorflow as tf


def auto_crop_image(image, label):
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

    # Find the first non-zero pixel for bottom border
    for i in tf.range(image.shape[0] - 1, -1, -1):
        if tf.reduce_sum(image[i, :, :]) > 0:
            bottom_border = i
            break

    # Find the first non-zero pixel for left border
    for i in tf.range(image.shape[1]):
        if tf.reduce_sum(image[:, i, :]) > 0:
            left_border = i
            break

    # Find the first non-zero pixel for right border
    for i in tf.range(image.shape[1] - 1, -1, -1):
        if tf.reduce_sum(image[:, i, :]) > 0:
            right_border = i
            break

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
    return image, label


def normalize_img(image, label):
    """Normalizes images: `uint8` -> `float32`."""
    return tf.cast(image, tf.float32) / 255., label


def prepareSet(ds: tf.data.Dataset, auto_crop=False):
    ds = ds.map(normalize_img, num_parallel_calls=tf.data.AUTOTUNE)
    if auto_crop:
        ds = ds.map(auto_crop_image, num_parallel_calls=tf.data.AUTOTUNE)
    ds = ds.cache()
    count = ds.reduce(0, lambda x, _: x + 1).numpy()
    ds = ds.shuffle(count)
    ds = ds.batch(128)
    ds = ds.prefetch(tf.data.AUTOTUNE)
    ds = ds.map(lambda image, label: (tf.image.rot90(image, k=-1), label))  # rotate 90 degrees
    ds = ds.map(lambda image, label: (tf.image.flip_left_right(image), label))  # flip left-right
    return ds


def removeClasses(ds: tf.data.Dataset, classes):
    """
    This function removes all specified classes from the dataset.
    """
    def filter_fn(image, label):
        return tf.math.reduce_all(tf.math.not_equal(label, classes))

    ds = ds.filter(filter_fn)
    return ds
