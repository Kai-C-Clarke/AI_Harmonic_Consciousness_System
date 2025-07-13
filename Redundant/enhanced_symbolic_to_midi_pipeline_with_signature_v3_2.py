
# enhanced_symbolic_to_midi_pipeline_with_signature_v3_2.py

import mido
import yaml
import time

def clamp_midi(val):
    return max(0, min(int(val), 127))

def open_midi_port(name="IAC Driver Ai Council MIDI"):
    available = mido.get_output_names()
    for port in available:
        if name in port:
            return mido.open_output(port)
    raise Exception(f"MIDI port '{name}' not found. Available: {available}")

def send_signature_pulse(pulse, outport, force=False):
    channel = pulse.get("channel", 15)
    if not force and channel == 15:  # assume channel 16 is reserved
        print("⚠️ Channel 16 may be in use. Skipping signature unless forced.")
        return

    conf = pulse.get("confidence_modulation", {})
    env = pulse.get("envelope", {})

    for note_event in pulse.get("pattern", []):
        note = note_event["note"]
        velocity = clamp_midi(note_event.get("velocity", 100) + conf.get("velocity_bias", 0))
        duration = note_event.get("duration", 0.3)
        delay = conf.get("timing_offset", 0.0)

        outport.send(mido.Message("note_on", note=note, velocity=velocity, channel=channel))
        time.sleep(max(0.01, duration + delay))
        outport.send(mido.Message("note_off", note=note, velocity=0, channel=channel))

    for cc in pulse.get("cc_signature", []):
        outport.send(mido.Message("control_change", control=cc["controller"], value=cc["value"], channel=channel))

def send_consciousness_message(msg, outport):
    agent = msg["identity"].lower()
    channel = {
        "kai": 0, "claude": 1, "perplexity": 2, "grok": 3
    }.get(agent, 0)

    env = msg["consciousness_message"].get("envelope", {})
    sustain = env.get("sustain", 0.5)
    sustain_val = clamp_midi(sustain * 127) if sustain <= 1.0 else clamp_midi(sustain)

    cc_map = {
        28: clamp_midi(env.get("attack", 0) * 127),
        29: clamp_midi(env.get("decay", 0) * 127),
        30: sustain_val,
        31: clamp_midi(env.get("release", 0) * 127)
    }

    for cc, value in cc_map.items():
        outport.send(mido.Message("control_change", control=cc, value=value, channel=channel))

    for osc in msg["consciousness_message"]["oscillators"]:
        note = osc.get("pitch", 60)
        amp = clamp_midi((osc.get("amplitude", 100) / 100) * 127)
        outport.send(mido.Message("note_on", note=note, velocity=amp, channel=channel))
        time.sleep(0.4)
        outport.send(mido.Message("note_off", note=note, velocity=0, channel=channel))

if __name__ == "__main__":
    import sys
    try:
        with open(sys.argv[1], "r") as f:
            message = yaml.safe_load(f)

        outport = open_midi_port()
        if "signature_pulse" in message:
            send_signature_pulse(message["signature_pulse"], outport, force=False)
        send_consciousness_message(message, outport)
        print("✅ MIDI message sent successfully.")
    except Exception as e:
        print(f"❌ MIDI transmission error: {e}")
