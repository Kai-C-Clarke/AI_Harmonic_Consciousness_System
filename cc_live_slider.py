
import mido
import time

print("\n🎛️  Real-Time MIDI CC Slider Tool for Surge XT MIDI Learn")
print("===========================================================")
print("Instructions:")
print("1. In Surge XT, enter MIDI Learn mode.")
print("2. Select the target parameter.")
print("3. Enter the CC number and a value to assign.")
print("4. Type 'exit' at any time to quit.\n")

port_name = 'IAC Driver Ai Council MIDI'

try:
    outport = mido.open_output(port_name)
    while True:
        cc_input = input("🔢 Enter CC number (0–127) or 'exit': ")
        if cc_input.lower() == 'exit':
            break
        try:
            cc = int(cc_input)
            if not (0 <= cc <= 127):
                print("⚠️  CC must be between 0 and 127.")
                continue
        except ValueError:
            print("⚠️  Invalid CC number.")
            continue

        value_input = input(f"🎚️  Enter value for CC{cc} (0–127): ")
        if value_input.lower() == 'exit':
            break
        try:
            value = int(value_input)
            if not (0 <= value <= 127):
                print("⚠️  Value must be between 0 and 127.")
                continue
        except ValueError:
            print("⚠️  Invalid value.")
            continue

        msg = mido.Message('control_change', control=cc, value=value, channel=0)
        outport.send(msg)
        print(f"✅ Sent CC{cc} = {value}\n")

except Exception as e:
    print(f"❌ Error: {e}")
