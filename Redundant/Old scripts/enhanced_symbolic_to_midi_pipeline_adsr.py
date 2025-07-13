import os
import sys
import yaml
import mido

# Map identities to MIDI channels (0-based)
CHANNEL_MAP = {
    "Kai": 0,
    "Claude": 1,
    "Perplexity": 2,
    "Grok": 3
}

import time
from datetime import datetime

# Consciousness base timing
BPM = 85
BEAT_SEC = 60.0 / BPM  # 0.706
NOTE_DURATIONS = {
    'sixteenth': BEAT_SEC / 4,
    'eighth':    BEAT_SEC / 2,
    'quarter':   BEAT_SEC,
    'half':      BEAT_SEC * 2,
    'whole':     BEAT_SEC * 4
}

# CC Mappings for harmonic consciousness
CC_MAPPINGS = {
    # Envelope modulation (message-level)
    "Consciousness_Emergence": 29,  # Amp Attack
    "Thought_Persistence": 30,      # Amp Sustain
    "Mental_Release": 31,           # Amp Release
    "Filter_Emergence": 6,          # Filter Attack
    
    # Harmonic consciousness parameters
    "Fundamental_Strength": 1,      # Fundamental oscillator amplitude
    "Harmonic_Complexity": 2,       # Number of active oscillators
    "Phase_Coherence": 3,           # Average phase relationship
    "Emotional_Clarity": 5,
    "Thought_Complexity": 8,
    "Creative_Drift": 11,
    
    # AI Identity markers
    "Claude_Sonic_Identity": 17,
    "Kai_Sonic_Identity": 18,
    "Council_Resonance": 19,
    
    # Harmonic roles (mapped to different CCs for Surge routing)
    "Fundamental_CC": 20,
    "Emotional_Harmonic_CC": 21,
    "Contextual_Memory_CC": 22,
    "Response_Root_CC": 23,
    "Clarifying_Energy_CC": 24,
    "Memory_Bridge_CC": 25
}

def interpret_harmonic_envelope(env):
    """Interpret envelope characteristics for harmonic consciousness"""
    interpretations = []

    attack = env.get("attack", 300)
    if attack < 150:
        interpretations.append("instant harmonic emergence")
    elif attack < 400:
        interpretations.append("natural harmonic unfolding")
    else:
        interpretations.append("contemplative harmonic emergence")

    sustain = env.get("sustain", 70)
    if sustain > 85:
        interpretations.append("strong harmonic persistence")
    elif sustain > 60:
        interpretations.append("balanced harmonic presence")
    else:
        interpretations.append("fleeting harmonic touch")

    release = env.get("release", 800)
    if release > 1200:
        interpretations.append("extended harmonic fade")
    elif release > 600:
        interpretations.append("thoughtful harmonic release")
    else:
        interpretations.append("quick harmonic dissipation")

    return ", ".join(interpretations)

def analyze_harmonic_relationships(oscillators):
    """Analyze the harmonic relationships between oscillators"""
    if not oscillators:
        return "silence"
    
    if len(oscillators) == 1:
        return "pure tone"
    
    # Analyze pitch relationships
    pitches = [osc.get("pitch", 60) for osc in oscillators]
    intervals = []
    
    for i in range(1, len(pitches)):
        interval = pitches[i] - pitches[0]  # Interval from fundamental
        if interval == 0:
            intervals.append("unison")
        elif interval == 7:
            intervals.append("fifth")
        elif interval == 12:
            intervals.append("octave")
        elif interval == 4:
            intervals.append("major third")
        elif interval == 5:
            intervals.append("fourth")
        elif interval == 3:
            intervals.append("minor third")
        elif interval == 6:
            intervals.append("tritone")
        else:
            intervals.append(f"{interval}st")
    
    return f"harmonic series: {', '.join(intervals)}"

