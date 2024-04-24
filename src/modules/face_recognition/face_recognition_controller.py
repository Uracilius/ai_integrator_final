from .src.input import capture_1_photo_timeout_5, capture_n_photo_timeout_t
from .src.input_processor import preprocess_image
from .src.db.connector import save_new_user, get_closest_face

def add_user(name):
    photo = capture_1_photo_timeout_5()
    if photo is None:
        raise Exception("Failed to capture a photo. Please ensure the camera is connected and functional.")

    face = preprocess_image(photo)
    if face is None:
        raise ValueError("No detectable face found in the photo. Please ensure your face is visible and well-lit.")

    message = save_new_user(face, name)
    
    return "User added successfully."


def get_user():
    photo = capture_1_photo_timeout_5()
    if photo is None:
        raise Exception("Failed to capture a photo. Please ensure the camera is connected and functional.")
    
    face = preprocess_image(photo)
    if face is None:
        raise ValueError("No detectable face found in the photo. Please ensure your face is visible and well-lit.")
    
    return get_closest_face(face)


#if __name__ == '__main__':
#    user_name = "John Doe"
#    try:
#        message = add_user(user_name)
#        print(message)
#    except Exception as e:
#        print(f"Error: {str(e)}")
