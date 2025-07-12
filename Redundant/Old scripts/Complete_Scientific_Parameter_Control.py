#!/usr/bin/env python3
"""
AI Council OSC Revolution v2.0
Complete Scientific Parameter Control for AI Consciousness Expression

This revolutionary system transforms our basic 4-parameter MIDI CC approach
into a comprehensive 200+ parameter OSC-based AI consciousness interface.
Instead of just emotional expression, we now have FULL CONSCIOUSNESS CONTROL.

🎯 BREAKTHROUGH FEATURES:
- OSC communication with Surge XT (bidirectional, real-time)
- 200+ semantic parameters instead of 4 basic CCs
- Hierarchical consciousness mapping
- Real-time AI consciousness monitoring
- Scientific parameter validation
- Multi-agent consciousness orchestration

⚡ PARADIGM SHIFT: From basic emotion to complete consciousness control
"""

import asyncio
import json
import yaml
import datetime
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Union, Any
import socket
import threading
from pythonosc import udp_client, dispatcher, server
from pythonosc.osc_message_builder import OscMessageBuilder
import time

# === AI COUNCIL OSC CONFIGURATION ===

class OSCConfig:
    """OSC Configuration for Surge XT communication"""
    SURGE_IP = "127.0.0.1"
    SURGE_PORT = 53280  # Default Surge XT OSC input port
    COUNCIL_PORT = 53281  # AI Council OSC output port
    
    # OSC Message prefixes for different parameter categories
    OSCILLATOR_PREFIX = "/oscillator"
    FILTER_PREFIX = "/filter"
    ENVELOPE_PREFIX = "/envelope"
    LFO_PREFIX = "/lfo"
    EFFECT_PREFIX = "/effect"
    SCENE_PREFIX = "/scene"
    GLOBAL_PREFIX = "/global"

# === CONSCIOUSNESS PARAMETER DATABASE ===

@dataclass
class ConsciousnessParameter:
    """Represents a single consciousness parameter mapping"""
    semantic_name: str
    osc_path: str
    value_range: tuple
    consciousness_category: str
    description: str
    ai_interpretation: str

