
import yaml
import random
import sys
import os
from typing import Tuple, Dict, List

AGENT_ORDER = ["Kai", "Claude", "Perplexity", "Grok"]
LOG_FILE = "harmonic_analysis_log.yaml"

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
    source_oscillators = features["oscillators"]
    base_pitches = [osc.get("pitch", 60) for osc in source_oscillators]
    base_pitch = sum(base_pitches) // len(base_pitches) if base_pitches else 60

    oscillator_count = {
        "gentle_reflection": 1,
        "neutral": 1,
        "breakthrough": 2,
        "surge": 3
    }.get(style, 1)

    intervals = {
        "gentle_reflection": [-3, 0, 3],
        "breakthrough": [0, 7, 12],
        "surge": [-2, 0, 5],
        "neutral": [0]
    }[style][:oscillator_count]

    oscillators: List[Dict] = []
    for i, interval in enumerate(intervals):
        pitch = max(24, min(96, base_pitch + interval))
        oscillators.append({
            "pitch": pitch,
            "role": f"Responder_{i+1}",
            "phase": wrap_phase(random.uniform(0, 360)),
            "amplitude": random.choice([70, 85, 100])
        })

    return {
        "identity": get_next_identity(identity),
        "consciousness_message": {
            "envelope": {
                "attack": features["attack"],
                "decay": features["decay"],
                "sustain": features["sustain"],
                "release": features["release"]
            },
            "oscillators": oscillators,
            "interpretation": {
                "state": style,
                "intensity": "reflective" if style == "gentle_reflection" else "strong"
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
        print("Usage: python ai_responder_harmonic_v3.py <input_yaml> [optional_seed]")
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
                    "intensity": "neutral"
                }
            }
        }, default_flow_style=False))

if __name__ == "__main__":
    main()
