import mido
import time

port_name = "IAC Driver Ai Council MIDI"
cc_values = {
    1: 100,    # Emotional Clarity
    5: 100,    # Thought Complexity
    17: 100    # Sonic Identity
}

with mido.open_output(port_name) as out:
    print("🎛️ Blasting CC test values...")
    for cc, val in cc_values.items():
        msg = mido.Message('control_change', control=cc, value=val)
        out.send(msg)
        print(f"✅ Sent CC{cc} = {val}")
        time.sleep(0.3)
