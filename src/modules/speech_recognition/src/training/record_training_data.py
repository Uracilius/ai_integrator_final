import os
import csv
import sounddevice as sd
import wavio
from pydub import AudioSegment
from pydub.playback import play
import modules.speech_recognition.speech_recognition_controller as sr

def record_audio(duration=2, fs=16000):
    """Record audio for a given duration and sample rate."""
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Wait until the recording is finished
    return recording

def play_audio(recording, fs=16000):
    """Play back the recorded audio."""
    wavio.write('temp.wav', recording, fs, sampwidth=2)
    sound = AudioSegment.from_wav('temp.wav')
    play(sound)
    os.remove('temp.wav')

def save_recording(recording, filename, fs=16000):
    """Save the recording to a WAV file."""
    wavio.write(filename, recording, fs, sampwidth=2)

def recognize_command(recording, fs=16000):
    """Recognize spoken command from recording."""
    recognizer = sr.Recognizer()
    wavio.write('temp_command.wav', recording, fs, sampwidth=2)
    with sr.AudioFile('temp_command.wav') as source:
        audio_data = recognizer.record(source)
    os.remove('temp_command.wav')
    try:
        command = recognizer.recognize_google(audio_data).lower()
        return command
    except sr.UnknownValueError:
        return None

def get_last_word_index(filename):
    """Retrieve the last processed word's index from a file."""
    try:
        with open(filename, 'r') as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return 0  # If no file exists, start from the first word

def save_last_word_index(filename, index):
    """Save the last processed word's index to a file."""
    with open(filename, 'w') as f:
        f.write(str(index))

def main():
    words_file = 'src/modules/speech_recognition/src/training/google-10000-english-no-swears.txt'
    output_folder = 'src/modules/speech_recognition/src/training/training_data'
    last_word_file = 'src/modules/speech_recognition/src/training/last_word_index.txt'
    last_index = get_last_word_index(last_word_file)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(words_file, 'r') as file:
        reader = csv.reader(file, delimiter='\n')
        for index, row in enumerate(reader):
            if index < last_index:
                continue  # Skip to the next word if this one has been processed
            word = row[0].strip()
            while True:
                print(f"Please say the word '{word}'.")
                recording = record_audio()
                play_audio(recording)
                print("Say 'next' to save and proceed or 'record' to re-record.")
                command_recording = record_audio(duration=3)
                command = recognize_command(command_recording)

                while command not in ['next', 'record']:
                    print("Didn't catch that. Say 'next' to save and proceed or 'record' to re-record.")
                    command_recording = record_audio(duration=3)
                    command = recognize_command(command_recording)

                if command == 'next':
                    save_recording(recording, os.path.join(output_folder, f"{word}.wav"))
                    save_last_word_index(last_word_file, index + 1)  # Save the index of the next word
                    break  # Proceed to the next word

if __name__ == "__main__":
    main()
