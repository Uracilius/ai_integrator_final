import os
import json
from pocketsphinx import LiveSpeech, get_model_path


CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config', 'config.json')

def load_config(path):
    with open(path, 'r') as config_file:
        config = json.load(config_file)
    return config

def initialize_sphinx():
    config = load_config(CONFIG_PATH) 
    model_path = get_model_path()
    speech = LiveSpeech(
        verbose=config['verbose'],
        sampling_rate=config['sampling_rate'],
        buffer_size=config['buffer_size'],
        no_search=config['no_search'],
        full_utt=config['full_utt'],
        hmm=os.path.join(model_path, config['hmm']),
        lm=os.path.join(model_path, config['lm']),
        dic=os.path.join(model_path, config['dic'])
    )
    return speech

