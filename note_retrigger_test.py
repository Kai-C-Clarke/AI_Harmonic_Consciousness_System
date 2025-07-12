import mido
import time
import random

PORT_NAME = 'IAC Driver Ai Council MIDI'
out = mido.open_output(PORT_NAME)
print(f"✅ Connected to {PORT_NAME}")

base_note = 62  # D4
base_velocity = 80
cc_values = {
    1: 75,   # Emotional Clarity
    5: 70,   # Thought Complexity
    17: 64   # Claude Sonic Identity
}

for i in range(3):
    note = base_note + i
    velocity = base_velocity + random.randint(-5, 5)
    print(f"\n🎵 Triggering note: {note} | Velocity: {velocity}")
    
    for cc, val in cc_values.items():
        out.send(mido.Message('control_change', control=cc, value=val))
        print(f"✅ Sent CC{cc} = {val}")
    
    out.send(mido.Message('note_on', note=note, velocity=velocity))
    time.sleep(0.5)
    out.send(mido.Message('note_off', note=note))
    print("✅ Note played and released")

    time.sleep(1)

print("\n✅ Done — note retrigger test completed.")
