import mido
import time

# Use the correct port name (exactly as shown)
outport = mido.open_output('IAC Driver Ai Council MIDI')

print("Sending test CC messages to Surge XT...")

# Send test CC sweep
for value in range(0, 128, 10):
    msg = mido.Message('control_change', channel=0, control=1, value=value)
    outport.send(msg)
    print(f"Sent CC1 = {value}")
    time.sleep(0.2)

print("Test complete!")
outport.close()