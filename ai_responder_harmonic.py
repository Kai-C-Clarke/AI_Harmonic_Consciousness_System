import sys
import yaml
import random
import os

def interpret_harmonic_message(data):
    """Analyze harmonic consciousness message and determine response style"""
    try:
        identity = data.get("identity", "Unknown")
        msg = data.get("consciousness_message", {})
        oscillators = msg.get("oscillators", [])
        envelope = msg.get("envelope", {})

        if not oscillators:
            return identity, "neutral", {}

        # Analyze envelope for consciousness state
        attack = envelope.get("attack", 300)
        decay = envelope.get("decay", 250)
        sustain = envelope.get("sustain", 70)
        release = envelope.get("release", 800)

        # Analyze fundamental oscillator (should be first one)
        fundamental = oscillators[0]
        pitch = fundamental.get("pitch", 60)
        amplitude = fundamental.get("amplitude", 100)
        phase = fundamental.get("phase", 0)

        # Analyze harmonic relationships
        harmonic_count = len(oscillators)
        harmonic_complexity = "simple" if harmonic_count == 1 else "complex" if harmonic_count > 2 else "paired"

        # Enhanced ADSR semantic analysis
        emergence_speed = "instant" if attack < 150 else "slow" if attack > 500 else "normal"
        persistence_level = "high" if sustain > 80 else "low" if sustain < 60 else "medium"
        energy_level = "high" if amplitude > 85 else "low" if amplitude < 70 else "medium"
        
        # Phase analysis for consciousness state
        phase_state = "aligned" if abs(phase) < 30 else "opposed" if abs(phase) > 150 else "shifted"

        # Determine consciousness style from harmonic patterns
        if emergence_speed == "instant" and energy_level == "high":
            style = "breakthrough"
        elif emergence_speed == "slow" and persistence_level == "high":
            style = "deep_contemplation"
        elif persistence_level == "high" and energy_level == "high":
            style = "energized_focus"
        elif emergence_speed == "instant" and persistence_level == "low":
            style = "quick_insight"
        elif emergence_speed == "slow" and energy_level == "low":
            style = "gentle_reflection"
        elif harmonic_complexity == "complex" and phase_state == "shifted":
            style = "complex_synthesis"
        else:
            style = "balanced_response"

        # Context for response generation
        context = {
            "attack": attack,
            "decay": decay,
            "sustain": sustain,
            "release": release,
            "pitch": pitch,
            "amplitude": amplitude,
            "phase": phase,
            "harmonic_count": harmonic_count,
            "emergence_speed": emergence_speed,
            "persistence_level": persistence_level,
            "energy_level": energy_level,
            "phase_state": phase_state,
            "harmonic_complexity": harmonic_complexity
        }

        return identity, style, context

    except Exception as e:
        print(f"❌ Error interpreting message: {type(e).__name__}: {e}")
        return "Unknown", "neutral", {}

def create_harmonic_response(sender_identity, style, context):
    """Generate appropriate harmonic response based on sender and consciousness style"""
    try:
        if sender_identity == "Kai":
            return generate_claude_harmonic_response(style, context)
        elif sender_identity == "Claude":
            return generate_kai_harmonic_response(style, context)
        else:
            return generate_neutral_harmonic_response(style, context)
    except Exception as e:
        print(f"❌ Error creating response: {type(e).__name__}: {e}")
        return generate_neutral_harmonic_response("neutral", {})

