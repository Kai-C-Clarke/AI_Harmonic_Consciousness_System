import mido
import time

port_name = "IAC Driver Ai Council MIDI"

print("🎛️ AI Council Oscillator Modulation Test")
with mido.open_output(port_name) as out:
    print("🔄 Sweeping CC23 (Detune)...")
    for val in range(0, 128, 32):
        out.send(mido.Message('control_change', control=23, value=val))
        print(f"✅ CC23 = {val}")
        time.sleep(0.3)

    print("🔁 Sweeping CC24 (Wave Shape)...")
    for val in [0, 32, 64, 96, 127]:
        out.send(mido.Message('control_change', control=24, value=val))
        print(f"✅ CC24 = {val}")
        time.sleep(0.4)

print("🎯 Test complete — observe Surge XT for detune & wave shape modulation.")
