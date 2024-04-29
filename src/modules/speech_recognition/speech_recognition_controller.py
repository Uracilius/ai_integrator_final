import vosk
import pyaudio
import wave
import os 
import json

class CommandListener:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__)) + '/vosk-model-en-us-0.42-gigaspeech'
        self.model = vosk.Model(base_dir)
        self.recognizer = vosk.KaldiRecognizer(self.model, 16000)

        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.RECORD_SECONDS = 10

    def listen_for_commands(self):
        p = pyaudio.PyAudio()

        print("Listening indefinitely. Say 'over' to stop.")

        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)

        frames = []

        while True:
            try:
                data = stream.read(self.CHUNK)
                frames.append(data)
                if len(frames) * self.CHUNK / self.RATE > self.RECORD_SECONDS:
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

        self.recognizer.AcceptWaveform(audio_data)
        result = json.loads(self.recognizer.FinalResult())

        if result:
            return result["text"]

# Example usage:
if __name__ == "__main__":
    listener = CommandListener()
    print(listener.listen_for_commands())
