var img;
var canvas, ctx;
var startX, startY, endX, endY;
var isDrawing = false;

// Function to handle user mouse down event
function handleMouseDown(event) {
  // only start drawing once user has uploaded an image
  if (img) { 
      startX = event.offsetX;
      startY = event.offsetY;
      isDrawing = true;
  }
}

// Function to handle user mouse move event
function handleMouseMove(event) {
  if (!isDrawing) return;
  endX = event.offsetX;
  endY = event.offsetY;
  drawRectangle();
}

// Function to handle user mouse up event
function handleMouseUp(event) {
  if (!isDrawing) return;
  endX = event.offsetX;
  endY = event.offsetY;
  isDrawing = false;
  drawRectangle();
}

// Function to draw a rectangle on the image canvas
function drawRectangle() {
  // Clear the canvas to remove any previous rectangle drawings
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  // Draw the image that the user uploaded onto the canvas
  ctx.drawImage(img, 0, 0);
  // Draw the rectangle based on user's mouse movement
  ctx.beginPath();
  ctx.rect(startX, startY, endX - startX, endY - startY);
  ctx.lineWidth = 2;
  ctx.strokeStyle = 'red';
  ctx.stroke();
}

function handleImageUpload(event) {
    // Create a new instance of FileReader
    var reader = new FileReader();
  
    // Define an event handler for when the FileReader has loaded the file
    reader.onload = function(event) {
      // Create image element
      img = new Image();
  
      // Define an event handler for when the Image has finished loading
      img.onload = function() {
        // Set the canvas dimensions to match the loaded image
        canvas.width = img.width;
        canvas.height = img.height;
        // Draw the image on the canvas at position (0, 0)
        ctx.drawImage(img, 0, 0);
      };
  
      // Set the source of the Image element to the loaded file data
      img.src = event.target.result;
    };
  
    // Check if a file was selected
    if (event.target.files && event.target.files[0]) {
      // Read the selected file as a Data URL
      reader.readAsDataURL(event.target.files[0]);
    }
  }
  
// function that adds event listeners to the canvas element - gets called when body in index.html is loaded
function init() {
    // Create a 2d context object on the canvas
    canvas = document.getElementById('canvas');
    ctx = canvas.getContext('2d');
    // Add event listeners for mouse on canvas
    canvas.addEventListener('mousedown', handleMouseDown);
    canvas.addEventListener('mousemove', handleMouseMove);
    canvas.addEventListener('mouseup', handleMouseUp);
    // Add event listener for image upload
    document.getElementById('image_upload').addEventListener('change', handleImageUpload);
}
