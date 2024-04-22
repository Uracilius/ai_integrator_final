from .src.sphinx import initialize_sphinx


def listen_for_commands():
    speech_recognizer = initialize_sphinx()
    print("Listening indefinitely. Say 'quit' to stop.")

    try:
        for phrase in speech_recognizer:
            print('You said:', phrase)
            if str(phrase).strip().lower() == 'over':
                return phrase
    except KeyboardInterrupt:
        print("Stopped by user.")
        