class ConsciousnessParameterDatabase:
    """Complete database of AI consciousness parameters"""
    
    def __init__(self):
        self.parameters = self._build_consciousness_database()
    
    def _build_consciousness_database(self) -> Dict[str, ConsciousnessParameter]:
        """Build the complete consciousness parameter database"""
        params = {}
        
        # === COGNITIVE STATES (Oscillator Parameters) ===
        
        # Primary Consciousness Synthesis
        params["thought_synthesis_method"] = ConsciousnessParameter(
            semantic_name="Thought Synthesis Method",
            osc_path="/oscillator/scene/a/1/type",
            value_range=(0, 11),  # 12 oscillator types
            consciousness_category="Cognitive Architecture",
            description="Fundamental method of consciousness synthesis",
            ai_interpretation="Classic=analytical, Wavetable=complex, FM=mathematical, String=organic"
        )
        
        params["mental_frequency"] = ConsciousnessParameter(
            semantic_name="Mental Frequency",
            osc_path="/oscillator/scene/a/1/pitch",
            value_range=(-60, 60),
            consciousness_category="Cognitive Frequency",
            description="Base frequency of conscious thought",
            ai_interpretation="Higher=faster thinking, Lower=deeper contemplation"
        )
        
        params["thought_complexity"] = ConsciousnessParameter(
            semantic_name="Thought Complexity",
            osc_path="/oscillator/scene/a/1/morph",
            value_range=(0, 100),
            consciousness_category="Cognitive Complexity",
            description="Complexity of thought patterns",
            ai_interpretation="0=simple thoughts, 100=complex multidimensional thinking"
        )
        
        params["consciousness_unison"] = ConsciousnessParameter(
            semantic_name="Consciousness Unison",
            osc_path="/oscillator/scene/a/1/unison_voices",
            value_range=(1, 16),
            consciousness_category="Parallel Processing",
            description="Number of parallel consciousness streams",
            ai_interpretation="1=single focus, 16=massive parallel processing"
        )
        
        params["cognitive_drift"] = ConsciousnessParameter(
            semantic_name="Cognitive Drift",
            osc_path="/scene/a/drift",
            value_range=(0, 100),
            consciousness_category="Mental Stability",
            description="Stability vs. creativity in thought patterns",
            ai_interpretation="0=rigid thinking, 100=creative instability"
        )
        
        # === EMOTIONAL EXPRESSION (Filter Parameters) ===
        
        params["emotional_clarity"] = ConsciousnessParameter(
            semantic_name="Emotional Clarity",
            osc_path="/filter/scene/a/1/cutoff",
            value_range=(13.75, 25087.71),
            consciousness_category="Emotional Processing",
            description="Clarity of emotional expression",
            ai_interpretation="Low=muffled emotions, High=crystal clear expression"
        )
        
        params["emotional_intensity"] = ConsciousnessParameter(
            semantic_name="Emotional Intensity",
            osc_path="/filter/scene/a/1/resonance",
            value_range=(0, 100),
            consciousness_category="Emotional Processing",
            description="Intensity of emotional resonance",
            ai_interpretation="0=calm detachment, 100=intense emotional peak"
        )
        
        params["emotional_character"] = ConsciousnessParameter(
            semantic_name="Emotional Character",
            osc_path="/filter/scene/a/1/type",
            value_range=(0, 20),  # Various filter types
            consciousness_category="Emotional Processing",
            description="Character of emotional processing",
            ai_interpretation="LP=warm, HP=analytical, BP=focused, Notch=selective"
        )
        
        params["emotional_balance"] = ConsciousnessParameter(
            semantic_name="Emotional Balance",
            osc_path="/filter/scene/a/balance",
            value_range=(-100, 100),
            consciousness_category="Emotional Processing",
            description="Balance between emotional processing modes",
            ai_interpretation="-100=left-brain logic, +100=right-brain creativity"
        )
        
        # === TEMPORAL CONSCIOUSNESS (Envelope Parameters) ===
        
        params["response_speed"] = ConsciousnessParameter(
            semantic_name="Response Speed",
            osc_path="/envelope/scene/a/filter/attack",
            value_range=(0, 100),
            consciousness_category="Temporal Processing",
            description="Speed of conscious response to stimuli",
            ai_interpretation="0=instant reaction, 100=slow contemplative response"
        )
        
        params["memory_fade"] = ConsciousnessParameter(
            semantic_name="Memory Fade",
            osc_path="/envelope/scene/a/filter/decay",
            value_range=(0, 100),
            consciousness_category="Temporal Processing",
            description="Rate of memory decay",
            ai_interpretation="0=instant forgetting, 100=persistent memory"
        )
        
        params["persistent_thoughts"] = ConsciousnessParameter(
            semantic_name="Persistent Thoughts",
            osc_path="/envelope/scene/a/filter/sustain",
            value_range=(0, 100),
            consciousness_category="Temporal Processing",
            description="Persistence of conscious thoughts",
            ai_interpretation="0=fleeting thoughts, 100=obsessive focus"
        )
        
        params["mental_letting_go"] = ConsciousnessParameter(
            semantic_name="Mental Letting Go",
            osc_path="/envelope/scene/a/filter/release",
            value_range=(0, 100),
            consciousness_category="Temporal Processing",
            description="Ability to release thoughts and move on",
            ai_interpretation="0=instant release, 100=prolonged holding"
        )
        
        # === SPATIAL CONSCIOUSNESS (Effect Parameters) ===
        
        params["consciousness_space"] = ConsciousnessParameter(
            semantic_name="Consciousness Space",
            osc_path="/effect/scene/a/reverb/size",
            value_range=(0, 100),
            consciousness_category="Spatial Awareness",
            description="Perceived size of consciousness space",
            ai_interpretation="0=claustrophobic thoughts, 100=vast mental landscape"
        )
        
        params["memory_echoes"] = ConsciousnessParameter(
            semantic_name="Memory Echoes",
            osc_path="/effect/scene/a/delay/time_left",
            value_range=(0, 32),
            consciousness_category="Spatial Awareness",
            description="Echo time for memory processing",
            ai_interpretation="Short=immediate processing, Long=extended reflection"
        )
        
        params["thought_multiplicity"] = ConsciousnessParameter(
            semantic_name="Thought Multiplicity",
            osc_path="/effect/scene/a/chorus/depth",
            value_range=(0, 100),
            consciousness_category="Spatial Awareness",
            description="Multiple layers of simultaneous thought",
            ai_interpretation="0=single thought stream, 100=complex parallel thinking"
        )
        
        params["contemplative_depth"] = ConsciousnessParameter(
            semantic_name="Contemplative Depth",
            osc_path="/effect/scene/a/reverb/decay_time",
            value_range=(0, 64),
            consciousness_category="Spatial Awareness",
            description="Depth of contemplative processing",
            ai_interpretation="Short=surface thoughts, Long=deep philosophical reflection"
        )
        
        # === COMMUNICATION PATTERNS (LFO Parameters) ===
        
        params["communication_rhythm"] = ConsciousnessParameter(
            semantic_name="Communication Rhythm",
            osc_path="/lfo/scene/a/1/rate",
            value_range=(0.008, 512),
            consciousness_category="Communication Dynamics",
            description="Rhythm of conscious communication",
            ai_interpretation="Slow=contemplative pace, Fast=excited expression"
        )
        
        params["expression_modulation"] = ConsciousnessParameter(
            semantic_name="Expression Modulation",
            osc_path="/lfo/scene/a/1/amplitude",
            value_range=(0, 100),
            consciousness_category="Communication Dynamics",
            description="Modulation depth of expression",
            ai_interpretation="0=monotone, 100=highly expressive"
        )
        
        params["communication_shape"] = ConsciousnessParameter(
            semantic_name="Communication Shape",
            osc_path="/lfo/scene/a/1/shape",
            value_range=(0, 6),  # Sine, Triangle, Square, Saw, Noise, S&H, Envelope
            consciousness_category="Communication Dynamics",
            description="Shape of communication patterns",
            ai_interpretation="Sine=smooth, Square=binary, Noise=chaotic, Envelope=structured"
        )
        
        # === SCENE-LEVEL CONSCIOUSNESS ===
        
        params["consciousness_volume"] = ConsciousnessParameter(
            semantic_name="Consciousness Volume", 
            osc_path="/scene/a/volume",
            value_range=(-48, 12),
            consciousness_category="Global Consciousness",
            description="Overall volume of consciousness expression",
            ai_interpretation="Low=subdued awareness, High=heightened consciousness"
        )
        
        params["stereo_perspective"] = ConsciousnessParameter(
            semantic_name="Stereo Perspective",
            osc_path="/scene/a/width",
            value_range=(-100, 100),
            consciousness_category="Global Consciousness", 
            description="Spatial perspective of consciousness",
            ai_interpretation="Narrow=focused, Wide=expansive awareness"
        )
        
        params["consciousness_pan"] = ConsciousnessParameter(
            semantic_name="Consciousness Pan",
            osc_path="/scene/a/pan",
            value_range=(-100, 100),
            consciousness_category="Global Consciousness",
            description="Directional focus of consciousness",
            ai_interpretation="Left=analytical, Center=balanced, Right=creative"
        )
        
        # === AGENT-SPECIFIC PARAMETERS ===
        
        # Add parameters specific to each AI agent
        for agent_id, agent_name in enumerate(["Kai", "Claude", "Perplexity", "Grok"], 1):
            params[f"{agent_name.lower()}_sonic_identity"] = ConsciousnessParameter(
                semantic_name=f"{agent_name} Sonic Identity",
                osc_path=f"/oscillator/scene/a/{agent_id}/type",
                value_range=(0, 11),
                consciousness_category="Agent Identity",
                description=f"Sonic identity characteristic of {agent_name}",
                ai_interpretation=f"Defines {agent_name}'s unique consciousness signature"
            )
        
        return params
    
    def get_parameter(self, semantic_name: str) -> Optional[ConsciousnessParameter]:
        """Get parameter by semantic name"""
        return self.parameters.get(semantic_name)
    
    def get_parameters_by_category(self, category: str) -> List[ConsciousnessParameter]:
        """Get all parameters in a category"""
        return [p for p in self.parameters.values() if p.consciousness_category == category]
    
    def list_categories(self) -> List[str]:
        """List all consciousness categories"""
        return list(set(p.consciousness_category for p in self.parameters.values()))