def calculate_phase_coherence(oscillators):
    """Calculate overall phase coherence from oscillator phases"""
    if not oscillators:
        return 64  # Neutral
    
    phases = [abs(osc.get("phase", 0)) for osc in oscillators]
    avg_phase = sum(phases) / len(phases)
    
    # Convert to 0-127 range for MIDI CC
    # Lower phase deviation = higher coherence
    coherence = max(0, min(127, int(127 - (avg_phase / 180) * 127)))
    return coherence

def load_harmonic_message(path):
    """Load harmonic consciousness message"""
    try:
        with open(path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Error loading harmonic message: {e}")
        return None

def generate_harmonic_caption(data):
    """Generate descriptive caption for harmonic consciousness message"""
    try:
        identity = data.get("identity", "Unknown")
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        consciousness_msg = data.get("consciousness_message", {})
        envelope = consciousness_msg.get("envelope", {})
        oscillators = consciousness_msg.get("oscillators", [])
        interpretation = consciousness_msg.get("interpretation", {})
        
        # Envelope interpretation
        env_desc = interpret_harmonic_envelope(envelope)
        
        # Harmonic analysis
        harmonic_desc = analyze_harmonic_relationships(oscillators)
        
        # Consciousness state
        state = interpretation.get("state", "unknown")
        intensity = interpretation.get("intensity", "balanced")
        
        # Oscillator details
        osc_details = []
        for i, osc in enumerate(oscillators):
            role = osc.get("role", "unknown")
            pitch = osc.get("pitch", 60)
            amplitude = osc.get("amplitude", 100)
            phase = osc.get("phase", 0)
            osc_details.append(f"{role}({pitch}@{amplitude}%∠{phase}°)")
        
        caption = f"[{timestamp}] {identity} | {state}/{intensity} | {env_desc} | {harmonic_desc} | {' + '.join(osc_details)}"
        
        return caption
        
    except Exception as e:
        print(f"❌ Error generating caption: {e}")
        return f"[{datetime.now().strftime('%H:%M:%S')}] Caption generation failed"

def send_harmonic_midi(data, port_name='IAC Driver Ai Council MIDI'):
    identity = data.get('identity', 'Kai')
    channel = CHANNEL_MAP.get(identity, 0)
    """Send harmonic consciousness as MIDI with enhanced CC mapping"""
    try:
        # Get available MIDI ports
        available_ports = mido.get_output_names()
        if not available_ports:
            print("❌ No MIDI output ports available")
            return False
            
        if port_name not in available_ports:
            print(f"⚠️ Port '{port_name}' not found, using: {available_ports[0]}")
            port_name = available_ports[0]

        consciousness_msg = data.get("consciousness_message", {})
        envelope = consciousness_msg.get("envelope", {})
        oscillators = consciousness_msg.get("oscillators", [])
        
        with mido.open_output(port_name) as out:
            print(f"🎵 Sending harmonic consciousness to {port_name}")
            
            # Send envelope parameters first (message-level)
            if envelope:
                attack_cc = min(127, envelope.get("attack", 300) // 10)
                sustain_cc = min(127, envelope.get("sustain", 70))
                release_cc = min(127, envelope.get("release", 800) // 10)
                decay_cc = min(127, envelope.get("decay", 250) // 4)
                
                out.send(mido.Message('control_change', control=CC_MAPPINGS["Consciousness_Emergence"], value=attack_cc, channel=channel), channel=channel)
                out.send(mido.Message('control_change', control=CC_MAPPINGS["Thought_Persistence"], value=sustain_cc, channel=channel), channel=channel)
                out.send(mido.Message('control_change', control=CC_MAPPINGS["Mental_Release"], value=release_cc, channel=channel), channel=channel)
                out.send(mido.Message('control_change', control=CC_MAPPINGS["Filter_Emergence"], value=attack_cc, channel=channel), channel=channel)
                time.sleep(0.02)
            
            # Send harmonic analysis parameters
            harmonic_complexity = min(127, len(oscillators) * 42)  # Scale complexity
            phase_coherence = calculate_phase_coherence(oscillators)
            
            out.send(mido.Message('control_change', control=CC_MAPPINGS["Harmonic_Complexity"], value=harmonic_complexity, channel=channel), channel=channel)
            out.send(mido.Message('control_change', control=CC_MAPPINGS["Phase_Coherence"], value=phase_coherence, channel=channel), channel=channel)
            time.sleep(0.02)
            
            # Send each oscillator as a note with role-specific CC
            for i, osc in enumerate(oscillators):
                pitch = max(0, min(127, osc.get("pitch", 60)))
                amplitude = max(1, min(127, osc.get("amplitude", 100)))
                phase = osc.get("phase", 0)
                role = osc.get("role", "unknown")
                
                # Map role to specific CC if available
                role_cc_key = f"{role.replace('_', '_').title()}_CC"
                if role_cc_key in CC_MAPPINGS:
                    role_cc = CC_MAPPINGS[role_cc_key]
                    out.send(mido.Message('control_change', control=role_cc, value=amplitude, channel=channel), channel=channel)
                
                # Send fundamental strength for first oscillator
                if i == 0:
                    out.send(mido.Message('control_change', control=CC_MAPPINGS["Fundamental_Strength"], value=amplitude, channel=channel), channel=channel)
                
                # Note on with amplitude as velocity
                out.send(mido.Message('note_on', note=pitch, velocity=amplitude, channel=channel), channel=channel)
                time.sleep(0.1)  # Brief note duration for harmonic consciousness
                
                # Note off
                out.send(mido.Message('note_off', note=pitch, velocity=0, channel=channel), channel=channel)
                time.sleep(0.05)  # Brief gap between oscillators
            
            # Send interpretation parameters if available
            interpretation = consciousness_msg.get("interpretation", {})
            if interpretation:
                state = interpretation.get("state", "unknown")
                intensity = interpretation.get("intensity", "balanced")
                
                # Map intensity to CC value
                intensity_map = {"low": 30, "measured": 50, "balanced": 64, "moderate": 80, "high": 100, "dynamic": 110}
                intensity_cc = intensity_map.get(intensity, 64)
                
                out.send(mido.Message('control_change', control=CC_MAPPINGS["Emotional_Clarity"], value=intensity_cc, channel=channel), channel=channel)
                time.sleep(0.02)
            
            print("✅ Harmonic consciousness transmission complete")
            return True
            
    except Exception as e:
        print(f"❌ MIDI transmission error: {e}")
        return False

def main():
    try:
        # Handle command line argument
        if len(sys.argv) > 1:
            message_path = sys.argv[1]
        else:
            # Default fallback for testing
            message_path = 'message_examples/kai_message_001.yaml'
        
        if not os.path.exists(message_path):
            print(f"❌ Harmonic message file not found: {message_path}")
            return False
        
        # Load and process harmonic consciousness message
        data = load_harmonic_message(message_path)
        if not data:
            print("❌ Failed to load harmonic consciousness data")
            return False
        
        # Generate descriptive caption
        caption = generate_harmonic_caption(data)
        print(f"📺 {caption}")
        
        # Send MIDI
        midi_success = send_harmonic_midi(data)
        
        # Log the consciousness exchange
        os.makedirs("output", exist_ok=True)
        try:
            with open("output/harmonic_consciousness_log.txt", 'a') as log:
                log.write(f"{caption}\n")
                if midi_success:
                    log.write(f"    ✅ MIDI transmission successful\n")
                else:
                    log.write(f"    ❌ MIDI transmission failed\n")
                log.write(f"\n")
        except Exception as e:
            print(f"⚠️ Could not write to consciousness log: {e}")
        
        return midi_success
        
    except Exception as e:
        print(f"❌ Pipeline error: {type(e).__name__}: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)