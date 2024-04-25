from src.modules.speech_recognition.speech_recognition_controller import listen_for_commands
from src.modules.face_recognition.face_recognition_controller import add_user, get_user
from src.modules.chat_api.chat_api_controller import ChatController
from src.modules.text_to_speech.text_to_speech import print_and_speak
def main_add_user():
    try:
        user_name = input("Give me the new user's name: ")
        add_user_result = add_user(user_name)
        print(f"User {user_name} added successfully.")
    except Exception as e:
        print(f"Failed to add user {user_name}. Error: {str(e)}")

def main_get_user():
    print_and_speak("Starting user identification procedure. Smile for the camera!")
    try:
        user_info = get_user()
        return user_info['metadatas']
    except Exception as e:
        print(f"Failed to find user. Error: {str(e)}")

def main_listen():
    try:
        command = listen_for_commands()
        return command
    except Exception as e:
        print(f"Error during listening for commands: {str(e)}")
        return ""

if __name__ == "__main__":
    user_name = None
    command = main_listen()  # Attempt to listen for commands safely

    if "add" in command and "user" in command:
        main_add_user()  # Attempt to add another user if the command includes "add user"
    elif "recognize" in command or "identify" in command:
        user_name = main_get_user()[0][0]['name']
        print(user_name)

    chat_controller = ChatController()
    
    if "else" in command or "new" in command or "different" in command:
        while user_name is None:
            user_name = main_get_user()[0][0]['name']
            print_and_speak("User identified:", user_name)
        print_and_speak(chat_controller.start_conversation(user_name=user_name, query=command))
    else:
        print_and_speak(chat_controller.continue_conversation(command))
    continue_convo = True
    
    while continue_convo:
        command = main_listen()
        print_and_speak(chat_controller.continue_conversation(command))
        if "end" in command and "conversation" in command:
            tags = chat_controller.extract_tags()
            continue_convo = False
    print(tags)
                 
