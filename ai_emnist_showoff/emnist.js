const model = tf.loadLayersModel('./jsmodel/model.json');

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