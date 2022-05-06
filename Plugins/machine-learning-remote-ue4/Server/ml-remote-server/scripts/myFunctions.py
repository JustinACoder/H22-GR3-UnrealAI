import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import unreal_engine as ue
import scipy.ndimage as ndimage


def auto_crop_image_nolabel(image, offsetpercent=0.065, resizemethod='bilinear', size=28):
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
    image = tf.image.resize(image, (size, size), method=resizemethod, antialias=True)

    # return as tensorflow tensor
    return image


def get_line(start, end):
    """Bresenham's Line Algorithm
    Produces a list of tuples from start and end
    >>> points1 = get_line((0, 0), (3, 4))
    >>> points2 = get_line((3, 4), (0, 0))
    >>> assert(set(points1) == set(points2))
    >>> print points1
    [(0, 0), (1, 1), (1, 2), (2, 3), (3, 4)]
    >>> print points2
    [(3, 4), (2, 3), (1, 2), (1, 1), (0, 0)]
    """
    # Setup initial conditions
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1

    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)

    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True

    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1

    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1

    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx

    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    return points


def createImageFromInput(json_data, stroke_width=2, additional_sides=1):
    data = np.array(json_data)
    ue.log('data shape: ' + str(data.shape))
    vectors_originals = np.zeros((data.shape[0] // 2, 2))
    for i, coord in enumerate(data):
        vectors_originals[i // 2, i % 2] = coord

    # coordinates are in the form of (x, y) from top left corner to bottom right corner.
    # Values are in the range of 0 to 1.

    # find the coordinates in a 256x256 image (that will be resized later to 28x28)
    vectors_resized = np.zeros((vectors_originals.shape[0], 2), dtype=np.int32)
    for i, vector in enumerate(vectors_originals):
        vectors_resized[i, 0] = int(vector[0] * 256)
        vectors_resized[i, 1] = int(vector[1] * 256)

    # create the image using Bresenham's line algorithm
    image = np.zeros((256, 256, 1))
    for i in range(vectors_resized.shape[0] - 1):
        points = get_line((vectors_resized[i, 0], vectors_resized[i, 1]),
                          (vectors_resized[i + 1, 0], vectors_resized[i + 1, 1]))
        for point in points:
            image[point[1], point[0], 0] = 1

    image = auto_crop_image_nolabel(image, size=28-2*additional_sides)

    # adjust pixel values
    max_value = np.max(image)
    multiplicator = 1/max_value
    image = image * multiplicator

    # use dilation to add stroke width
    image = ndimage.binary_dilation(image, iterations=stroke_width).astype(float)

    # add additional sides (add additional_sides * to the sides of the image)
    image = np.pad(image, ((additional_sides, additional_sides), (additional_sides, additional_sides), (0, 0)),
                     'constant', constant_values=0)


    showImage(image)

    # return as tensorflow tensor
    return image


def showImage(np_pixels: np.ndarray):
    # show the image
    try:
        plt.imshow(np_pixels[0, :, :, 0], cmap='gray')
    except:
        plt.imshow(np_pixels[:, :, 0], cmap='gray')
    plt.show()
