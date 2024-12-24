# -*- coding: utf-8 -*-
"""Untitled32.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1nEqBiiQUBIKdb_JaF-fVBoum3g61gxkV

PYTHON CODE TO RECOGNIZE IMAGE OF GRAPH AND FIND EQUATION
"""

from IPython.display import display, Javascript
from google.colab.output import eval_js
from base64 import b64decode

def take_photo(filename='photo.jpg', quality=0.8):
  js = Javascript('''
    async function takePhoto(quality) {
      const div = document.createElement('div');
      const capture = document.createElement('button');
      capture.textContent = 'Capture';
      div.appendChild(capture);

      const video = document.createElement('video');
      video.style.display = 'block';
      const stream = await navigator.mediaDevices.getUserMedia({video: true});

      document.body.appendChild(div);
      div.appendChild(video);
      video.srcObject = stream;
      await video.play();

      // Resize the output to fit the video element.
      google.colab.output.setIframeHeight(document.documentElement.scrollHeight, true);

      // Wait for Capture to be clicked.
      await new Promise((resolve) => capture.onclick = resolve);

      const canvas = document.createElement('canvas');
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      canvas.getContext('2d').drawImage(video, 0, 0);
      stream.getVideoTracks()[0].stop();
      div.remove();
      return canvas.toDataURL('image/jpeg', quality);
    }
    ''')
  display(js)
  data = eval_js('takePhoto({})'.format(quality))
  binary = b64decode(data.split(',')[1])
  with open(filename, 'wb') as f:
    f.write(binary)
  return filename

from IPython.display import Image
try:
  filename = take_photo()
  print('Saved to {}'.format(filename))

  # Show the image which was just taken.
  display(Image(filename))
except Exception as err:
  # Errors will be thrown if the user does not have a webcam or if they do not
  # grant the page permission to access it.
  print(str(err))
  import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Function to capture an image from the camera
def capture_image():
    cap = cv2.VideoCapture(0)  # Use the default camera (0)
    if not cap.isOpened():
        print("Error: Camera not found.")
        return None

    print("Press 's' to capture the image.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        # Display the camera feed
        cv2.imshow("Camera Feed", frame)

        # Capture the image when the user presses 's'
        if cv2.waitKey(1) & 0xFF == ord('s'):
            captured_image = frame
            cv2.imwrite("captured_graph.png", captured_image)
            print("Image captured and saved as 'captured_graph.png'")
            break

    cap.release()
    cv2.destroyAllWindows()
    return captured_image

# Function to preprocess the image (extracts the graph data points)
def preprocess_image(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply a binary threshold to the image
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    # Find contours to detect the graph line
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Get the largest contour, assuming it's the graph line
    contour = max(contours, key=cv2.contourArea)

    # Approximate the contour to reduce the number of points
    epsilon = 0.02 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)

    # Extract x and y coordinates from the contour points
    points = approx[:, 0, :]
    x_points = points[:, 0]
    y_points = points[:, 1]

    return x_points, y_points

# Example function to fit data (e.g., quadratic or linear)
def fit_curve(x, y):
    # Example: fit a quadratic curve to the data
    def model(x, a, b, c):
        return a * x**2 + b * x + c

    # Fit the model to the data
    popt, _ = curve_fit(model, x, y)
    a, b, c = popt

    # Return the fitted equation
    return f"y = {a:.2f}x² + {b:.2f}x + {c:.2f}"

# Main function to execute the process
def main():
    # Step 1: Capture the image
    image = capture_image()
    if image is None:
        return

    # Step 2: Preprocess the image and extract data points
    x_points, y_points = preprocess_image(image)

    # Step 3: Fit a curve to the data points
    equation = fit_curve(x_points, y_points)
    print(f"Predicted Equation: {equation}")

    # Step 4: Plot the original graph and the fitted curve
    plt.scatter(x_points, y_points, color='blue', label='Extracted Points')
    plt.plot(x_points, np.polyval(np.polyfit(x_points, y_points, 2), x_points), color='red', label='Fitted Curve')
    plt.legend()
    plt.title("Graph and Fitted Curve")
    plt.show()

if __name__ == "__main__":
    main()