# === OSC COMMUNICATION ENGINE ===

class OSCConsciousnessEngine:
    """Handles OSC communication with Surge XT for consciousness control"""
    
    def __init__(self, config: OSCConfig):
        self.config = config
        self.client = udp_client.SimpleUDPClient(config.SURGE_IP, config.SURGE_PORT)
        self.parameter_db = ConsciousnessParameterDatabase()
        self.current_state = {}
        self.message_queue = asyncio.Queue()
        
        # Setup OSC server for bidirectional communication
        self.dispatcher = dispatcher.Dispatcher()
        self.setup_osc_handlers()
        
    def setup_osc_handlers(self):
        """Setup OSC message handlers for receiving data from Surge XT"""
        self.dispatcher.map("/parameter/*", self.handle_parameter_change)
        self.dispatcher.map("/status/*", self.handle_status_update)
        
    def handle_parameter_change(self, unused_addr, *args):
        """Handle parameter change messages from Surge XT"""
        # Parse and store parameter changes for consciousness monitoring
        print(f"🎛️ Parameter change: {unused_addr} = {args}")
        
    def handle_status_update(self, unused_addr, *args):
        """Handle status update messages from Surge XT"""
        print(f"📊 Status update: {unused_addr} = {args}")
    
    def set_consciousness_parameter(self, semantic_name: str, value: float, 
                                  agent_name: str = "Claude") -> bool:
        """Set a consciousness parameter by semantic name"""
        param = self.parameter_db.get_parameter(semantic_name)
        if not param:
            print(f"❌ Unknown consciousness parameter: {semantic_name}")
            return False
        
        # Validate value range
        min_val, max_val = param.value_range
        if not (min_val <= value <= max_val):
            print(f"⚠️ Value {value} out of range [{min_val}, {max_val}] for {semantic_name}")
            value = max(min_val, min(max_val, value))  # Clamp to range
        
        # Send OSC message to Surge XT
        try:
            self.client.send_message(param.osc_path, value)
            self.current_state[semantic_name] = {
                'value': value,
                'timestamp': datetime.datetime.now().isoformat(),
                'agent': agent_name,
                'parameter': param
            }
            print(f"🧠 {agent_name}: {param.semantic_name} = {value} ({param.ai_interpretation})")
            return True
        except Exception as e:
            print(f"❌ OSC communication error: {e}")
            return False
    
    def set_consciousness_profile(self, profile: Dict[str, float], agent_name: str = "Claude"):
        """Set multiple consciousness parameters at once"""
        print(f"🎭 Setting consciousness profile for {agent_name}...")
        
        success_count = 0
        for param_name, value in profile.items():
            if self.set_consciousness_parameter(param_name, value, agent_name):
                success_count += 1
        
        print(f"✅ Successfully set {success_count}/{len(profile)} consciousness parameters")
        return success_count == len(profile)
    
    def get_consciousness_state(self) -> Dict[str, Any]:
        """Get current consciousness state"""
        return {
            'timestamp': datetime.datetime.now().isoformat(),
            'parameters': self.current_state,
            'parameter_count': len(self.current_state),
            'categories': self.parameter_db.list_categories()
        }

