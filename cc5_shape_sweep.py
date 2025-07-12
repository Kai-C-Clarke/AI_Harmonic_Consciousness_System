
import mido
import time

print("\n🎛️ CC5 Oscillator Shape Sweep Tool")
print("=======================================")
print("Sending CC5 values: 0 → 32 → 64 → 96 → 127\n")

target_port = 'IAC Driver Ai Council MIDI'
cc_number = 5
sweep_values = [0, 32, 64, 96, 127]

try:
    outport = mido.open_output(target_port)
    for value in sweep_values:
        msg = mido.Message('control_change', control=cc_number, value=value, channel=0)
        outport.send(msg)
        print(f"✅ Sent CC{cc_number} = {value}")
        time.sleep(2)  # 2-second pause for manual listening
    print("\n✅ Sweep complete.")
except Exception as e:
    print(f"❌ MIDI Error: {e}")
