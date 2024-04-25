import torch
from .utils.tools import prepare_text
from scipy.io.wavfile import write
import time
from sys import modules as mod
import os
try:
    import winsound
except ImportError:
    from subprocess import call


class TTS_Engine:
    def __init__(self):
        print("Initializing TTS Engine...")
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        base_dir = os.path.dirname(os.path.abspath(__file__))
        glados_path = os.path.join(base_dir, 'models', 'glados.pt')
        vocoder_path = os.path.join(base_dir, 'models', 'vocoder-gpu.pt')
        
        self.glados = torch.jit.load(glados_path)
        self.vocoder = torch.jit.load(vocoder_path, map_location=self.device)

        # Prepare models in RAM
        for i in range(4):
            init = self.glados.generate_jit(prepare_text(str(i)))
            init_mel = init['mel_post'].to(self.device)
            self.vocoder(init_mel)
        print("TTS Engine initialized")

    def print_and_speak(self, *args):
        text = ' '.join(map(str, args))

        # Tokenize, clean, and phonemize input text
        x = prepare_text(text).to('cpu')

        with torch.no_grad():
            # Generate generic TTS-output
            old_time = time.time()
            tts_output = self.glados.generate_jit(x)
            #print("Forward Tacotron took " + str((time.time() - old_time) * 1000) + "ms")

            # Use HiFiGAN as vocoder to make output sound like GLaDOS
            old_time = time.time()
            mel = tts_output['mel_post'].to(self.device)
            audio = self.vocoder(mel)
            #print("HiFiGAN took " + str((time.time() - old_time) * 1000) + "ms")
            
            # Normalize audio to fit in wav-file
            audio = audio.squeeze()
            audio = audio * 32768.0
            audio = audio.cpu().numpy().astype('int16')
            output_file = ('output.wav')
            
            # Write audio file to disk
            write(output_file, 22050, audio)

            # Play audio file
            if 'winsound' in mod:
                winsound.PlaySound(output_file, winsound.SND_FILENAME)
            else:
                call(["aplay", "./output.wav"])