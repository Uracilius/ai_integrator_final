from src.modules.face_recognition.src.input import capture_1_photo_timeout_5
from src.modules.face_recognition.src.input_processor import preprocess_image
from src.modules.face_recognition.src.db.connector import save_new_user, get_first_thing_in_collection, get_closest_face


def add_user(name):
    photo = capture_1_photo_timeout_5()
    face = preprocess_image(photo)
    
    if face is not None:
        result = save_new_user(face, name)[0]
        return result
    return [0, "I'm sorry, I couldn't see you clearly. Could you please consider trying again?"]

