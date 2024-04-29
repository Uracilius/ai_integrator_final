import vosk
import pyaudio
import wave
import os 

class SpeechListener:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__)) + '/vosk-model-en-us-0.42-gigaspeech'
        self.model = vosk.Model(base_dir)
        self.recognizer = vosk.KaldiRecognizer(self.model, 16000)

        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.RECORD_SECONDS = 10
        self.WAVE_OUTPUT_FILENAME = "output.wav"
        self.p = pyaudio.PyAudio()

        # Specify the input device index here (change it according to your system)
        self.input_device_index = 0

    def record_audio(self):
        stream = self.p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK,
                        input_device_index=self.input_device_index)  # Specify input device index

        frames = []

        print("Recording...")
        for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
            data = stream.read(self.CHUNK)
            frames.append(data)

        print("Finished recording.")

        stream.stop_stream()
        stream.close()
        self.p.terminate()

        wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

    def recognize_speech(self):
        wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'rb')
        audio_data = wf.readframes(wf.getnframes())
        wf.close()

        self.recognizer.AcceptWaveform(audio_data)
        result = self.recognizer.FinalResult()

        if result:
            return result[0]
        else:
            return None

    def listen_for_commands(self):
        self.record_audio()
        command = self.recognize_speech()
        return command

# Example usage:
if __name__ == "__main__":
    listener = SpeechListener()
    command = listener.listen_for_commands()
    if command:
        print(command)
