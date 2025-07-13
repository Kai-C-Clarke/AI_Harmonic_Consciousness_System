
import mido
import yaml
import time

# Load symbolic message from YAML
def load_symbolic_message(path):
    with open(path, 'r') as file:
        return yaml.safe_load(file)

# Map agent names to MIDI channels
AGENT_CHANNEL_MAP = {
    'kai': 0,
    'claude': 1,
    'perplexity': 2,
    'grok': 3
}

# Convert symbolic message to MIDI
def send_midi_message(message):
    agent = message['identity']['agent'].lower()
    channel = AGENT_CHANNEL_MAP.get(agent, 0)
    pitch = message['pitch']['value']
    velocity = int((message['amplitude']['value'] / 100) * 127)

    adsr = message['amplitude']['envelope']
    attack = adsr['attack'] / 1000
    decay = adsr['decay'] / 1000
    sustain = adsr['sustain']
    release = adsr['release'] / 1000

    outport = mido.open_output('IAC Driver Ai Council MIDI')

    # Note on
    note_on = mido.Message('note_on', note=pitch, velocity=velocity, channel=channel)
    outport.send(note_on)

    # Simulate ADSR with sleep for now (approximate)
    time.sleep(attack + decay + release)

    # Note off
    note_off = mido.Message('note_off', note=pitch, velocity=0, channel=channel)
    outport.send(note_off)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python enhanced_symbolic_to_midi_pipeline_adsr_fixed.py <path_to_yaml>")
        sys.exit(1)

    message_path = sys.argv[1]
    symbolic_message = load_symbolic_message(message_path)
    send_midi_message(symbolic_message)
