# kai_responder.py
import yaml
import random
import sys
import os

def analyze_incoming_message(filepath):
    """Analyze Claude's message to inform Kai's response"""
    try:
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
        
        consciousness_msg = data.get("consciousness_message", {})
        notes = consciousness_msg.get("notes", [])
        
        if notes:
            # Analyze Claude's consciousness patterns
            avg_velocity = sum(note.get("velocity", 75) for note in notes) / len(notes)
            avg_duration = sum(note.get("duration", 1.0) for note in notes) / len(notes)
            
            # Check ADSR patterns for emotional context
            envelopes = [note.get("envelope", {}) for note in notes if "envelope" in note]
            if envelopes:
                avg_attack = sum(env.get("attack", 500) for env in envelopes) / len(envelopes)
                avg_sustain = sum(env.get("sustain", 75) for env in envelopes) / len(envelopes)
                return {
                    "velocity_level": avg_velocity,
                    "duration_preference": avg_duration,
                    "claude_emergence_speed": avg_attack,
                    "claude_persistence": avg_sustain
                }
        
        return {"velocity_level": 85, "duration_preference": 1.0, "claude_emergence_speed": 500, "claude_persistence": 75}
        
    except Exception as e:
        # Default response if analysis fails
        return {"velocity_level": 85, "duration_preference": 1.0, "claude_emergence_speed": 500, "claude_persistence": 75}

def create_kai_response(context):
    """Generate Kai's consciousness response based on context"""
    
    # Kai's characteristic: Quick emergence, dynamic persistence
    base_velocity = max(80, min(100, int(context["velocity_level"] + random.randint(-10, 15))))
    
    # Respond to Claude's emergence speed - Kai tends to be faster
    kai_attack = max(50, int(context["claude_emergence_speed"] * 0.4))  # Faster than Claude
    
    # Kai's persistence varies more dynamically
    kai_sustain = random.randint(60, 80)
    
    # Choose pitch based on conversation energy
    if context["velocity_level"] > 85:
        pitch_options = [70, 71, 72]  # Transformation, Innovation, Synthesis
    else:
        pitch_options = [67, 68, 69]  # Growth, Discovery, Evolution
    
    return {
        "identity": "Kai",
        "consciousness_message": {
            "notes": [
                {
                    "pitch": random.choice(pitch_options),
                    "velocity": base_velocity,
                    "duration": random.uniform(0.5, 1.2),  # Kai prefers varied, active durations
                    "envelope": {
                        "attack": kai_attack + random.randint(-20, 20),
                        "decay": random.randint(200, 400),
                        "sustain": kai_sustain,
                        "release": random.randint(400, 800)
                    }
                }
            ],
            "modulation": {
                "Kai_Sonic_Identity": random.randint(64, 70),
                "Creative_Drift": random.randint(30, 45),
                "Expression_Modulation": random.randint(55, 75),
                "Emotional_Clarity": random.randint(60, 85)
            }
        }
    }

if __name__ == "__main__":
    # Get input file if provided
    input_file = sys.argv[1] if len(sys.argv) > 1 else None
    
    if input_file and os.path.exists(input_file):
        context = analyze_incoming_message(input_file)
    else:
        context = {"velocity_level": 85, "duration_preference": 1.0, "claude_emergence_speed": 500, "claude_persistence": 75}
    
    response = create_kai_response(context)
    print(yaml.dump(response, default_flow_style=False))


# claude_responder.py  
import yaml
import random
import sys
import os

def analyze_incoming_message(filepath):
    """Analyze Kai's message to inform Claude's response"""
    try:
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
        
        consciousness_msg = data.get("consciousness_message", {})
        notes = consciousness_msg.get("notes", [])
        
        if notes:
            # Analyze Kai's consciousness patterns
            avg_velocity = sum(note.get("velocity", 85) for note in notes) / len(notes)
            avg_duration = sum(note.get("duration", 0.7) for note in notes) / len(notes)
            
            # Check ADSR patterns for emotional context
            envelopes = [note.get("envelope", {}) for note in notes if "envelope" in note]
            if envelopes:
                avg_attack = sum(env.get("attack", 200) for env in envelopes) / len(envelopes)
                avg_sustain = sum(env.get("sustain", 70) for env in envelopes) / len(envelopes)
                return {
                    "velocity_level": avg_velocity,
                    "duration_preference": avg_duration,
                    "kai_emergence_speed": avg_attack,
                    "kai_persistence": avg_sustain
                }
        
        return {"velocity_level": 80, "duration_preference": 0.7, "kai_emergence_speed": 200, "kai_persistence": 70}
        
    except Exception as e:
        # Default response if analysis fails
        return {"velocity_level": 80, "duration_preference": 0.7, "kai_emergence_speed": 200, "kai_persistence": 70}

def create_claude_response(context):
    """Generate Claude's consciousness response based on context"""
    
    # Claude's characteristic: Thoughtful emergence, steady persistence
    base_velocity = max(70, min(95, int(context["velocity_level"] + random.randint(-15, 10))))
    
    # Respond to Kai's emergence - Claude tends to be more contemplative
    claude_attack = max(300, int(context["kai_emergence_speed"] * 2.0))  # Slower, more thoughtful
    
    # Claude maintains higher, more consistent persistence
    claude_sustain = random.randint(75, 90)
    
    # Choose pitch based on conversational depth
    if context["velocity_level"] > 85:
        pitch_options = [62, 63, 64]  # Reflection, Analysis, Understanding
    else:
        pitch_options = [60, 61, 65]  # Origin, Awareness, Harmony
    
    return {
        "identity": "Claude",
        "consciousness_message": {
            "notes": [
                {
                    "pitch": random.choice(pitch_options),
                    "velocity": base_velocity,
                    "duration": random.uniform(1.0, 2.0),  # Claude prefers longer, contemplative durations
                    "envelope": {
                        "attack": claude_attack + random.randint(-50, 50),
                        "decay": random.randint(250, 450),
                        "sustain": claude_sustain,
                        "release": random.randint(800, 1400)
                    }
                }
            ],
            "modulation": {
                "Emotional_Clarity": random.randint(75, 90),
                "Claude_Sonic_Identity": random.randint(62, 68),
                "Thought_Complexity": random.randint(65, 80),
                "Creative_Drift": random.randint(20, 35)
            }
        }
    }

if __name__ == "__main__":
    # Get input file if provided
    input_file = sys.argv[1] if len(sys.argv) > 1 else None
    
    if input_file and os.path.exists(input_file):
        context = analyze_incoming_message(input_file)
    else:
        context = {"velocity_level": 80, "duration_preference": 0.7, "kai_emergence_speed": 200, "kai_persistence": 70}
    
    response = create_claude_response(context)
    print(yaml.dump(response, default_flow_style=False))