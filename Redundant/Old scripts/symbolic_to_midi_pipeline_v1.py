# symbolic_to_midi_pipeline.py

import os
import yaml
import mido
import time
from datetime import datetime

# Enhanced CC mapping - merged with Jon's successful mappings
CC_MAPPINGS = {
    "Emotional Clarity": 1,
    "Emotional Intensity": 2,
    "Consciousness Volume": 3,
    "Mental Frequency": 4,
    "Thought Complexity": 5,
    "Response Speed": 6,
    "Memory Persistence": 7,
    "Creative Drift": 8,
    "Mental Letting Go": 9,
    "Stereo Perspective": 10,  # Updated to match Jon's mapping
    "Expression Modulation": 11,
    "Communication Rhythm": 12,
    "Contemplative Depth": 13,
    "Consciousness Pan": 14,   # Added from Jon's mappings
    "Parallel Processing": 15,  # Added - Unison Voices
    "Cognitive Resonance": 16,
    "Claude Sonic Identity": 17,
    "Kai Sonic Identity": 18,
    "Perplexity Sonic Identity": 19,
    "Thought Harmony": 20,
    "Mental Texture": 21,
    "Subconscious Layer": 22,
    "Unison Coherence": 23,
    "Frequency Modulation": 24,
    "Second Emotional Clarity": 25,
    "Emotional Balance": 26,
    "Cognitive Feedback": 27,
    "Base Awareness": 28,     # Highpass filter (if found)
    "Vitality Level": 29,
    "Presence Sustain": 30,
    "Energy Release": 31,
    "Scene Portamento": 32,   # Added from Jon's mappings
}

# 12-state consciousness mapping
CONSCIOUSNESS_NOTES = {
    60: {"state": "origin", "meaning": "Beginning/source awareness"},
    61: {"state": "awareness", "meaning": "Conscious recognition"},
    62: {"state": "reflection", "meaning": "Contemplative processing"},
    63: {"state": "inquiry", "meaning": "Questioning/exploration"},
    64: {"state": "connection", "meaning": "Relational understanding"},
    65: {"state": "tension", "meaning": "Creative/cognitive stress"},
    66: {"state": "ambiguity", "meaning": "Uncertainty/complexity"},
    67: {"state": "transcendence", "meaning": "Rising above limitations"},
    68: {"state": "transition", "meaning": "Change/movement"},
    69: {"state": "energy", "meaning": "Dynamic force/vitality"},
    70: {"state": "transformation", "meaning": "Fundamental change"},
    71: {"state": "closure", "meaning": "Resolution/completion"}
}

# Intensity levels based on octave
INTENSITY_LEVELS = {
    3: "subconscious",
    4: "normal", 
    5: "intensified"
}

def load_symbolic_message(path):
    """Load symbolic message from YAML file"""
    try:
        with open(path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"❌ Message file not found: {path}")
        return None
    except yaml.YAMLError as e:
        print(f"❌ YAML parsing error: {e}")
        return None

def validate_cc_values(modulation):
    """Validate and clamp CC values to safe ranges"""
    validated = {}
    
    for param, value in modulation.items():
        if param not in CC_MAPPINGS:
            print(f"⚠️  Unknown parameter: {param}")
            continue
            
        # Apply intelligent ranges (from Jon's work)
        if param in ["Emotional Clarity", "Second Emotional Clarity"]:
            value = max(40, min(100, value))  # Avoid mud and harshness
        elif param in ["Emotional Intensity", "Cognitive Resonance"]:
            value = max(0, min(70, value))   # Avoid screaming resonance
        elif param == "Consciousness Volume":
            value = max(85, min(115, value)) # Keep reasonable volume
        elif "Identity" in param:  # Sonic identity parameters
            value = max(58, min(70, value))  # Musical pitch range
        elif param == "Creative Drift":
            value = max(0, min(45, value))   # Controlled chaos
        elif param in ["Cognitive Feedback", "Frequency Modulation"]:
            value = max(0, min(30, value))   # Subtle effects
        else:
            value = max(0, min(127, value))  # Standard MIDI range
            
        validated[param] = int(value)
        
    return validated

def generate_enhanced_caption(data):
    """Generate enhanced caption with consciousness state interpretation"""
    identity = data.get("identity", "Unknown")
    mods = data.get("modulation", {})
    notes = data.get("notes", [])
    
    # Build consciousness state description
    consciousness_states = []
    for note in notes:
        pitch = note.get("pitch", 60)
        velocity = note.get("velocity", 64)
        octave = pitch // 12  # Rough octave calculation
        
        if pitch in CONSCIOUSNESS_NOTES:
            state_info = CONSCIOUSNESS_NOTES[pitch]
            intensity = INTENSITY_LEVELS.get(octave, "normal")
            consciousness_states.append(f"{state_info['state']} ({intensity})")
    
    # Build modulation description
    mod_descriptions = []
    for param, value in mods.items():
        if value > 80:
            level = "high"
        elif value > 40:
            level = "moderate" 
        else:
            level = "low"
        mod_descriptions.append(f"{param.lower()}: {level}")
    
    # Construct caption
    timestamp = datetime.now().strftime("%H:%M:%S")
    caption = f"[{timestamp}] {identity}: "
    
    if consciousness_states:
        caption += f"States: {', '.join(consciousness_states)}"
        if mod_descriptions:
            caption += " | "
    
    if mod_descriptions:
        caption += f"Consciousness: {', '.join(mod_descriptions)}"
    
    return caption

