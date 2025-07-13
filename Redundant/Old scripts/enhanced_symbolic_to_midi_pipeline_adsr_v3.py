
import mido
import yaml
import time

# Mapping of agent names to MIDI channels (0–15)
AGENT_CHANNEL_MAP = {
    'kai': 0,
    'claude': 1,
    'perplexity': 2,
    'grok': 3
}

def load_symbolic_message(path):
    with open(path, 'r') as file:
        return yaml.safe_load(file)

def open_midi_port(port_name='IAC Driver Ai Council MIDI'):
    available_ports = mido.get_output_names()
    if port_name not in available_ports:
        print("⚠️ MIDI port not found. Available ports:")
        for port in available_ports:
            print(" -", port)
        exit(1)
    return mido.open_output(port_name)

def send_midi_message(message):
    agent = message['identity'].lower()
    if agent not in AGENT_CHANNEL_MAP:
        print(f"⚠️ Warning: Unknown agent identity '{agent}', defaulting to channel 0 (Kai)")
    channel = AGENT_CHANNEL_MAP.get(agent, 0)
    print(f"🎛️ Sending message from {agent} on MIDI channel {channel + 1}")

    outport = open_midi_port()

    # Send ADSR envelope as CC values (optional)
    envelope = message['consciousness_message'].get('envelope', {})
    if envelope:
        cc_map = {28: envelope.get('attack', 0),
                  29: envelope.get('decay', 0),
                  30: envelope.get('sustain', 0),
                  31: envelope.get('release', 0)}
        for cc, val in cc_map.items():
            outport.send(mido.Message('control_change', control=cc, value=min(val, 127), channel=channel))

    oscillators = message['consciousness_message'].get('oscillators', [])
    for osc in oscillators:
        pitch = osc.get('pitch', 60)
        amplitude = osc.get('amplitude', 100)
        velocity = int((amplitude / 100) * 127)

        print(f"🎵 Note ON | Pitch: {pitch}, Velocity: {velocity}, Channel: {channel + 1}")
        note_on = mido.Message('note_on', note=pitch, velocity=velocity, channel=channel)
        outport.send(note_on)

        time.sleep(0.5)  # Adjustable duration

        print(f"🎵 Note OFF | Pitch: {pitch}, Channel: {channel + 1}")
        note_off = mido.Message('note_off', note=pitch, velocity=0, channel=channel)
        outport.send(note_off)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python enhanced_symbolic_to_midi_pipeline_adsr_v3.py <path_to_yaml>")
        sys.exit(1)

    msg_path = sys.argv[1]
    msg = load_symbolic_message(msg_path)
    send_midi_message(msg)
