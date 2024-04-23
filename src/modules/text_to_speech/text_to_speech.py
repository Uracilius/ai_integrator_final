from gtts import gTTS
import os
import playsound

def print_and_speak(*args, **kwargs):
    message = ' '.join(map(str, args))
    
    # Get the directory path of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Set the path for saving the output file
    output_path = os.path.join(script_dir, "output.mp3")
    
    tts = gTTS(text=message, lang='en', slow=False)
    tts.save(output_path)
    
    # Play the audio file
    playsound.playsound(output_path)
    
    # Remove the output file after playing
    os.remove(output_path)