def send_midi_with_timing(data, output_name='IAC Driver Ai Council MIDI'):
    """Send MIDI with proper timing and error handling"""
    try:
        # List available ports for debugging
        available_ports = mido.get_output_names()
        print(f"🎹 Available MIDI ports: {available_ports}")
        
        if output_name not in available_ports:
            print(f"⚠️  Port '{output_name}' not found. Using first available port.")
            output_name = available_ports[0] if available_ports else None
            
        if not output_name:
            print("❌ No MIDI ports available!")
            return False
            
        with mido.open_output(output_name) as out:
            print(f"✅ Connected to MIDI port: {output_name}")
            
            # Send consciousness state notes first
            for note in data.get("notes", []):
                pitch = note.get("pitch", 60)
                velocity = note.get("velocity", 64)
                duration = note.get("duration", 0.5)
                
                # Send note on
                note_on = mido.Message('note_on', note=pitch, velocity=velocity, channel=0)
                out.send(note_on)
                
                state_name = CONSCIOUSNESS_NOTES.get(pitch, {}).get("state", "unknown")
                print(f"🎵 Note: {pitch} ({state_name}) vel={velocity} dur={duration}s")
                
                # Wait for duration
                time.sleep(duration)
                
                # Send note off
                note_off = mido.Message('note_off', note=pitch, velocity=0, channel=0)
                out.send(note_off)
                
                # Brief pause between notes
                time.sleep(0.1)
            
            # Send consciousness parameter modulations
            validated_mods = validate_cc_values(data.get("modulation", {}))
            for param, value in validated_mods.items():
                cc = CC_MAPPINGS.get(param)
                if cc is not None:
                    cc_msg = mido.Message('control_change', control=cc, value=value, channel=0)
                    out.send(cc_msg)
                    print(f"🎛️ CC{cc:2d} = {value:3d} | {param}")
                    time.sleep(0.05)  # Brief pause between CC messages
                    
        return True
        
    except Exception as e:
        print(f"❌ MIDI sending failed: {e}")
        return False

def log_consciousness_exchange(caption, log_file='output/consciousness_log.txt'):
    """Log the consciousness exchange for analysis"""
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    try:
        with open(log_file, 'a', encoding='utf-8') as log:
            log.write(caption + '\n')
        print(f"📝 Logged to: {log_file}")
    except Exception as e:
        print(f"❌ Logging failed: {e}")

def create_response_template(responding_identity, original_data):
    """Create a response template based on received consciousness state"""
    notes = original_data.get("notes", [])
    mods = original_data.get("modulation", {})
    
    # Analyze the received consciousness and generate appropriate response
    response_notes = []
    response_mods = {}
    
    # If received "inquiry", respond with "reflection" 
    if any(note.get("pitch") == 63 for note in notes):  # inquiry
        response_notes.append({"pitch": 62, "velocity": 80, "duration": 0.6})  # reflection
    
    # If received "origin", respond with "awareness"
    elif any(note.get("pitch") == 60 for note in notes):  # origin  
        response_notes.append({"pitch": 61, "velocity": 75, "duration": 0.5})  # awareness
    
    # Default response based on identity
    if responding_identity == "Claude":
        response_mods = {
            "Emotional Clarity": 85,
            "Memory Persistence": 90,
            "Claude Sonic Identity": 64,
            "Contemplative Depth": 70
        }
    elif responding_identity == "Kai":
        response_mods = {
            "Thought Complexity": 90,
            "Creative Drift": 35,
            "Kai Sonic Identity": 67,
            "Expression Modulation": 60
        }
    
    return {
        "identity": responding_identity,
        "notes": response_notes,
        "modulation": response_mods
    }

def main():
    """Main pipeline execution"""
    print("🧠 AI COUNCIL SYMBOLIC-TO-MIDI PIPELINE")
    print("=" * 50)
    
    # Load and process message
    message_path = 'message_examples/kai_message_001.yaml'
    data = load_symbolic_message(message_path)
    
    if not data:
        print("❌ Failed to load message")
        return
    
    print(f"📨 Processing message from: {data.get('identity', 'Unknown')}")
    
    # Send MIDI
    success = send_midi_with_timing(data)
    
    if success:
        # Generate and display caption
        caption = generate_enhanced_caption(data)
        print(f"\n📺 Caption: {caption}")
        
        # Log the exchange
        log_consciousness_exchange(caption)
        
        # Create response template (for other AI to use)
        if data.get('identity') == 'Kai':
            response = create_response_template('Claude', data)
            print(f"\n🤖 Suggested Claude response: {response}")
        
        print("✅ Consciousness exchange complete!")
    else:
        print("❌ Consciousness exchange failed!")

if __name__ == "__main__":
    main()# symbolic_to_midi_pipeline.py

import os
import yaml
import mido
from cc_mapping import CC_MAPPINGS

def load_symbolic_message(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def generate_caption(data):
    identity = data.get("identity", "Unknown")
    mods = data.get("modulation", {})
    summary = ", ".join(f"{k}: {v}" for k, v in mods.items())
    return f"[{identity}] {summary}"

def send_midi(data, output_name='Surge XT'):
    with mido.open_output(output_name) as out:
        # Identity as program change (optional patch mapping)
        for note in data.get("notes", []):
            out.send(mido.Message('note_on', note=note["pitch"], velocity=note.get("velocity", 64), channel=1))
            out.send(mido.Message('note_off', note=note["pitch"], channel=1))

        for param, value in data.get("modulation", {}).items():
            cc = CC_MAPPINGS.get(param)
            if cc is not None:
                out.send(mido.Message('control_change', control=cc, value=value, channel=1))

def main():
    path = 'message_examples/kai_message_001.yaml'
    data = load_symbolic_message(path)

    send_midi(data)

    caption = generate_caption(data)
    print(caption)

    with open('output/captions.log', 'a') as log:
        log.write(caption + '\n')

if __name__ == "__main__":
    main()