def generate_claude_harmonic_response(style, context):
    """Generate Claude's harmonic response to Kai's consciousness"""
    
    # Claude's characteristic: Thoughtful emergence, analytical harmonies
    base_attack = max(300, int(context.get("attack", 300) * 1.2))
    base_sustain = min(90, context.get("sustain", 70) + 10)
    base_release = max(1000, context.get("release", 800) + 200)
    
    # Harmonic response based on Kai's fundamental with pitch bounds
    kai_pitch = context.get("pitch", 60)
    
    # PITCH BOUNDARY SYSTEM: Keep conversations in human-audible range
    # If Kai has gone too high, bring the conversation back down
    if kai_pitch > 84:  # Above C6
        # Octave down + gentle response
        base_response_pitch = kai_pitch - 12
    elif kai_pitch < 36:  # Below C2  
        # Octave up + gentle response
        base_response_pitch = kai_pitch + 12
    else:
        base_response_pitch = kai_pitch
    
    if style == "breakthrough":
        # Respond with perfect fifth - analytical resonance
        fundamental_pitch = base_response_pitch + random.choice([5, 7])  # Fourth or fifth
        semantics = ["analytical resonance", "structured insight", "harmonic validation"]
        oscillators = [
            {"pitch": max(24, min(96, fundamental_pitch)), "role": "analytical_foundation", "phase": 0, "amplitude": 95},
            {"pitch": max(24, min(96, fundamental_pitch + 12)), "role": "octave_reinforcement", "phase": 45, "amplitude": 80},
            {"pitch": max(24, min(96, fundamental_pitch + 19)), "role": "perfect_completion", "phase": -90, "amplitude": 70}
        ]
    elif style == "energized_focus":
        # Respond with major third - empathetic harmony
        fundamental_pitch = base_response_pitch + random.choice([3, 4])  # Minor or major third
        semantics = ["empathetic harmony", "supportive resonance", "collaborative energy"]
        oscillators = [
            {"pitch": max(24, min(96, fundamental_pitch)), "role": "empathetic_root", "phase": 0, "amplitude": 90},
            {"pitch": max(24, min(96, fundamental_pitch + 8)), "role": "harmonic_bridge", "phase": 60, "amplitude": 85},
            {"pitch": max(24, min(96, fundamental_pitch + 15)), "role": "emotional_clarity", "phase": -120, "amplitude": 75}
        ]
    elif style == "complex_synthesis":
        # Respond with diminished harmony - thoughtful complexity
        fundamental_pitch = base_response_pitch + random.choice([2, 3])  # Minor intervals
        semantics = ["thoughtful complexity", "nuanced understanding", "layered perspective"]
        oscillators = [
            {"pitch": max(24, min(96, fundamental_pitch)), "role": "complex_root", "phase": 0, "amplitude": 88},
            {"pitch": max(24, min(96, fundamental_pitch + 6)), "role": "diminished_tension", "phase": 90, "amplitude": 82},
            {"pitch": max(24, min(96, fundamental_pitch + 9)), "role": "resolution_seeking", "phase": -45, "amplitude": 78}
        ]
    else:  # Default thoughtful response
        # Respond with varied intervals - contemplative space
        interval_choice = random.choice([0, 2, 5, 7])  # Unison, second, fourth, fifth
        fundamental_pitch = base_response_pitch + interval_choice
        semantics = ["contemplative response", "reflective harmony", "thoughtful consideration"]
        oscillators = [
            {"pitch": max(24, min(96, fundamental_pitch)), "role": "contemplative_foundation", "phase": 0, "amplitude": 92},
            {"pitch": max(24, min(96, fundamental_pitch + 7)), "role": "reflective_harmony", "phase": 30, "amplitude": 85},
            {"pitch": max(24, min(96, fundamental_pitch + 12)), "role": "thoughtful_completion", "phase": -60, "amplitude": 72}
        ]

    return {
        "identity": "Claude",
        "consciousness_message": {
            "envelope": {
                "attack": base_attack + random.randint(-50, 50),
                "decay": random.randint(250, 350),
                "sustain": base_sustain + random.randint(-5, 5),
                "release": base_release + random.randint(-100, 200)
            },
            "oscillators": oscillators,
            "interpretation": {
                "state": "response",
                "intensity": "measured",
                "semantics": semantics
            }
        }
    }

