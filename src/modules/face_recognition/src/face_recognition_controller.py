from input import capture_1_photo_timeout_5
from input_processor import preprocess_image
from db.connector import save_image, get_first_thing_in_collection, get_closest_face

if __name__=='__main__':
    
    photo = capture_1_photo_timeout_5()
    
    face = preprocess_image(photo)
    
    if face is not None:
        #save_image(face)
        print(get_closest_face(face))
        #print('Finished adding face to database.')
    else:
        print("No face detected.")