import speech_recognition as sr

def listen_for_commands():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening indefinitely. Say 'over' to stop.")
        recognizer.adjust_for_ambient_noise(source)

        while True:
            try:
                audio = recognizer.listen(source)
                phrase = recognizer.recognize_google(audio)
                print('You said:', phrase)

                if 'over' in phrase.lower():
                    return phrase

            except sr.UnknownValueError:
                # This exception is raised if the speech is unintelligible
                print("Could not understand audio")
            except sr.RequestError as e:
                # This exception is raised if there’s a problem with the Google API or internet connection
                print("Could not request results; {0}".format(e))
            except Exception as e:
                # General exception for any other issues that might arise
                print("An error occurred: {0}".format(e))


