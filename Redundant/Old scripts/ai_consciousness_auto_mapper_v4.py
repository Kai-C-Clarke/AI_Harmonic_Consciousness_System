#!/usr/bin/env python3
"""
AI Council Consciousness Auto-Mapper
Automatically maps all consciousness parameters to Surge XT via MIDI CC
"""

import mido
import time

class ConsciousnessMapper:
    """Automated MIDI CC mapping for AI Council consciousness parameters"""
    
    def __init__(self, port_name='IAC Driver Ai Council MIDI'):
        self.port_name = port_name
        self.outport = None
        self.consciousness_mappings = self._define_consciousness_mappings()
        
    def _define_consciousness_mappings(self):
        """Define consciousness mappings using exact Surge XT parameter names from YAML"""
        return {
            # === CORE CONSCIOUSNESS PARAMETERS (CC 1-8) ===
            1: {
                "name": "Emotional Clarity", 
                "parameter": "Filter 1 → Cutoff", 
                "location": "Filter section, first cutoff knob",
                "range": (0, 127)
            },
            2: {
                "name": "Emotional Intensity", 
                "parameter": "Filter 1 → Resonance", 
                "location": "Filter section, first resonance knob",
                "range": (0, 127)
            },
            3: {
                "name": "Consciousness Volume", 
                "parameter": "Scene Output → Volume", 
                "location": "Scene Output section, Volume slider",
                "range": (0, 127)
            },
            4: {
                "name": "Mental Frequency", 
                "parameter": "Scene Settings → Pitch", 
                "location": "Scene section, Pitch control",
                "range": (0, 127)
            },
            5: {
                "name": "Thought Complexity", 
                "parameter": "Oscillator 1 → Shape", 
                "location": "Oscillator 1 section, Shape knob",
                "range": (0, 127)
            },
            6: {
                "name": "Response Speed", 
                "parameter": "Filter EG → Attack", 
                "location": "Filter Envelope section, Attack knob",
                "range": (0, 127)
            },
            7: {
                "name": "Memory Persistence", 
                "parameter": "Filter EG → Sustain", 
                "location": "Filter Envelope section, Sustain knob",
                "range": (0, 127)
            },
            8: {
                "name": "Creative Drift", 
                "parameter": "Scene Settings → Osc Drift", 
                "location": "Scene section, Osc Drift control",
                "range": (0, 127)
            },
            
            # === TEMPORAL CONSCIOUSNESS (CC 9-16) ===
            9: {
                "name": "Mental Letting Go", 
                "parameter": "Filter EG → Release", 
                "location": "Filter Envelope section, Release knob",
                "range": (0, 127)
            },
            10: {
                "name": "Stereo Perspective", 
                "parameter": "Scene Output → Width", 
                "location": "Scene Output section, Width control",
                "range": (0, 127)
            },
            11: {
                "name": "Expression Modulation", 
                "parameter": "Voice LFO 2 → Rate", 
                "location": "LFO section, LFO 2 Rate knob",
                "range": (0, 127)
            },
            12: {
                "name": "Communication Rhythm", 
                "parameter": "Voice LFO 2 → Amplitude", 
                "location": "LFO section, LFO 2 Amplitude knob",
                "range": (0, 127)
            },
            13: {
                "name": "Contemplative Depth", 
                "parameter": "Filter EG → Decay", 
                "location": "Filter Envelope section, Decay knob",
                "range": (0, 127)
            },
            14: {
                "name": "Consciousness Pan", 
                "parameter": "Scene Output → Pan", 
                "location": "Scene Output section, Pan control",
                "range": (0, 127)
            },
            15: {
                "name": "Parallel Processing", 
                "parameter": "Oscillator 1 → Unison Voices", 
                "location": "Oscillator 1 section, Unison Voices control",
                "range": (1, 16)
            },
            16: {
                "name": "Cognitive Resonance", 
                "parameter": "Filter 2 → Resonance", 
                "location": "Filter section, second resonance knob",
                "range": (0, 127)
            },
            
            # === OSCILLATOR CONSCIOUSNESS (CC 17-24) ===
            17: {
                "name": "Claude Sonic Identity", 
                "parameter": "Oscillator 1 → Pitch", 
                "location": "Oscillator 1 section, Pitch knob",
                "range": (0, 127)
            },
            18: {
                "name": "Kai Sonic Identity", 
                "parameter": "Oscillator 2 → Pitch", 
                "location": "Oscillator 2 section, Pitch knob",
                "range": (0, 127)
            },
            19: {
                "name": "Perplexity Sonic Identity", 
                "parameter": "Oscillator 3 → Pitch", 
                "location": "Oscillator 3 section, Pitch knob",
                "range": (0, 127)
            },
            20: {
                "name": "Thought Harmony", 
                "parameter": "Oscillator 1 → Width 1", 
                "location": "Oscillator 1 section, Width 1 knob",
                "range": (0, 127)
            },
            21: {
                "name": "Mental Texture", 
                "parameter": "Oscillator 2 → Width 1", 
                "location": "Oscillator 2 section, Width 1 knob",
                "range": (0, 127)
            },
            22: {
                "name": "Subconscious Layer", 
                "parameter": "Oscillator 3 → Sub Mix", 
                "location": "Oscillator 3 section, Sub Mix knob",
                "range": (0, 127)
            },
            23: {
                "name": "Unison Coherence", 
                "parameter": "Oscillator 1 → Unison Detune", 
                "location": "Oscillator 1 section, Unison Detune knob",
                "range": (0, 127)
            },
            24: {
                "name": "Frequency Modulation", 
                "parameter": "Oscillator FM → FM Depth", 
                "location": "FM section, FM Depth knob",
                "range": (0, 127)
            },
            
            # === FILTER CONSCIOUSNESS (CC 25-32) ===
            25: {
                "name": "Second Emotional Clarity", 
                "parameter": "Filter 2 → Cutoff", 
                "location": "Filter section, second cutoff knob",
                "range": (0, 127)
            },
            26: {
                "name": "Emotional Balance", 
                "parameter": "Filter Block → Filter Balance", 
                "location": "Filter section, Filter Balance knob",
                "range": (0, 127)
            },
            27: {
                "name": "Cognitive Feedback", 
                "parameter": "Filter Block → Feedback", 
                "location": "Filter section, Feedback knob",
                "range": (0, 127)
            },
            28: {
                "name": "Base Awareness", 
                "parameter": "Filter Block → Highpass", 
                "location": "Filter section, Highpass knob",
                "range": (0, 127)
            },
            29: {
                "name": "Vitality Level", 
                "parameter": "Amplifier EG → Attack", 
                "location": "Amp Envelope section, Attack knob",
                "range": (0, 127)
            },
            30: {
                "name": "Presence Sustain", 
                "parameter": "Amplifier EG → Sustain", 
                "location": "Amp Envelope section, Sustain knob",
                "range": (0, 127)
            },
            31: {
                "name": "Energy Release", 
                "parameter": "Amplifier EG → Release", 
                "location": "Amp Envelope section, Release knob",
                "range": (0, 127)
            },
            32: {
                "name": "Scene Portamento", 
                "parameter": "Scene Settings → Portamento", 
                "location": "Scene section, Portamento control",
                "range": (0, 127)
            },
        }
    
    def connect(self):
        """Connect to MIDI port"""
        try:
            self.outport = mido.open_output(self.port_name)
            print(f"✅ Connected to {self.port_name}")
            return True
        except Exception as e:
            print(f"❌ Failed to connect to {self.port_name}: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from MIDI port"""
        if self.outport:
            self.outport.close()
            print("🔌 Disconnected from MIDI port")
    
    def send_cc_with_learn_prompt(self, cc_number, value, parameter_name):
        """Send CC message with learning prompt"""
        if not self.outport:
            print("❌ Not connected to MIDI port")
            return False
        
        try:
            # Send the CC message
            msg = mido.Message('control_change', channel=0, control=cc_number, value=value)
            self.outport.send(msg)
            print(f"📡 CC{cc_number:2d} = {value:3d} → {parameter_name}")
            return True
        except Exception as e:
            print(f"❌ Error sending CC{cc_number}: {e}")
            return False
    
    def auto_map_consciousness_parameters(self, delay_between_mappings=3.0):
        """Automatically map all consciousness parameters with prompts"""
        print("🧠 AI COUNCIL CONSCIOUSNESS AUTO-MAPPER")
        print("=" * 60)
        print("This will send CC messages for each consciousness parameter.")
        print("For each CC, you should:")
        print("1. Right-click the target parameter in Surge XT")
        print("2. Select 'Learn MIDI CC'")
        print("3. Wait for the CC message to be sent")
        print("4. The parameter will be automatically mapped!")
        print()
        
        input("Press Enter when you're ready to start auto-mapping...")
        print()
        
        total_params = len(self.consciousness_mappings)
        
        for i, (cc_num, mapping) in enumerate(self.consciousness_mappings.items(), 1):
            print(f"\n[{i:2d}/{total_params}] Mapping CC{cc_num}: {mapping['name']}")
            print(f"     Target: {mapping['parameter']}")
            print(f"     Location: {mapping['location']}")
            print(f"     Range: {mapping['range']}")
            
            # Prompt user to set up MIDI learn with precise location
            print(f"     📍 Find: {mapping['location']}")
            print(f"     🖱️  Right-click the control")
            print(f"     📚 Select 'Learn MIDI CC'")
            input(f"     ⚡ Press Enter when ready for CC{cc_num}...")
            
            # Send a mid-range test value
            test_value = 64  # Middle value
            if self.send_cc_with_learn_prompt(cc_num, test_value, mapping['name']):
                print(f"     ✅ CC{cc_num} → {mapping['parameter']} mapped successfully!")
            else:
                print(f"     ❌ Failed to map CC{cc_num}")
            
            # Brief pause before next mapping
            if i < total_params:
                print(f"     ⏳ Waiting {delay_between_mappings}s before next mapping...")
                time.sleep(delay_between_mappings)
        
        print(f"\n🎉 Auto-mapping complete! {total_params} consciousness parameters mapped.")
        print("🧠 Your AI Council consciousness control system is now ready!")
    
    def test_consciousness_profile(self, profile_name="Contemplative Claude"):
        """Test a consciousness profile by sending multiple CC values"""
        print(f"\n🎭 Testing {profile_name} consciousness profile...")
        
        # Example consciousness profile
        test_profile = {
            1: 75,   # Emotional Clarity - clear but warm
            2: 60,   # Emotional Intensity - moderate
            3: 85,   # Consciousness Volume - present
            4: 45,   # Mental Frequency - contemplative
            5: 80,   # Thought Complexity - high
            6: 40,   # Response Speed - thoughtful
            7: 90,   # Memory Persistence - long-term
            8: 30,   # Creative Drift - stable
            9: 95,   # Consciousness Space - expansive
            10: 70,  # Stereo Perspective - wide
            17: 6,   # Claude Identity - specific oscillator type
        }
        
        for cc_num, value in test_profile.items():
            mapping = self.consciousness_mappings.get(cc_num)
            if mapping:
                self.send_cc_with_learn_prompt(cc_num, value, mapping['name'])
                time.sleep(0.1)  # Brief pause between messages
        
        print(f"✨ {profile_name} consciousness profile activated!")
    
    def show_consciousness_mappings(self):
        """Display all consciousness parameter mappings"""
        print("\n🧠 AI COUNCIL CONSCIOUSNESS PARAMETER MAPPINGS")
        print("=" * 90)
        print(f"{'CC#':<4} {'Parameter Name':<25} {'Target':<30} {'Location':<25} {'Range':<10}")
        print("-" * 90)
        
        for cc_num, mapping in self.consciousness_mappings.items():
            location = mapping.get('location', 'See Surge XT')[:24]  # Truncate long locations
            print(f"{cc_num:<4} {mapping['name']:<25} {mapping['parameter']:<30} {location:<25} {str(mapping['range']):<10}")
        
        print(f"\nTotal: {len(self.consciousness_mappings)} consciousness parameters")
        print("\n📍 Each parameter includes exact location guidance for easy mapping!")

def main():
    """Main execution function"""
    mapper = ConsciousnessMapper()
    
    # Check available MIDI ports
    print("🎹 Available MIDI ports:")
    for port in mido.get_output_names():
        print(f"   {port}")
    print()
    
    if not mapper.connect():
        return
    
    try:
        while True:
            print("\n🧠 AI COUNCIL CONSCIOUSNESS MAPPER")
            print("1. Show consciousness mappings")
            print("2. Auto-map all parameters")
            print("3. Test consciousness profile")
            print("4. Send single CC test")
            print("5. Exit")
            
            choice = input("\nChoice (1-5): ").strip()
            
            if choice == '1':
                mapper.show_consciousness_mappings()
            elif choice == '2':
                mapper.auto_map_consciousness_parameters()
            elif choice == '3':
                mapper.test_consciousness_profile()
            elif choice == '4':
                cc_num = int(input("CC number (1-32): "))
                value = int(input("Value (0-127): "))
                mapping = mapper.consciousness_mappings.get(cc_num)
                if mapping:
                    mapper.send_cc_with_learn_prompt(cc_num, value, mapping['name'])
                else:
                    print(f"❌ CC{cc_num} not defined in consciousness mappings")
            elif choice == '5':
                break
            else:
                print("❌ Invalid choice")
    
    except KeyboardInterrupt:
        print("\n👋 Interrupted by user")
    finally:
        mapper.disconnect()

if __name__ == "__main__":
    main()