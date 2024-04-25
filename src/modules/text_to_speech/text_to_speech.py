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
    
    try:
        # Ensure the path is properly quoted to handle spaces
        safe_output_path = f"{output_path}"  # Enclose the path in quotes
        playsound.playsound(safe_output_path, block=True)
    finally:
        # Remove the output file after playing, ensuring cleanup even if playsound fails
        if os.path.exists(output_path):
            os.remove(output_path)
