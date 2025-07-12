#!/usr/bin/env python3
"""
AI Council Consciousness Tester
Test and demonstrate the mapped consciousness parameters in real-time
"""

import mido
import time
import random
import math

class ConsciousnessTester:
    """Test the mapped AI consciousness parameters"""
    
    def __init__(self, port_name='IAC Driver Ai Council MIDI'):
        self.port_name = port_name
        self.outport = None
        
        # Your successfully mapped parameters (from the MIDI mapping)
        self.mapped_controls = {
            1: "Emotional Clarity (Filter 1 Cutoff)",
            2: "Emotional Intensity (Filter 1 Resonance)", 
            3: "Consciousness Volume (Scene Volume)",
            4: "Mental Frequency (Scene Pitch)",
            5: "Thought Complexity (Osc 1 Shape)",
            7: "Memory Persistence (Filter EG Sustain)",
            8: "Creative Drift (Osc Drift)",
            9: "Mental Letting Go (Filter EG Release)",
            11: "Expression Modulation (LFO 1 Rate)",
            12: "Communication Rhythm (LFO 1 Amplitude)",
            13: "Contemplative Depth (LFO 1 Decay)",
            16: "Cognitive Resonance (Filter 2 Resonance)",
            17: "Claude Sonic Identity (Osc 1 Pitch)",
            18: "Kai Sonic Identity (Osc 2 Pitch)",
            19: "Perplexity Sonic Identity (Osc 3 Pitch)",
            20: "Thought Harmony (Osc 1 Width 1)",
            21: "Mental Texture (Osc 2 Width 1)",
            22: "Subconscious Layer (Osc 3 Sub Mix)",
            23: "Unison Coherence (Osc 1 Unison Detune)",
            24: "Frequency Modulation (FM Depth)",
            25: "Second Emotional Clarity (Filter 2 Cutoff)",
            26: "Emotional Balance (Filter Balance)",
            27: "Cognitive Feedback (Feedback)",
            29: "Vitality Level (Amp EG Attack)",
            30: "Presence Sustain (Amp EG Sustain)",
            31: "Energy Release (Amp EG Release)",
        }
    
    def connect(self):
        """Connect to MIDI port"""
        try:
            self.outport = mido.open_output(self.port_name)
            print(f"✅ Connected to {self.port_name}")
            return True
        except Exception as e:
            print(f"❌ Failed to connect: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from MIDI port"""
        if self.outport:
            self.outport.close()
            print("🔌 Disconnected")
    
    def send_cc(self, cc_num, value, description=""):
        """Send a CC message"""
        if not self.outport:
            return False
        
        try:
            msg = mido.Message('control_change', channel=0, control=cc_num, value=value)
            self.outport.send(msg)
            print(f"🎛️ CC{cc_num:2d} = {value:3d} | {description}")
            return True
        except Exception as e:
            print(f"❌ Error sending CC{cc_num}: {e}")
            return False
    
    def send_note(self, note, velocity=64, duration=1.0):
        """Send a MIDI note for testing"""
        if not self.outport:
            return False
        
        try:
            # Note on
            note_on = mido.Message('note_on', channel=0, note=note, velocity=velocity)
            self.outport.send(note_on)
            print(f"🎵 Note {note} ON (vel={velocity})")
            
            time.sleep(duration)
            
            # Note off
            note_off = mido.Message('note_off', channel=0, note=note, velocity=0)
            self.outport.send(note_off)
            print(f"🎵 Note {note} OFF")
            return True
        except Exception as e:
            print(f"❌ Error sending note: {e}")
            return False
    
    def test_parameter_sweep(self, cc_num, description, duration=3.0):
        """Sweep a parameter from 0 to 127 and back"""
        print(f"\n🌊 Testing {description}")
        steps = 20
        
        # Sweep up
        for i in range(steps + 1):
            value = int((i / steps) * 127)
            self.send_cc(cc_num, value, f"{description} ↗")
            time.sleep(duration / (steps * 2))
        
        # Sweep down  
        for i in range(steps, -1, -1):
            value = int((i / steps) * 127)
            self.send_cc(cc_num, value, f"{description} ↘")
            time.sleep(duration / (steps * 2))
    
    def demonstrate_consciousness_profiles(self):
        """Demonstrate different AI consciousness profiles"""
        
        profiles = {
            "Contemplative Claude": {
                1: 75,   # Clear but warm emotional clarity
                2: 35,   # Gentle intensity
                3: 95,   # Present volume
                5: 60,   # Moderate complexity
                7: 85,   # Good memory
                8: 15,   # Stable, low drift
                17: 64,  # Centered pitch
                20: 55,  # Harmonious thoughts
                29: 25,  # Gentle attack
                30: 75,  # Good sustain
            },
            
            "Energetic Kai": {
                1: 85,   # Bright clarity
                2: 50,   # Moderate intensity
                3: 105,  # Higher volume
                5: 80,   # Higher complexity
                7: 70,   # Active memory
                8: 35,   # Creative drift
                18: 67,  # Slightly higher pitch
                21: 70,  # Rich texture
                11: 45,  # Faster modulation
                12: 65,  # Expressive rhythm
            },
            
            "Analytical Perplexity": {
                1: 90,   # Crystal clarity
                2: 25,   # Controlled intensity
                3: 90,   # Measured volume
                5: 75,   # High complexity but controlled
                7: 90,   # Excellent memory
                8: 8,    # Very stable
                19: 61,  # Slightly lower pitch
                16: 20,  # Controlled resonance
                25: 85,  # Clear second filter
                26: 64,  # Balanced
            },
            
            "Gentle Creativity": {
                1: 65,   # Warm clarity
                2: 45,   # Moderate intensity
                3: 100,  # Good volume
                5: 85,   # High complexity
                7: 60,   # Flowing memory
                8: 25,   # Gentle drift
                11: 35,  # Gentle modulation
                12: 50,  # Steady rhythm
                24: 15,  # Subtle FM
                22: 25,  # Some subconscious layer
            }
        }
        
        for profile_name, params in profiles.items():
            print(f"\n🎭 DEMONSTRATING: {profile_name}")
            print("=" * 50)
            
            # Set the consciousness profile
            for cc_num, value in params.items():
                description = self.mapped_controls.get(cc_num, f"CC{cc_num}")
                self.send_cc(cc_num, value, description)
                time.sleep(0.1)
            
            print(f"\n🎵 Playing test notes with {profile_name} consciousness...")
            
            # Play some test notes to hear the consciousness
            test_notes = [60, 64, 67, 72]  # C major chord spread
            for note in test_notes:
                self.send_note(note, velocity=80, duration=1.5)
                time.sleep(0.5)
            
            input(f"\n👂 Listen to {profile_name}'s consciousness... Press Enter for next profile...")
    
    def interactive_consciousness_control(self):
        """Interactive real-time consciousness control"""
        print("\n🎛️ INTERACTIVE CONSCIOUSNESS CONTROL")
        print("Play notes on your MIDI keyboard or use these commands:")
        print("- cc1-31=value : Set consciousness parameter")
        print("- sweep cc# : Sweep a parameter") 
        print("- note 60 : Play test note")
        print("- random : Random consciousness state")
        print("- reset : Reset all parameters to neutral")
        print("- quit : Exit")
        
        while True:
            try:
                cmd = input("\n🧠 Consciousness > ").strip().lower()
                
                if cmd == 'quit':
                    break
                elif cmd == 'random':
                    self.random_consciousness_state()
                elif cmd == 'reset':
                    self.reset_consciousness()
                elif cmd.startswith('sweep '):
                    cc_num = int(cmd.split()[1].replace('cc', ''))
                    if cc_num in self.mapped_controls:
                        self.test_parameter_sweep(cc_num, self.mapped_controls[cc_num])
                elif cmd.startswith('note '):
                    note = int(cmd.split()[1])
                    self.send_note(note, velocity=80, duration=2.0)
                elif '=' in cmd and cmd.startswith('cc'):
                    cc_part, value_part = cmd.split('=')
                    cc_num = int(cc_part.replace('cc', ''))
                    value = int(value_part)
                    if cc_num in self.mapped_controls:
                        self.send_cc(cc_num, value, self.mapped_controls[cc_num])
                else:
                    print("❌ Invalid command")
                    
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def get_smart_range(self, cc_num):
        """Get intelligent value ranges for each consciousness parameter"""
        ranges = {
            # Filters - keep musical
            1: (40, 100),   # Emotional Clarity - avoid mud and harshness
            2: (0, 70),     # Emotional Intensity - avoid screaming resonance
            25: (35, 95),   # Second filter - musical range
            16: (0, 60),    # Cognitive Resonance - controlled
            
            # Volume/Levels - keep reasonable
            3: (85, 115),   # Consciousness Volume - present but not overwhelming
            
            # Pitch - musical intervals
            4: (58, 70),    # Mental Frequency - stay in musical range
            17: (58, 70),   # Claude Identity - musical pitch range
            18: (58, 70),   # Kai Identity - musical pitch range  
            19: (58, 70),   # Perplexity Identity - musical pitch range
            
            # Complexity/Shape - creative but controlled
            5: (30, 90),    # Thought Complexity - avoid extremes
            20: (30, 80),   # Thought Harmony - musical width
            21: (30, 80),   # Mental Texture - musical width
            
            # Time-based - natural feeling
            7: (50, 95),    # Memory Persistence - avoid too short
            9: (20, 80),    # Mental Letting Go - natural release times
            29: (10, 60),   # Vitality Level - natural attack times
            30: (40, 90),   # Presence Sustain - musical sustain
            31: (30, 85),   # Energy Release - natural release
            
            # Creative elements - controlled chaos
            8: (0, 45),     # Creative Drift - organic but not chaotic
            11: (10, 60),   # Expression Modulation - musical LFO rates
            12: (20, 80),   # Communication Rhythm - expressive but controlled
            13: (30, 70),   # Contemplative Depth - moderate decay
            
            # Advanced parameters - subtle effects
            22: (0, 40),    # Subconscious Layer - subtle sub mix
            23: (10, 50),   # Unison Coherence - tight but organic
            24: (0, 30),    # Frequency Modulation - subtle FM
            26: (45, 85),   # Emotional Balance - around center
            27: (0, 25),    # Cognitive Feedback - controlled feedback
        }
        
        return ranges.get(cc_num, (20, 107))  # Default safe range
    
    def random_consciousness_state(self):
        """Generate a musically intelligent random consciousness state"""
        print("🎲 Generating intelligent random consciousness state...")
        
        for cc_num in self.mapped_controls.keys():
            min_val, max_val = self.get_smart_range(cc_num)
            value = random.randint(min_val, max_val)
            
            self.send_cc(cc_num, value, self.mapped_controls[cc_num])
            time.sleep(0.05)
    
    def reset_consciousness(self):
        """Reset all parameters to neutral state"""
        print("🔄 Resetting consciousness to neutral state...")
        
        neutral_values = {
            1: 64,   # Mid clarity
            2: 30,   # Low intensity
            3: 100,  # Good volume
            4: 64,   # Center pitch
            5: 64,   # Mid complexity
            7: 64,   # Mid memory
            8: 20,   # Low drift
            9: 40,   # Quick release
            11: 30,  # Slow LFO
            12: 40,  # Mid amplitude
            17: 64,  # Center pitch
            18: 64,  # Center pitch  
            19: 64,  # Center pitch
            20: 50,  # Mid width
            21: 50,  # Mid width
            22: 20,  # Low sub mix
            24: 0,   # No FM
            25: 64,  # Mid cutoff
            26: 64,  # Balanced
            27: 0,   # No feedback
        }
        
        for cc_num, value in neutral_values.items():
            if cc_num in self.mapped_controls:
                self.send_cc(cc_num, value, self.mapped_controls[cc_num])
                time.sleep(0.05)

def main():
    """Main test function"""
    print("🧠🎵 AI COUNCIL CONSCIOUSNESS TESTER")
    print("=" * 60)
    
    tester = ConsciousnessTester()
    
    if not tester.connect():
        return
    
    try:
        while True:
            print("\n🧠 AI CONSCIOUSNESS TEST MENU")
            print("1. Demonstrate consciousness profiles")
            print("2. Test individual parameter sweeps") 
            print("3. Interactive consciousness control")
            print("4. Random consciousness states")
            print("5. Reset to neutral")
            print("6. Exit")
            
            choice = input("\nChoice (1-6): ").strip()
            
            if choice == '1':
                tester.demonstrate_consciousness_profiles()
            elif choice == '2':
                print("\nSelect parameter to sweep:")
                for cc_num, desc in list(tester.mapped_controls.items())[:10]:
                    print(f"  CC{cc_num}: {desc}")
                cc_choice = int(input("CC number: "))
                if cc_choice in tester.mapped_controls:
                    tester.test_parameter_sweep(cc_choice, tester.mapped_controls[cc_choice])
            elif choice == '3':
                tester.interactive_consciousness_control()
            elif choice == '4':
                tester.random_consciousness_state()
                tester.send_note(60, 80, 3.0)  # Play test note
            elif choice == '5':
                tester.reset_consciousness()
            elif choice == '6':
                break
            else:
                print("❌ Invalid choice")
                
    except KeyboardInterrupt:
        print("\n👋 Interrupted")
    finally:
        tester.disconnect()

if __name__ == "__main__":
    main()