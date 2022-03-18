/*
* In this file, we will use a pre-trained model to classify letters.
* The model is trained on the EMNIST dataset.
*
* PROBLEM AT THE MOMENT:
*   - The model has difficulty classifying the letters. Especially when the
*     letters are not taking up all the space.
*
* */
const pixelSize = 28;
const pixelRatio = canvas.width / pixelSize; // no need to get height, it's the same
const model = tf.loadLayersModel('./jsmodel/model.json');

/**
 * Show downsized canvas
 * */
function showDownsizedCanvas(arrayPixels) {
    const pixelRatioDownsized = downsizedcanvas.width / pixelSize;
    let imageData = downsizedctx.getImageData(0, 0, downsizedcanvas.width, downsizedcanvas.height);
    let dy, dx, index;

    // for each chunk of pixels
    for (let i = 0; i < pixelSize; i++) {
        for (let j = 0; j < pixelSize; j++) {
            let pixelChunkColor = (1 - arrayPixels[i][j]) * 255;

            // for each pixel in the chunk
            for (let i1 = 0; i1 < pixelRatioDownsized; i1++) {
                for (let j1 = 0; j1 < pixelRatioDownsized; j1++) {
                    //rgb (k=0 is red, k=1 is green, k=2 is blue)
                    for (let k = 0; k < 3; k++) {
                        dy = i * pixelRatioDownsized + i1;
                        dx = j * pixelRatioDownsized + j1;
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
function getAverageColor(j, i) {
    let imageData = ctx.getImageData(j, i, pixelRatio, pixelRatio);
    let data = imageData.data;
    let r = 0; // we just need red as we are using a black and white image (same rgb values)
    for (let k = 0; k < data.length; k += 4) {
        r += data[k];
    }

    let nbPixels = data.length / 4;
    return 1 - (r / (nbPixels * 255)); // 1- because we want black to be 1 and white to be 0
}


/**
 * Takes in a canvas, compress it to 28x28 pixels and retuns the array of pixel values between 0 and 1.
 * */
function getPixels() {
    // create array of pixels
    let newPixels2D = [];

    // loop through chunks of pixels
    for (let i = 0; i < canvas.height; i += pixelRatio) {
        let line = [];
        for (let j = 0; j < canvas.width; j += pixelRatio) {

            // get the average color of the chunk
            let averageColor = getAverageColor(j, i);

            // push the average color to the 2D array
            line.push(averageColor);
        }
        newPixels2D.push(line);
    }

    //show downsized canvas
    showDownsizedCanvas(newPixels2D);

    return [newPixels2D];
}

document.getElementById('predict').addEventListener('click', async () => {
    let pixels = getPixels();
    let tensor = tf.tensor3d(pixels, [1, pixelSize, pixelSize]);
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