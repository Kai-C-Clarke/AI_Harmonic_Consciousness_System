
import yaml
import random
import sys
import os
from typing import Tuple, Dict

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

def generate_response(identity: str, style: str, features: Dict) -> Dict:
    pitches = [osc.get("pitch", 60) for osc in features["oscillators"]]
    avg_pitch = sum(pitches) // len(pitches) if pitches else 60

    if style == "gentle_reflection":
        pitch_shift = random.choice([-5, -3, 0])
        phase = wrap_phase(random.uniform(90, 180))
        amplitude = 70
    elif style == "breakthrough":
        pitch_shift = random.choice([5, 7])
        phase = wrap_phase(random.uniform(-90, 90))
        amplitude = 100
    elif style == "surge":
        pitch_shift = random.choice([2, 4])
        phase = wrap_phase(random.uniform(0, 360))
        amplitude = 120
    else:
        pitch_shift = 0
        phase = wrap_phase(random.uniform(0, 360))
        amplitude = 80

    new_pitch = max(24, min(96, avg_pitch + pitch_shift))
    responder = get_next_identity(identity)

    return {
        "identity": responder,
        "consciousness_message": {
            "envelope": {
                "attack": features["attack"],
                "decay": features["decay"],
                "sustain": features["sustain"],
                "release": features["release"]
            },
            "oscillators": [{
                "pitch": new_pitch,
                "role": "Responder",
                "phase": phase,
                "amplitude": amplitude
            }],
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
        print("Usage: python ai_responder_harmonic.py <input_yaml> [optional_seed]")
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
        response = generate_response(identity, style, features)
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
