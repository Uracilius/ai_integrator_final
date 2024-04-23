from src.modules.speech_recognition.speech_recognition_controller import listen_for_commands
from src.modules.face_recognition.face_recognition_controller import add_user

if __name__ == "__main__":
    command = listen_for_commands()
    if "add" in command and "user" in command:
        add_user(input("give me the new user's name"))
