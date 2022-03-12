/*
* In this file, we are going to draw the canvas.
* If the user presses the mouse, we are going to draw a point at the mouse position of radius 5.
* */

let isDrawing = false;
let prevX = null;
let prevY = null;


canvas = document.getElementById('canvas');
ctx = canvas.getContext('2d');

window.addEventListener('mousedown', function (e) {
    isDrawing = true;
    prevX = e.clientX - canvas.offsetLeft;
    prevY = e.clientY - canvas.offsetTop;
    draw(e.clientX, e.clientY);
});

canvas.addEventListener('mousemove', function (e) {
    if (isDrawing) {
        draw(e.clientX, e.clientY);
    }
});

window.addEventListener('mouseup', function () {
    isDrawing = false;
});

function draw(x,y) {
    const radius = 20;

    //calculate position of the mouse relative to the canvas
    let mouseX = x - canvas.offsetLeft;
    let mouseY = y - canvas.offsetTop;

    ctx.beginPath();
    ctx.moveTo(prevX, prevY);
    ctx.lineTo(mouseX, mouseY);
    ctx.lineWidth = radius * 2;
    ctx.lineCap = 'round';
    ctx.stroke();
    ctx.closePath();

    prevX = mouseX;
    prevY = mouseY;
}

