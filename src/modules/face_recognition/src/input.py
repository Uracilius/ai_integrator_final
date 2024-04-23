import cv2
import time

def capture_1_photo_timeout_5():
    """ Capture 1 photo after a 5-second timeout. """
    cap = open_camera()
    if cap is None:
        return None

    time.sleep(5)
    photos = capture_photos(cap, 1, 0)
    cap.release()
    return photos[0] if photos else None

def capture_3_photo_timeout_5():
    """ Capture 3 photos, 1 second apart, after a 5-second timeout. """
    cap = open_camera()
    if cap is None:
        return []

    time.sleep(5)
    photos = capture_photos(cap, 3, 1)
    cap.release()
    return photos

def capture_n_photo_timeout_t(n, t):
    """ Capture n photos, 1 second apart, after a t-second timeout. """
    cap = open_camera()
    if cap is None:
        return []

    time.sleep(t)
    photos = capture_photos(cap, n, 1)
    cap.release()
    return photos

##Utility (broken out for better error-handling)
def open_camera():
    """ Attempt to open the camera and return the camera object or None if unsuccessful. """
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Camera could not be accessed.")
        return None
    return cap

def capture_photos(cap, count, interval):
    """ Capture a specified number of photos with a given interval using the provided camera object. """
    photos = []
    for i in range(count):
        ret, frame = cap.read()
        if ret:
            photos.append(frame)
        time.sleep(interval)
    return photos

if __name__ == '__main__':
    photos = capture_3_photo_timeout_5()
