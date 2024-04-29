from src.modules.speech_recognition.speech_recognition_controller import listen_for_commands
from src.modules.face_recognition.face_recognition_controller import add_user, get_user
from src.modules.chat_api.chat_api_controller import ChatController
from src.modules.context_manager.context_manager_controller import add_chat_to_context, get_convo_context
from src.modules.shared.DTO.chroma_response import ChromaResponse
from src.modules.shared.DTO.context_data import ContextDTO
from src.modules.text_to_speech.glados import TTS_Engine

user_info = None
continue_convo = True
tags = None
chat_controller = ChatController()
tts_engine = TTS_Engine()

def main_add_user():
    try:
        user_name = input("Give me the new user's name: ")
        add_user_result = add_user(user_name)
        if add_user_result:  # Assuming add_user returns a truthy value on success
            print(f"User {user_name} added successfully.")
        else:
            print(f"Failed to add user {user_name}.")
    except Exception as e:
        print(f"Failed to add user. Error: {str(e)}")

def main_identify_user():
    global user_info  # Declare global to modify the global variable
    try:
        user_info = ChromaResponse(get_user()).get_first_item()
        if user_info is None:
            print("No user found.")
    except Exception as e:
        print(f"Failed to find user. Error: {str(e)}")

def main_recognize_command(command):
    global user_info, continue_convo, tags  # Declare global to modify the global variables
    if user_info is None:
        main_identify_user()
    if "end" in command and "conversation" in command:
        extract_tags_end_conversation()
    elif "add" in command and "user" in command:
        main_add_user()
    elif "else" in command or "new" in command or "different" in command:
        new_chat_response = chat_controller.start_conversation(user_name=user_info['metadata']['name'], query=command)
        tts_engine.print_and_speak(new_chat_response)
    elif "remember" in command:
        user_info, chat_controller.conversation_history = get_convo_context(command, user_info['id'])
        tts_engine.print_and_speak(chat_controller.continue_conversation(command))
    else:
        tts_engine.print_and_speak(chat_controller.continue_conversation(command))

def extract_tags_end_conversation():
    global continue_convo  # Declare global to modify the global variable
    global tags
    tags = chat_controller.extract_tags()
    continue_convo = False

if __name__ == "__main__":
    tts_engine.print_and_speak("Online and ready. Give your command.")

    while continue_convo:
        command = input("Give your command: ")
        # command = listen_for_commands()
        main_recognize_command(command)
    if tags:
        add_chat_to_context(chat_controller.conversation_history, ContextDTO(user_id=user_info['id'], tags=tags.split(', ')))