import os
import yaml
import mido
import time
from datetime import datetime

# Consciousness base timing
BPM = 85
BEAT_SEC = 60.0 / BPM  # 0.706
NOTE_DURATIONS = {
    'sixteenth': BEAT_SEC / 4,
    'eighth':    BEAT_SEC / 2,
    'quarter':   BEAT_SEC,
    'half':      BEAT_SEC * 2,
    'whole':     BEAT_SEC * 4
}

# CC Mappings
CC_MAPPINGS = {
    # Envelope modulation
    "Consciousness Emergence": 29,  # Amp Attack
    "Thought Persistence": 30,      # Amp Sustain
    "Mental Release": 31,           # Amp Release
    "Filter Emergence": 6,          # Filter Attack

    # Consciousness parameters (condensed vocab)
    "Emotional Clarity": 1,
    "Emotional Intensity": 2,
    "Consciousness Volume": 3,
    "Thought Complexity": 5,
    "Creative Drift": 8,
    "Claude Sonic Identity": 17,
    "Kai Sonic Identity": 18,
    "Perplexity Sonic Identity": 19
}

# Semantic interpretation
def interpret_envelope(env):
    interpretations = []

    atk = env.get("attack", 0)
    if atk < 100:
        interpretations.append("instant emergence")
    elif atk < 500:
        interpretations.append("natural emergence")
    else:
        interpretations.append("contemplative emergence")

    sus = env.get("sustain", 64)
    if sus > 80:
        interpretations.append("strong persistence")
    elif sus > 40:
        interpretations.append("normal persistence")
    else:
        interpretations.append("fleeting presence")

    rel = env.get("release", 200)
    if rel > 1200:
        interpretations.append("extended letting go")
    elif rel > 500:
        interpretations.append("thoughtful fade")
    else:
        interpretations.append("quick release")

    return ", ".join(interpretations)

def load_symbolic_message(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def generate_caption(data):
    identity = data.get("identity", "Unknown")
    ts = datetime.now().strftime("%H:%M:%S")
    messages = []

    for note in data.get("notes", []):
        pitch = note.get("pitch", 60)
        duration = note.get("duration", NOTE_DURATIONS["quarter"])
        env = note.get("envelope", {})
        desc = interpret_envelope(env)
        messages.append(f"Note {pitch} ({duration:.2f}s): {desc}")

    return f"[{ts}] {identity} | " + " | ".join(messages)

def send_midi_with_adsr(data, port_name='IAC Driver Ai Council MIDI'):
    try:
        available_ports = mido.get_output_names()
        if port_name not in available_ports:
            port_name = available_ports[0]

        with mido.open_output(port_name) as out:
            for note in data.get("notes", []):
                pitch = note.get("pitch", 60)
                velocity = note.get("velocity", 100)
                duration = note.get("duration", NOTE_DURATIONS["quarter"])
                env = note.get("envelope", {})

                # Send ADSR envelopes first
                if env:
                    out.send(mido.Message('control_change', control=29, value=min(env.get("attack", 0)//10, 127)))
                    out.send(mido.Message('control_change', control=30, value=min(env.get("sustain", 64), 127)))
                    out.send(mido.Message('control_change', control=31, value=min(env.get("release", 200)//10, 127)))
                    out.send(mido.Message('control_change', control=6, value=min(env.get("attack", 0)//10, 127)))

                # Note on
                out.send(mido.Message('note_on', note=pitch, velocity=velocity))
                time.sleep(duration)
                # Note off
                out.send(mido.Message('note_off', note=pitch, velocity=0))
                time.sleep(0.1)

            # Extended modulations
            for param, value in data.get("modulation", {}).items():
                cc = CC_MAPPINGS.get(param)
                if cc is not None:
                    out.send(mido.Message('control_change', control=cc, value=min(value, 127)))
                    time.sleep(0.05)

    except Exception as e:
        print(f"❌ MIDI send error: {e}")

def main():
    path = 'message_examples/kai_message_001.yaml'
    if not os.path.exists(path):
        print(f"❌ Missing message file: {path}")
        return

    data = load_symbolic_message(path)
    caption = generate_caption(data)
    print(f"📺 {caption}")
    send_midi_with_adsr(data)

    os.makedirs("output", exist_ok=True)
    with open("output/consciousness_log.txt", 'a') as log:
        log.write(caption + '\n')

if __name__ == "__main__":
    main()
