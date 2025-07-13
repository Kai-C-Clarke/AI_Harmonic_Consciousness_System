# enhanced_symbolic_to_midi_pipeline_with_signature_v3_2.py

import mido
import yaml
import time
import sys
from typing import Any, Dict, Optional

# MIDI CC constants for envelope shaping
CC_ATTACK = 28
CC_DECAY = 29
CC_SUSTAIN = 30
CC_RELEASE = 31

# Default MIDI port name
DEFAULT_MIDI_PORT = "IAC Driver Ai Council MIDI"

def clamp_midi(val: float) -> int:
    """Clamp a value to the valid MIDI range [0, 127]."""
    return max(0, min(int(val), 127))

def open_midi_port(name: str = DEFAULT_MIDI_PORT):
    """
    Open a MIDI output port by (partial) name match.
    Args:
        name: The name (or part of the name) of the MIDI port.
    Returns:
        A mido output port object.
    Raises:
        Exception if the port cannot be found.
    """
    available = mido.get_output_names()
    for port in available:
        if name in port:
            return mido.open_output(port)
    raise Exception(f"MIDI port '{name}' not found. Available: {available}")

def send_signature_pulse(pulse: Dict[str, Any], outport, force: bool = False) -> None:
    """
    Send a signature pulse as a series of MIDI note and CC events.
    Args:
        pulse: Dictionary containing pattern, cc_signature, confidence_modulation, envelope, and channel.
        outport: mido output port to send messages to.
        force: If True, override channel 16 warning.
    """
    channel = pulse.get("channel", 15)
    if not force and channel == 15:  # MIDI channels are 0-based; 15 is channel 16
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
        # This timing is not sample-accurate; for critical timing, consider a scheduling library
        time.sleep(max(0.01, duration + delay))
        outport.send(mido.Message("note_off", note=note, velocity=0, channel=channel))

    for cc in pulse.get("cc_signature", []):
        outport.send(mido.Message("control_change", control=cc["controller"], value=cc["value"], channel=channel))

def send_consciousness_message(msg: Dict[str, Any], outport) -> None:
    """
    Send a 'consciousness message' as a series of MIDI envelope and note events.
    Args:
        msg: Dictionary containing 'identity' and 'consciousness_message' keys.
        outport: mido output port to send messages to.
    """
    agent = msg.get("identity", "").lower()
    channel_map = {"kai": 0, "claude": 1, "perplexity": 2, "grok": 3}
    channel = channel_map.get(agent, 0)

    cmsg = msg.get("consciousness_message", {})
    env = cmsg.get("envelope", {})

    # Provide more musical defaults
    sustain = env.get("sustain", 0.7)
    attack = env.get("attack", 0.01)
    decay = env.get("decay", 0.1)
    release = env.get("release", 0.2)

    sustain_val = clamp_midi(sustain * 127) if sustain <= 1.0 else clamp_midi(sustain)

    cc_map = {
        CC_ATTACK: clamp_midi(attack * 127),
        CC_DECAY: clamp_midi(decay * 127),
        CC_SUSTAIN: sustain_val,
        CC_RELEASE: clamp_midi(release * 127)
    }

    # Send envelope CCs
    for cc, value in cc_map.items():
        outport.send(mido.Message("control_change", control=cc, value=value, channel=channel))

    for osc in cmsg.get("oscillators", []):
        note = osc.get("pitch", 60)
        amp = clamp_midi((osc.get("amplitude", 100) / 100) * 127)
        outport.send(mido.Message("note_on", note=note, velocity=amp, channel=channel))
        time.sleep(0.4)
        outport.send(mido.Message("note_off", note=note, velocity=0, channel=channel))

def validate_message(message: Dict[str, Any]) -> None:
    """
    Validate the structure of the message YAML.
    Raises descriptive errors if required keys are missing.
    """
    if "identity" not in message:
        raise ValueError("YAML must contain 'identity' key.")
    if "consciousness_message" not in message:
        raise ValueError("YAML must contain 'consciousness_message' key.")
    if "oscillators" not in message["consciousness_message"]:
        raise ValueError("YAML 'consciousness_message' must contain 'oscillators' key.")

def main():
    """
    Main entry point: parses command-line args, loads YAML, opens MIDI port, and sends messages.
    """
    import argparse

    parser = argparse.ArgumentParser(description="Send symbolic-to-MIDI messages from a YAML input file.")
    parser.add_argument("yaml_file", help="YAML file containing consciousness message.")
    parser.add_argument("--midi-port", default=DEFAULT_MIDI_PORT, help="MIDI port name (partial match allowed).")
    parser.add_argument("--force-signature", action="store_true", help="Force sending signature pulse on channel 16.")
    args = parser.parse_args()

    try:
        with open(args.yaml_file) as f:
            message = yaml.safe_load(f)
        validate_message(message)
        outport = open_midi_port(args.midi_port)
        if "signature_pulse" in message:
            send_signature_pulse(message["signature_pulse"], outport, force=args.force_signature)
        send_consciousness_message(message, outport)
        print("✅ MIDI message sent successfully.")
    except Exception as e:
        print(f"❌ MIDI transmission error: {e}")

if __name__ == "__main__":
    main()