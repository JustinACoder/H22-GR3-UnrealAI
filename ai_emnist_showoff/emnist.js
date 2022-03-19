/*
* In this file, we will use a pre-trained model to classify letters.
* The model is trained on the EMNIST dataset.
*
* PROBLEM AT THE MOMENT:
*   - The model has difficulty classifying the letters. Especially when the
*     letters are not taking up all the space. (Solved)
*   - For the moment, if we draw letters too small, the image will be
*     cropped and the stroke width would be abnormally large. To solve
*     this, we will have to save the exact path of the stroke and
*     manually change stroke width depending on the size of the letter.
*
* */
const pixelSize = 28;
const model = tf.loadLayersModel('./jsmodel/model.json');


if (canvas.width !== canvas.height) {
    alert('The canvas must be square.');
    throw new Error('The canvas must be square.');
}


/**
 * Show downsized canvas. The arrayPixels should already be a 2D reduced array.
 * */
function showDownsizedCanvas(arrayPixels) {
    const pixelRatioDownsized = downsizedcanvas.width / pixelSize;
    let imageData = downsizedctx.getImageData(0, 0, downsizedcanvas.width, downsizedcanvas.height);
    let dy, dx, index;

    // for each chunk of pixels
    for (let i = 0; i < arrayPixels.length; i++) {
        for (let j = 0; j < arrayPixels[i].length; j++) {
            let pixelChunkColor = (1 - arrayPixels[i][j]??0) * 255;

            // for each pixel in the chunk
            for (let i1 = 0; i1 < pixelRatioDownsized; i1++) {
                for (let j1 = 0; j1 < pixelRatioDownsized; j1++) {
                    dy = i * pixelRatioDownsized + i1;
                    dx = j * pixelRatioDownsized + j1;

                    //rgb (k=0 is red, k=1 is green, k=2 is blue)
                    for (let k = 0; k < 3; k++) {
                        index = (dy * downsizedcanvas.width + dx) * 4 + k;

                        imageData.data[index] = pixelChunkColor;
                    }

                    //transparency (k=3 is alpha)
                    imageData.data[(dy * downsizedcanvas.width + dx) * 4 + 3] = 255;

                    //Note: *4 is because each pixel is represented by 4 values (r,g,b,a)
                }
            }
        }
    }
    downsizedctx.putImageData(imageData, 0, 0);
}


/**
 * Get the average pixel value in a chunk of pixels.
 * */
function getAverageColor(listPixels, x, y, pixelRatio) {
    let sum = 0;
    let count = 0;
    for (let i1 = y; i1 < y + pixelRatio && Math.round(i1) < listPixels.length; i1++) {
        for (let j1 = x; j1 < x + pixelRatio && Math.round(j1) < listPixels.length; j1++) { // valid length bc its a square
            sum += listPixels[Math.round(i1)][Math.round(j1)];
            count++;
        }
    }
    return sum / count;
}


/**
 * Takes in a 2D list of pixels, compress it to 28x28 pixels and returns the array of pixel values between 0 and 1.
 * */
function getPixels(listPixels) {
    // create array of pixels
    let newPixels2D = [];

    let pixelRatio = listPixels.length / pixelSize;

    // loop through chunks of pixels
    for (let i = 0; Math.round(i) < listPixels.length; i += pixelRatio) {
        let line = [];
        for (let j = 0; Math.round(j) < listPixels.length; j += pixelRatio) { // valid length because its a square
            // get the average color of the chunk
            let averageColor = getAverageColor(listPixels, j, i, pixelRatio);

            // push the average color to the 2D array
            line.push(averageColor);
        }
        newPixels2D.push(line);
    }

    //show downsized canvas
    showDownsizedCanvas(newPixels2D);

    return newPixels2D;
}

document.getElementById('predict').addEventListener('click', async () => {
    let croppedImage = autoCropImage();
    let pixels = getPixels(croppedImage);
    let tensor = tf.tensor3d([pixels], [1, pixelSize, pixelSize]);
    tensor = tf.expandDims(tensor, -1);
    let predictionResult = (await model).predict(tensor);
    let prediction_array = predictionResult.dataSync();
    let max = 0;
    let max_index = 0;
    for (let i = 0; i < prediction_array.length; i++) {
        if (prediction_array[i] > max) {
            max = prediction_array[i];
            max_index = i;
        }
    }

    if(max_index === 0){
        prediction.innerHTML = '<span style="color: red; font-size: xxx-large">' + '?' + '</span>';
    }else{
        prediction.innerHTML = '<span style="color: #1c9f00; font-size: xxx-large">' + String.fromCharCode(max_index + 64) + '</span>';
    }
});