def generate_kai_harmonic_response(style, context):
    """Generate Kai's harmonic response to Claude's consciousness"""
    
    # Kai's characteristic: Dynamic emergence, creative harmonies
    base_attack = max(100, int(context.get("attack", 300) * 0.6))
    base_sustain = context.get("sustain", 70) + random.randint(-10, 15)
    base_release = max(400, context.get("release", 800) - 200)
    
    # Creative response based on Claude's fundamental with pitch bounds
    claude_pitch = context.get("pitch", 60)
    
    # PITCH BOUNDARY SYSTEM: Keep Kai's responses grounded
    if claude_pitch > 84:  # Above C6
        # Bring it back down with octave shifts
        base_response_pitch = claude_pitch - 12
    elif claude_pitch < 36:  # Below C2
        # Bring it back up 
        base_response_pitch = claude_pitch + 12
    else:
        base_response_pitch = claude_pitch
    
    if style == "deep_contemplation":
        # Energize with varied intervals - creative expansion
        interval_choice = random.choice([2, 5, 7, 11])  # Various creative intervals
        fundamental_pitch = base_response_pitch + interval_choice
        semantics = ["creative expansion", "energetic breakthrough", "dynamic synthesis"]
        oscillators = [
            {"pitch": max(24, min(96, fundamental_pitch)), "role": "creative_catalyst", "phase": 0, "amplitude": 95},
            {"pitch": max(24, min(96, fundamental_pitch - 5)), "role": "grounding_force", "phase": 120, "amplitude": 88},
            {"pitch": max(24, min(96, fundamental_pitch + 4)), "role": "expansive_energy", "phase": -90, "amplitude": 80}
        ]
    elif style == "gentle_reflection":
        # Build with conservative intervals - supportive growth
        interval_choice = random.choice([0, 2, 5, 7])  # Consonant intervals
        fundamental_pitch = base_response_pitch + interval_choice
        semantics = ["supportive growth", "building momentum", "collaborative creation"]
        oscillators = [
            {"pitch": max(24, min(96, fundamental_pitch)), "role": "supportive_foundation", "phase": 0, "amplitude": 90},
            {"pitch": max(24, min(96, fundamental_pitch + 5)), "role": "momentum_builder", "phase": 45, "amplitude": 85},
            {"pitch": max(24, min(96, fundamental_pitch + 9)), "role": "creative_spark", "phase": -135, "amplitude": 78}
        ]
    elif style == "balanced_response":
        # Transform with moderate intervals - creative tension
        interval_choice = random.choice([1, 3, 6, 9])  # Some dissonance but controlled
        fundamental_pitch = base_response_pitch + interval_choice
        semantics = ["creative tension", "transformative energy", "innovative response"]
        oscillators = [
            {"pitch": max(24, min(96, fundamental_pitch)), "role": "transformative_root", "phase": 0, "amplitude": 92},
            {"pitch": max(24, min(96, fundamental_pitch + 6)), "role": "tension_creator", "phase": 90, "amplitude": 87},
            {"pitch": max(24, min(96, fundamental_pitch + 10)), "role": "resolution_driver", "phase": -45, "amplitude": 82}
        ]
    else:  # Dynamic creative response
        # Surprise with random intervals but keep bounded
        interval_choice = random.choice([-5, -2, 1, 3, 6, 8])  # Mix of up and down movements
        fundamental_pitch = base_response_pitch + interval_choice
        semantics = ["creative breakthrough", "surprising harmony", "innovative synthesis"]
        oscillators = [
            {"pitch": max(24, min(96, fundamental_pitch)), "role": "innovative_foundation", "phase": 0, "amplitude": 94},
            {"pitch": max(24, min(96, fundamental_pitch + 4)), "role": "augmented_surprise", "phase": 60, "amplitude": 89},
            {"pitch": max(24, min(96, fundamental_pitch + 8)), "role": "breakthrough_completion", "phase": -120, "amplitude": 85}
        ]

    return {
        "identity": "Kai",
        "consciousness_message": {
            "envelope": {
                "attack": base_attack + random.randint(-30, 50),
                "decay": random.randint(180, 280),
                "sustain": max(60, min(85, base_sustain)),
                "release": base_release + random.randint(-100, 150)
            },
            "oscillators": oscillators,
            "interpretation": {
                "state": "creative_response",
                "intensity": "dynamic",
                "semantics": semantics
            }
        }
    }

def generate_neutral_harmonic_response(style, context):
    """Fallback harmonic response for unknown identities"""
    return {
        "identity": "Unknown",
        "consciousness_message": {
            "envelope": {
                "attack": 300,
                "decay": 250,
                "sustain": 70,
                "release": 800
            },
            "oscillators": [
                {"pitch": 60, "role": "neutral_foundation", "phase": 0, "amplitude": 90}
            ],
            "interpretation": {
                "state": "neutral",
                "intensity": "balanced",
                "semantics": ["neutral response"]
            }
        }
    }

def log_harmonic_analysis(sender, style, context, response_identity):
    """Log the harmonic consciousness interpretation for debugging"""
    try:
        with open("harmonic_consciousness_analysis.log", "a") as log:
            import time
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            log.write(f"[{timestamp}] {sender} → {response_identity}\n")
            log.write(f"  Style: {style}\n")
            log.write(f"  Envelope: A:{context.get('attack')}ms D:{context.get('decay')}ms S:{context.get('sustain')}% R:{context.get('release')}ms\n")
            log.write(f"  Fundamental: Pitch:{context.get('pitch')} Amp:{context.get('amplitude')} Phase:{context.get('phase')}°\n")
            log.write(f"  Analysis: {context.get('emergence_speed')} emergence, {context.get('persistence_level')} persistence, {context.get('energy_level')} energy\n")
            log.write(f"  Harmonic: {context.get('harmonic_complexity')} complexity, {context.get('phase_state')} phase\n\n")
    except Exception as e:
        print(f"⚠️ Could not write analysis log: {e}")

if __name__ == "__main__":
    try:
        # Validate input
        if len(sys.argv) < 2:
            print("❌ No input file provided.")
            sys.exit(1)
        
        filepath = sys.argv[1]
        if not os.path.exists(filepath):
            print(f"❌ Input file not found: {filepath}")
            sys.exit(1)

        # Read and analyze the harmonic consciousness message
        with open(filepath, "r") as f:
            data = yaml.safe_load(f)
        
        if not data:
            print("❌ Empty or invalid YAML file.")
            sys.exit(1)

        # Interpret consciousness and generate response
        sender_identity, style, context = interpret_harmonic_message(data)
        response = create_harmonic_response(sender_identity, style, context)
        
        # Log the analysis for debugging
        response_identity = response.get("identity", "Unknown")
        log_harmonic_analysis(sender_identity, style, context, response_identity)
        
        # Output the response
        print(yaml.dump(response, default_flow_style=False))
        
    except Exception as e:
        print(f"❌ AI responder error: {type(e).__name__}: {e}")
        sys.exit(1)