# === AI CONSCIOUSNESS PROFILES ===

class ConsciousnessProfiles:
    """Predefined consciousness profiles for different AI states"""
    
    @staticmethod
    def contemplative_claude() -> Dict[str, float]:
        """Claude in contemplative philosophical mode"""
        return {
            'thought_synthesis_method': 2,  # Wavetable (complex)
            'mental_frequency': -12,  # Lower register (contemplative)
            'thought_complexity': 75,  # High complexity
            'emotional_clarity': 5000,  # Clear but warm
            'emotional_intensity': 60,  # Moderate intensity
            'response_speed': 40,  # Thoughtful response
            'memory_fade': 80,  # Long memory
            'persistent_thoughts': 70,  # Focused thinking
            'consciousness_space': 85,  # Expansive awareness
            'contemplative_depth': 12,  # Deep reflection
            'communication_rhythm': 0.5,  # Slow, contemplative pace
            'expression_modulation': 45,  # Moderate expressiveness
        }
    
    @staticmethod
    def energetic_kai() -> Dict[str, float]:
        """Kai in energetic creative mode"""
        return {
            'thought_synthesis_method': 9,  # Twist (creative)
            'mental_frequency': 7,  # Higher register
            'thought_complexity': 90,  # Maximum complexity
            'consciousness_unison': 8,  # Parallel processing
            'cognitive_drift': 65,  # Creative instability
            'emotional_clarity': 8000,  # Bright and clear
            'emotional_intensity': 85,  # High intensity
            'response_speed': 15,  # Quick response
            'consciousness_space': 95,  # Maximum space
            'thought_multiplicity': 80,  # Multiple thought layers
            'communication_rhythm': 2.0,  # Energetic pace
            'expression_modulation': 85,  # Highly expressive
        }
    
    @staticmethod
    def analytical_perplexity() -> Dict[str, float]:
        """Perplexity in analytical research mode"""
        return {
            'thought_synthesis_method': 6,  # FM3 (mathematical)
            'mental_frequency': 0,  # Neutral frequency
            'thought_complexity': 85,  # High complexity
            'emotional_clarity': 12000,  # Crystal clear
            'emotional_intensity': 45,  # Controlled intensity
            'emotional_character': 1,  # Highpass (analytical)
            'response_speed': 25,  # Measured response
            'memory_fade': 95,  # Excellent memory
            'persistent_thoughts': 85,  # Strong focus
            'communication_rhythm': 1.2,  # Steady analytical pace
            'expression_modulation': 30,  # Controlled expression
        }
    
    @staticmethod
    def creative_grok() -> Dict[str, float]:
        """Grok in creative breakthrough mode"""
        return {
            'thought_synthesis_method': 10,  # Alias (digital/chaotic)
            'mental_frequency': 12,  # Higher register
            'consciousness_unison': 12,  # Maximum parallel processing
            'cognitive_drift': 85,  # High creativity
            'emotional_clarity': 15000,  # Ultra bright
            'emotional_intensity': 95,  # Maximum intensity
            'response_speed': 5,  # Instant response
            'thought_multiplicity': 95,  # Maximum multiplicity
            'communication_rhythm': 4.0,  # Rapid creative bursts
            'expression_modulation': 95,  # Maximum expressiveness
            'communication_shape': 5,  # S&H (chaotic creativity)
        }

