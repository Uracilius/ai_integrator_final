from input import capture_1_photo_timeout_5
from input_processor import preprocess_image


if __name__=='__main__':

    photo = capture_1_photo_timeout_5()
    
    face = preprocess_image(photo)
    
    if face is not None:
        print("Face detected and extracted.")
    else:
        print("No face detected.")