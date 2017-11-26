def SpriteSheet(path, frameWidth, frameHeight, frameSpeed, endFrame) {
 
  // code removed for brevity
 
  var currentFrame = 0;  // the current frame to draw
  var counter = 0;       // keep track of frame rate
 
  // Update the animation
  this.update = function() {
 
    // update to the next frame if it is time
    if (counter == (frameSpeed - 1))
      currentFrame = (currentFrame + 1) % endFrame;
 
    // update the counter
    counter = (counter + 1) % frameSpeed;
    }
  };
