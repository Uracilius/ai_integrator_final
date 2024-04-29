import vosk
import pyaudio
import wave
import os 

def listen_for_commands():
    base_dir = os.path.dirname(os.path.abspath(__file__)) + '/vosk-model-en-us-0.42-gigaspeech'
       
    model = vosk.Model(base_dir)
    recognizer = vosk.KaldiRecognizer(model, 16000)

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = 10  # Adjust recording duration as needed

    p = pyaudio.PyAudio()

    print("Listening indefinitely. Say 'over' to stop.")

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []

    while True:
        try:
            data = stream.read(CHUNK)
            frames.append(data)
            if len(frames) * CHUNK / RATE > RECORD_SECONDS:
                break
        except KeyboardInterrupt:
            print("Listening stopped by user")
            break
        except Exception as e:
            print("An error occurred:", e)
            break

    stream.stop_stream()
    stream.close()
    p.terminate()

    audio_data = b''.join(frames)

    recognizer.AcceptWaveform(audio_data)
    result = recognizer.FinalResult()

    if result:
        return result[0]

# Example usage:
if __name__ == "__main__":
    listen_for_commands()
