import cv2
from mtcnn import MTCNN
import numpy as np
def preprocess_image(frame):
    """
    Preprocess an image frame to detect and extract a normalized face.
    
    Args:
    frame (numpy.ndarray): The image frame as captured from the camera.
    
    Returns:
    numpy.ndarray or None: The preprocessed face image or None if no face is detected.
    """
    
    # Convert image to RGB (as OpenCV captures in BGR)
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Detect faces in the image using MTCNN
    detector = MTCNN()
    results = detector.detect_faces(image)
    if results:
        # Extract the bounding box from the first detected face
        x1, y1, width, height = results[0]['box']
        x2, y2 = x1 + width, y1 + height
        
        # Extract and crop the face from the frame
        face = image[y1:y2, x1:x2]
        
        # Resize face to expected size (e.g., 160x160 pixels)
        face = cv2.resize(face, (160, 160))
        
        # Normalize pixel values to the range 0-1
        face = face.astype(np.uint8)
        
        return face
    else:
        return None