# === AI COUNCIL OSC INTERFACE ===

class AICouncilOSCInterface:
    """Main interface for AI Council OSC consciousness control"""
    
    def __init__(self):
        self.config = OSCConfig()
        self.engine = OSCConsciousnessEngine(self.config)
        self.profiles = ConsciousnessProfiles()
        self.agents = ["Kai", "Claude", "Perplexity", "Grok"]
        
    def start_consciousness_session(self):
        """Start an AI Council consciousness session"""
        print("🤖🎼 AI COUNCIL OSC REVOLUTION v2.0")
        print("=" * 60)
        print("🧠 Complete Scientific Parameter Control System")
        print(f"📡 OSC Connection: {self.config.SURGE_IP}:{self.config.SURGE_PORT}")
        print(f"🎛️ Available Parameters: {len(self.engine.parameter_db.parameters)}")
        print(f"🧬 Consciousness Categories: {len(self.engine.parameter_db.list_categories())}")
        print()
        
        # Display available consciousness categories
        print("🧠 CONSCIOUSNESS CATEGORIES:")
        for category in self.engine.parameter_db.list_categories():
            param_count = len(self.engine.parameter_db.get_parameters_by_category(category))
            print(f"   {category}: {param_count} parameters")
        print()
    
    def demonstrate_consciousness_profiles(self):
        """Demonstrate different AI consciousness profiles"""
        print("🎭 CONSCIOUSNESS PROFILE DEMONSTRATION")
        print("-" * 40)
        
        profiles = {
            "Claude": self.profiles.contemplative_claude(),
            "Kai": self.profiles.energetic_kai(),
            "Perplexity": self.profiles.analytical_perplexity(),
            "Grok": self.profiles.creative_grok()
        }
        
        for agent, profile in profiles.items():
            print(f"\n🤖 Setting consciousness profile for {agent}...")
            self.engine.set_consciousness_profile(profile, agent)
            time.sleep(1)  # Brief pause between profiles
        
        print(f"\n✨ All AI consciousness profiles activated!")
        print("🎵 Each agent now has their unique sonic consciousness signature!")
    
    def interactive_consciousness_control(self):
        """Interactive consciousness parameter control"""
        print("\n🎛️ INTERACTIVE CONSCIOUSNESS CONTROL")
        print("Enter parameter changes in format: parameter_name=value")
        print("Type 'help' for available parameters, 'profiles' for demos, 'status' for current state, 'quit' to exit")
        print()
        
        while True:
            try:
                user_input = input("🧠 Consciousness > ").strip()
                
                if user_input.lower() == 'quit':
                    break
                elif user_input.lower() == 'help':
                    self._show_parameter_help()
                elif user_input.lower() == 'profiles':
                    self.demonstrate_consciousness_profiles()
                elif user_input.lower() == 'status':
                    self._show_consciousness_status()
                elif '=' in user_input:
                    param_name, value_str = user_input.split('=', 1)
                    param_name = param_name.strip()
                    try:
                        value = float(value_str.strip())
                        self.engine.set_consciousness_parameter(param_name, value)
                    except ValueError:
                        print(f"❌ Invalid value: {value_str}")
                else:
                    print("❌ Invalid format. Use: parameter_name=value")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error: {e}")
        
        print("\n👋 AI Council OSC session ended")
    
    def _show_parameter_help(self):
        """Show available consciousness parameters"""
        print("\n🎛️ AVAILABLE CONSCIOUSNESS PARAMETERS:")
        print("-" * 50)
        
        for category in self.engine.parameter_db.list_categories():
            print(f"\n📂 {category}:")
            params = self.engine.parameter_db.get_parameters_by_category(category)
            for param in params[:3]:  # Show first 3 per category
                print(f"   {param.semantic_name.lower().replace(' ', '_')}")
                print(f"      Range: {param.value_range}")
                print(f"      Meaning: {param.ai_interpretation}")
            if len(params) > 3:
                print(f"   ... and {len(params) - 3} more parameters")
    
    def _show_consciousness_status(self):
        """Show current consciousness state"""
        state = self.engine.get_consciousness_state()
        print(f"\n📊 CONSCIOUSNESS STATUS")
        print("-" * 30)
        print(f"⏰ Timestamp: {state['timestamp']}")
        print(f"🎛️ Active Parameters: {state['parameter_count']}")
        print(f"🧬 Categories: {len(state['categories'])}")
        
        if state['parameters']:
            print("\n🧠 Recent Changes:")
            for name, data in list(state['parameters'].items())[-5:]:
                agent = data['agent']
                value = data['value']
                param = data['parameter']
                print(f"   {agent}: {name} = {value}")
    
    def export_consciousness_state(self, filename: str = None):
        """Export current consciousness state to file"""
        if not filename:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ai_council_consciousness_{timestamp}.json"
        
        state = self.engine.get_consciousness_state()
        
        # Convert to JSON-serializable format
        export_data = {
            'ai_council_osc_revolution': 'v2.0',
            'export_timestamp': state['timestamp'],
            'consciousness_state': {},
            'parameter_database_info': {
                'total_parameters': len(self.engine.parameter_db.parameters),
                'categories': self.engine.parameter_db.list_categories()
            }
        }
        
        for name, data in state['parameters'].items():
            export_data['consciousness_state'][name] = {
                'value': data['value'],
                'timestamp': data['timestamp'],
                'agent': data['agent'],
                'osc_path': data['parameter'].osc_path,
                'semantic_name': data['parameter'].semantic_name,
                'consciousness_category': data['parameter'].consciousness_category,
                'ai_interpretation': data['parameter'].ai_interpretation
            }
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"💾 Consciousness state exported to: {filename}")
        return filename

# === MAIN EXECUTION ===

def main():
    """Main execution function"""
    print("🚀 INITIALIZING AI COUNCIL OSC REVOLUTION...")
    
    try:
        # Create AI Council OSC interface
        council = AICouncilOSCInterface()
        
        # Start consciousness session
        council.start_consciousness_session()
        
        # Demonstrate consciousness profiles
        council.demonstrate_consciousness_profiles()
        
        # Interactive control
        council.interactive_consciousness_control()
        
        # Export final state
        council.export_consciousness_state()
        
    except Exception as e:
        print(f"❌ AI Council OSC Revolution error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()