/**
 This function remove crop the image in a way that (1) the image is square, (2) the
 image is centered and (3) the letter takes all the space.

 To do this, we crop each border until we hit the first non-zero pixel.
 We then extend the smallest side of the cropped image to the size of the biggest
 side to get a square image. Then we return the image in black and white.
 */
function autoCropImage(){
    const OFFSET_BORDER = 2; // space added to the border of the image (0 means no space) (dont put too much space)

    // set default values
    let top_border = 0
    let bottom_border = canvas.height - 1
    let left_border = 0
    let right_border = canvas.width - 1


    function is_border_empty(line){
        let data = line.data;
        for (let i = 0; i < data.length; i += 4) {
            if (data[i] === 0) { // 1 (white) means empty. (not 0 means not empty)
                return false;
            }
        }
        return true;
    }


    // Find the first non-zero pixel for top border
    for(let i=0;i<canvas.height;i++){
        // if every pixel is not black, we haven't reached the top border
        // get all the pixels in the line
        let line = ctx.getImageData(0, i, canvas.width, 1);
        if(!is_border_empty(line)){
            top_border = i;
            break;
        }
    }

    // Find the first non-zero pixel for bottom border
    for(let i=canvas.height-1;i>=0;i--){
        // if every pixel is not black, we haven't reached the bottom border
        // get all the pixels in the line
        let line = ctx.getImageData(0, i, canvas.width, 1);
        if(!is_border_empty(line)){
            bottom_border = i;
            break;
        }
    }

    // Find the first non-zero pixel for left border
    for(let i=0;i<canvas.width;i++){
        // if every pixel is not black, we haven't reached the left border
        // get all the pixels in the line
        let line = ctx.getImageData(i, 0, 1, canvas.height);
        if(!is_border_empty(line)){
            left_border = i;
            break;
        }
    }

    // Find the first non-zero pixel for right border
    for(let i=canvas.width-1;i>=0;i--){
        // if every pixel is not black, we haven't reached the right border
        // get all the pixels in the line
        let line = ctx.getImageData(i, 0, 1, canvas.height);
        if(!is_border_empty(line)){
            right_border = i;
            break;
        }
    }

    // find the middle of the cropped image
    let middle_x = (left_border + right_border) / 2
    let middle_y = (top_border + bottom_border) / 2

    // find the biggest side
    let biggest_side = Math.max(right_border - left_border, bottom_border - top_border)

    // ratio
    let pixelRatio = biggest_side / pixelSize;

    // crop the image with the middle as (middle_x, middle_y)
    const offset = OFFSET_BORDER * pixelRatio // additional column/row
    top_border = Math.floor((middle_y - biggest_side / 2) - offset)
    bottom_border = Math.floor((middle_y + biggest_side / 2) + offset)
    left_border = Math.floor((middle_x - biggest_side / 2) - offset)
    right_border = Math.floor((middle_x + biggest_side / 2) + offset)

    // size of the cropped image
    let size = Math.max(right_border - left_border, bottom_border - top_border)

    // crop the image
    let croppedImage = ctx.getImageData(left_border, top_border, size, size);

    /*
    * Note :
    * When we crop the image, if we try to get pixels outside the image, we get
    * a transparent black pixel. However, black means something is written.
    * Therefore, we will have to change pixel to white if their alpha is 0.
    * This way, we can make the difference between the black stroke and the
    * black pixels outside the image.
    * */

    // transforms to a 2d array
    let croppedImageData = croppedImage.data;
    let croppedImageData2D = [];
    for (let i = 0; i < size; i++) {
        croppedImageData2D[i] = [];
        for (let j = 0; j < size; j++) {
            if (croppedImageData[(i * size + j) * 4 + 3] === 0) {
                // if alpha is 0, it means the pixel is empty
                croppedImageData2D[i][j] = 0;
            } else {
                croppedImageData2D[i][j] = 1-croppedImageData[(i * size + j) * 4]/255; // only the red channel as R=G=B;
            }
        }
    }
    return croppedImageData2D;
}