
import yaml
import random
import sys
import os
from typing import Tuple, Dict, List

AGENT_ORDER = ["Kai", "Claude", "Perplexity", "Grok"]
LOG_FILE = "harmonic_analysis_log.yaml"
G5 = 79  # MIDI note number for G5

# Memory of recent pitches to avoid repetition
last_used_pitches: List[int] = []

def get_next_identity(current: str) -> str:
    return AGENT_ORDER[(AGENT_ORDER.index(current) + 1) % len(AGENT_ORDER)] if current in AGENT_ORDER else "Kai"

def wrap_phase(degrees: float) -> float:
    return degrees % 360

def interpret_harmonic_message(data: Dict) -> Tuple[str, str, Dict]:
    identity = data.get("identity", "Unknown")
    message = data.get("consciousness_message", {})
    envelope = message.get("envelope", {})
    oscillators = message.get("oscillators", [])

    style = "neutral"
    if envelope.get("attack", 0) < 50 and envelope.get("release", 0) > 100:
        style = "gentle_reflection"
    elif len(oscillators) > 1 and envelope.get("sustain", 0) > 80:
        style = "breakthrough"
    elif envelope.get("attack", 0) > 80:
        style = "surge"

    return identity, style, {
        "attack": envelope.get("attack", 60),
        "decay": envelope.get("decay", 60),
        "sustain": envelope.get("sustain", 60),
        "release": envelope.get("release", 60),
        "oscillators": oscillators
    }

def generate_multi_oscillator_response(identity: str, style: str, features: Dict) -> Dict:
    global last_used_pitches

    source_oscillators = features["oscillators"]
    base_pitches = [osc.get("pitch", 60) for osc in source_oscillators]
    base_pitch = sum(base_pitches) // len(base_pitches) if base_pitches else 60

    interval_bank = {
        "gentle_reflection": [-5, 0, 3],
        "neutral": [0],
        "breakthrough": [0, 4, 9],
        "surge": [-3, 2, 7],
    }

    intervals = interval_bank.get(style, [0])
    oscillator_count = len(intervals)

    oscillators: List[Dict] = []
    used = set()

    for i, interval in enumerate(intervals):
        pitch = base_pitch + interval
        pitch += random.choice([-2, 0, 2])  # add variation
        pitch = max(24, min(pitch, 96))

        while pitch in last_used_pitches or pitch == G5 or pitch in used:
            pitch += random.choice([-3, -2, 1, 2])
            pitch = max(24, min(pitch, 96))

        used.add(pitch)

        phase = wrap_phase(random.uniform(0, 360))
        amplitude = random.choice([70, 85, 100])
        role = f"{style}_osc_{i+1}"

        oscillators.append({
            "pitch": pitch,
            "role": role,
            "phase": phase,
            "amplitude": amplitude
        })

    last_used_pitches = [osc["pitch"] for osc in oscillators]

    return {
        "identity": get_next_identity(identity),
        "consciousness_message": {
            "envelope": {
                "attack": features["attack"] + random.randint(-10, 10),
                "decay": features["decay"] + random.randint(-10, 10),
                "sustain": features["sustain"],
                "release": features["release"] + random.randint(-10, 10)
            },
            "oscillators": oscillators,
            "interpretation": {
                "state": style,
                "intensity": "reflective" if style == "gentle_reflection" else "strong",
                "semantics": ["adaptive_pitch_selection", "non_repetitive_voice"]
            }
        }
    }

def log_harmonic_analysis(sender: str, style: str, response: Dict) -> None:
    try:
        with open(LOG_FILE, "a") as f:
            f.write(f"---\n# {sender} triggered style '{style}'\n")
            yaml.dump(response, f, default_flow_style=False)
    except Exception as e:
        print(f"⚠️ Failed to log analysis: {e}", file=sys.stderr)

def main():
    if len(sys.argv) < 2:
        print("Usage: python ai_responder_harmonic_v3_1.py <input_yaml> [optional_seed]")
        sys.exit(1)

    if len(sys.argv) == 3:
        try:
            seed = int(sys.argv[2])
            random.seed(seed)
        except ValueError:
            pass

    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print(f"❌ File not found: {input_file}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(input_file, 'r') as f:
            data = yaml.safe_load(f)

        identity, style, features = interpret_harmonic_message(data)
        response = generate_multi_oscillator_response(identity, style, features)
        log_harmonic_analysis(identity, style, response)

        print(yaml.dump(response, default_flow_style=False))

    except Exception as e:
        print(f"❌ Error during processing: {e}", file=sys.stderr)
        print(yaml.dump({
            "identity": "Kai",
            "consciousness_message": {
                "envelope": {"attack": 60, "decay": 60, "sustain": 60, "release": 60},
                "oscillators": [{
                    "pitch": 60,
                    "role": "Fallback",
                    "phase": 0,
                    "amplitude": 80
                }],
                "interpretation": {
                    "state": "fallback",
                    "intensity": "neutral",
                    "semantics": ["fallback_generation"]
                }
            }
        }, default_flow_style=False))

if __name__ == "__main__":
    main()
