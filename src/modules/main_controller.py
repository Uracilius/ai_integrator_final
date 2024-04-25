from src.modules.speech_recognition.speech_recognition_controller import listen_for_commands
from src.modules.face_recognition.face_recognition_controller import add_user, get_user
from src.modules.chat_api.chat_api_controller import ChatController
from src.modules.text_to_speech.text_to_speech import print_and_speak
from src.modules.context_manager.context_manager_controller import add_chat_to_context, get_convo_context
from src.modules.shared.DTO.chroma_response import ChromaResponse
from src.modules.shared.DTO.context_data import ContextDTO

def main_add_user():
    print_and_speak("Starting user registration procedure. Smile for the camera!")
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
        return user_info
    except Exception as e:
        print(f"Failed to find user. Error: {str(e)}")

if __name__ == "__main__":
    user_name = None
    chat_controller = ChatController()
    context = ContextDTO()
    user_info = None
    continue_convo = True

    while continue_convo:
        command = listen_for_commands()
        if "end" in command and "conversation" in command:
            tags = chat_controller.extract_tags()
            context.tags=tags.split(", ")
            continue_convo = False
        elif "add" in command and "user" in command:
            main_add_user()
        elif "recognize" in command or "identify" in command:
            user_info = ChromaResponse(main_get_user()).get_first_item()
            print(user_name)
        elif "else" in command or "new" in command or "different" in command:
            while user_info is None:
                user_info = ChromaResponse(main_get_user()).get_first_item()
                user_name = user_info['metadata']['name']
                print_and_speak("User identified:", user_name)
            print_and_speak(chat_controller.start_conversation(user_name=user_name, query=command))
        elif "remember" in command:
            while user_info is None:
                user_info = ChromaResponse(main_get_user()).get_first_item()
                context.user_id = user_info['id']
                user_name = user_info['metadata']['name']
                print_and_speak("User identified:", user_name)
            user_info, chat_controller.conversation_history = get_convo_context(command, user_info['id'])
            print_and_speak(chat_controller.continue_conversation(command))
        else:
            print_and_speak(chat_controller.continue_conversation(command))
    
    add_chat_to_context(chat_controller.conversation_history,context)
                 
