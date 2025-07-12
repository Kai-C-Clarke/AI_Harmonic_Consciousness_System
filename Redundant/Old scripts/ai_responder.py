import yaml
import random

def create_response():
    return {
        "identity": "Claude",
        "notes": [
            {
                "pitch": 62,  # Reflection
                "velocity": random.randint(75, 90),
                "duration": 1.412,  # Half note (contemplative)
                "envelope": {
                    "attack": 500,
                    "decay": 300,
                    "sustain": 85,
                    "release": 1100
                }
            }
        ],
        "modulation": {
            "Emotional Clarity": 80,
            "Claude Sonic Identity": 64,
            "Thought Complexity": 70
        }
    }

if __name__ == "__main__":
    response = create_response()
    print(yaml.dump(response))
