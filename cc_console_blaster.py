import mido
import time

# Define CC test map with large, distinct value swings
test_ccs = [
    {"cc": 1, "name": "Filter Cutoff", "values": [0, 127, 64]},
    {"cc": 29, "name": "Amp Attack", "values": [0, 127, 64]},
    {"cc": 30, "name": "Amp Sustain", "values": [0, 127, 64]},
    {"cc": 31, "name": "Amp Release", "values": [0, 127, 64]},
    {"cc": 5, "name": "Osc Shape", "values": [0, 127, 64]},
    {"cc": 3, "name": "Scene Volume", "values": [0, 127, 64]},
]

# MIDI port name to target
target_port = 'IAC Driver Ai Council MIDI'

try:
    with mido.open_output(target_port) as out:
        for entry in test_ccs:
            cc = entry["cc"]
            name = entry["name"]
            for val in entry["values"]:
                msg = mido.Message('control_change', control=cc, value=val, channel=0)
                out.send(msg)
                print(f"🎛️ Sent CC{cc} ({name}) = {val}")
                time.sleep(1)
except Exception as e:
    print(f"❌ MIDI Error: {e}")
