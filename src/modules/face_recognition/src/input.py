import cv2
import time
from .exceptions import CameraError, CaptureError

def capture_1_photo_timeout_5():
    """ Capture 1 photo after a 5-second timeout. """
    try:
        cap = open_camera()
        time.sleep(5)
        photos = capture_photos(cap, 1, 0)
        cap.release()
        return photos[0] if photos else None
    except CameraError:
        return None
    except CaptureError:
        return None

def capture_3_photo_timeout_5():
    """ Capture 3 photos, 1 second apart, after a 5-second timeout. """
    try:
        cap = open_camera()
        time.sleep(5)
        photos = capture_photos(cap, 3, 1)
        cap.release()
        return photos
    except CameraError:
        return []
    except CaptureError:
        return []

def capture_n_photo_timeout_t(n, t):
    """ Capture n photos, 1 second apart, after a t-second timeout. """
    try:
        cap = open_camera()
        time.sleep(t)
        photos = capture_photos(cap, n, 1)
        cap.release()
        return photos
    except CameraError:
        return []
    except CaptureError:
        return []

## Utility (broken out for better error-handling)
def open_camera():
    """ Attempt to open the camera and handle failure immediately. """
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            error_msg = "Camera could not be accessed."
            print(f"Error: {error_msg}")
            raise CameraError(error_msg, errors=cap.get(cv2.CAP_PROP_ERR))
        return cap
    except cv2.error as e:
        error_msg = f"CV2 error occurred: {str(e)}"
        print(f"Error: {error_msg}")
        raise CameraError(error_msg)

def capture_photos(cap, count, interval):
    """ Capture a specified number of photos, logging errors immediately. """
    photos = []
    for i in range(count):
        try:
            ret, frame = cap.read()
            if not ret:
                error_msg = "Failed to capture photo."
                print(f"Error after {i} successful frames: {error_msg}")
                raise CaptureError(error_msg, frame_count=i)
            photos.append(frame)
            time.sleep(interval)
        except cv2.error as e:
            error_msg = f"CV2 error during capture: {str(e)}"
            print(f"Error after {i} successful frames: {error_msg}")
            raise CaptureError(error_msg, frame_count=i)
    return photos


#if __name__ == '__main__':
#    photos = capture_3_photo_timeout_5()
