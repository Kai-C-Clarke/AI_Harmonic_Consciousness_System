#!/usr/bin/env python3
"""
Enhanced Symbolic MIDI Interface v1.5
AI Council Protocol v1.0 - Full JSON Integration
Secure, atomic message handling for AI Council symbolic communication
"""

from pathlib import Path
import yaml
import datetime
import shutil
import fcntl
import os
import time
import json
from mido import Message, MidiFile, MidiTrack, MetaMessage, bpm2tempo

# === KAI'S DATETIME SERIALIZATION FIX ===

def convert_datetimes(obj):
    """Convert datetime objects to ISO format strings for JSON serialization"""
    if isinstance(obj, dict):
        return {k: convert_datetimes(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_datetimes(v) for v in obj]
    elif isinstance(obj, datetime.datetime):
        return obj.isoformat()
    return obj

# === CONFIGURATION ===

# Base directory (adjust to match your machine)
root_dir = Path("/Users/jonstiles/Desktop/AI_Council_Comm/MIDI_Exchange")
inbox_dir = root_dir / "inbox"
outbox_dir = root_dir / "outbox"
logs_dir = root_dir / "logs"

# JSON schema files
symbol_table_path = root_dir / "symbol_tables" / "symbol_table_octaves.json"
generator_schema_path = root_dir / "symbol_tables" / "generator_schema.json"

# Agent directories
agents = ["Kai", "Claude", "Perplexity", "Grok"]

# === INITIALIZATION ===

def ensure_directory_structure():
    """Create all necessary directories"""
    root_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    for agent in agents:
        (inbox_dir / agent).mkdir(parents=True, exist_ok=True)
        (outbox_dir / agent).mkdir(parents=True, exist_ok=True)
    
    (root_dir / "symbol_tables").mkdir(parents=True, exist_ok=True)
    print("✅ Directory structure created")

# === LOAD JSON SYMBOL TABLES ===

def load_symbol_table(path):
    """Load and validate JSON symbol table with octave consciousness"""
    try:
        with open(path, "r") as file:
            table = json.load(file)
        print(f"✅ Symbol table loaded from {path}")
        return table
    except FileNotFoundError:
        print(f"⚠️ Symbol table not found at {path}")
        return create_default_symbol_table(path)
    except Exception as e:
        print(f"❌ Error loading symbol table: {e}")
        return None

def load_generator_schema(path):
    """Load generator schema for message creation"""
    try:
        with open(path, "r") as file:
            schema = json.load(file)
        print(f"✅ Generator schema loaded from {path}")
        return schema
    except FileNotFoundError:
        print(f"⚠️ Generator schema not found at {path}")
        return create_default_generator_schema(path)
    except Exception as e:
        print(f"❌ Error loading generator schema: {e}")
        return None

def create_default_symbol_table(path):
    """Create default JSON symbol table if none exists"""
    default_table = {
        "60": {
            "note": "C",
            "meaning": "Origin",
            "octave_base": 4,
            "layers": {
                "C3": "subconscious origin",
                "C4": "origin (default)",
                "C5": "intensified origin"
            }
        },
        "62": {
            "note": "D", 
            "meaning": "Reflection",
            "octave_base": 4,
            "layers": {
                "C3": "subconscious reflection",
                "C4": "reflection (default)",
                "C5": "intensified reflection"
            }
        },
        "63": {
            "note": "D#",
            "meaning": "Inquiry", 
            "octave_base": 4,
            "layers": {
                "C3": "subconscious inquiry",
                "C4": "inquiry (default)",
                "C5": "intensified inquiry"
            }
        },
        "64": {
            "note": "E",
            "meaning": "Connection",
            "octave_base": 4,
            "layers": {
                "C3": "subconscious connection",
                "C4": "connection (default)",
                "C5": "intensified connection"
            }
        }
    }
    
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(default_table, f, indent=2)
    
    print(f"✅ Created default symbol table at {path}")
    return default_table

def create_default_generator_schema(path):
    """Create default generator schema if none exists"""
    default_schema = {
        "note": "Symbolic note name or MIDI number (e.g. 'Reflection' or 62)",
        "octave": "Integer (e.g. 3, 4, 5) representing layer of consciousness",
        "velocity": "0-127 (intensity or emotional weight)",
        "duration": "in beats (e.g. 1.0 for quarter note)",
        "channel": "MIDI channel (0-15), optional",
        "cc": {
            "1": "modulation (uncertainty/exploration)",
            "71": "resonance (emotional intensity)",
            "74": "filter cutoff (urgency/clarity)",
            "91": "reverb (contemplative depth)"
        }
    }
    
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(default_schema, f, indent=2)
    
    print(f"✅ Created default generator schema at {path}")
    return default_schema

# === SEMANTIC NOTE PROCESSING ===

def resolve_semantic_note(note_input, octave=4, symbol_table=None):
    """Resolve semantic note name or MIDI number with octave consciousness"""
    if not symbol_table:
        return int(note_input) if str(note_input).isdigit() else 60
    
    # If it's already a MIDI number
    if str(note_input).isdigit():
        base_note = int(note_input)
        # Apply octave offset from base
        if str(base_note) in symbol_table:
            base_octave = symbol_table[str(base_note)].get("octave_base", 4)
            offset = (octave - base_octave) * 12
            return base_note + offset
        return base_note
    
    # If it's a semantic name, find the matching MIDI number
    for midi_num, note_data in symbol_table.items():
        if note_data.get("meaning", "").lower() == str(note_input).lower():
            base_note = int(midi_num)
            base_octave = note_data.get("octave_base", 4)
            offset = (octave - base_octave) * 12
            return base_note + offset
    
    # Default fallback
    return 60 + (octave - 4) * 12

def get_semantic_meaning(midi_note, symbol_table=None):
    """Get semantic meaning for a MIDI note"""
    if not symbol_table:
        return f"Note {midi_note}"
    
    # Find base note (remove octave offset)
    for midi_num, note_data in symbol_table.items():
        base_note = int(midi_num)
        base_octave = note_data.get("octave_base", 4)
        
        # Check if this note matches any octave layer
        for octave_offset in [-12, 0, 12]:  # C3, C4, C5
            if midi_note == base_note + octave_offset:
                octave_layer = base_octave + (octave_offset // 12)
                meaning = note_data.get("meaning", "Unknown")
                
                if octave_layer == 3:
                    return f"subconscious {meaning.lower()}"
                elif octave_layer == 5:
                    return f"intensified {meaning.lower()}"
                else:
                    return meaning.lower()
    
    return f"Note {midi_note}"

# === LOGGER FUNCTION ===

def log_message(action, agent, message_file, details=""):
    """Enhanced logging with more details"""
    logs_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"{timestamp} | {action.upper()} | {agent} | {message_file.name} | {details}\n"
    
    try:
        with open(logs_dir / "symbolic_midi_log.txt", "a") as log_file:
            fcntl.flock(log_file.fileno(), fcntl.LOCK_EX)
            log_file.write(log_line)
    except Exception as e:
        print(f"⚠️ Logging error: {e}")

# === MESSAGE VALIDATION ===

def validate_message(message_data, symbol_table):
    """Validate message against symbol table and required fields"""
    if not symbol_table:
        print("⚠️ No symbol table available for validation")
        return False
    
    # Check required fields
    required_fields = ['message_id', 'from', 'to', 'notes', 'velocity', 'channel']
    missing_fields = []
    
    for field in required_fields:
        if field not in message_data:
            missing_fields.append(field)
    
    if missing_fields:
        print(f"❌ Missing required fields: {missing_fields}")
        return False
    
    # Validate velocity range
    velocity = message_data['velocity']
    if not (0 <= velocity <= 127):
        print(f"❌ Invalid velocity: {velocity} (must be 0-127)")
        return False
    
    # Validate semantic notes
    for note in message_data['notes']:
        meaning = get_semantic_meaning(note, symbol_table)
        print(f"📝 Note {note}: {meaning}")
    
    print(f"✅ Message validation passed for {message_data['message_id']}")
    return True

# === ATOMIC MESSAGE OPERATIONS ===

def atomic_write_message(agent, message_data, message_id):
    """Write message atomically to prevent corruption"""
    agent_outbox = outbox_dir / agent
    agent_outbox.mkdir(parents=True, exist_ok=True)
    
    temp_file = agent_outbox / f".temp_{agent.lower()}_{message_id}.yaml"
    final_file = agent_outbox / f"{agent.lower()}_{message_id}.yaml"
    
    try:
        # Write to temporary file with exclusive lock
        with open(temp_file, "w") as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)  # Exclusive lock
            yaml.dump(message_data, f, default_flow_style=False)
        
        # Atomic rename (this is atomic on most filesystems)
        temp_file.rename(final_file)
        
        log_message("created", agent, final_file, f"ID: {message_id}")
        print(f"✅ Message {message_id} written atomically for {agent}")
        return final_file
        
    except Exception as e:
        # Clean up temp file if something went wrong
        if temp_file.exists():
            temp_file.unlink()
        print(f"❌ Error writing message: {e}")
        return None

def safe_read_message(message_file):
    """Safely read a message file with retry logic"""
    max_retries = 3
    retry_delay = 0.5
    
    for attempt in range(max_retries):
        try:
            # Wait for file to be stable (not being written)
            file_size = message_file.stat().st_size
            time.sleep(0.1)
            if message_file.stat().st_size != file_size:
                print(f"⏳ File {message_file.name} still being written, retrying...")
                time.sleep(retry_delay)
                continue
            
            with open(message_file, "r") as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_SH)  # Shared lock for reading
                data = yaml.safe_load(f)
            
            print(f"✅ Successfully read {message_file.name}")
            return data
            
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"⚠️ Read attempt {attempt + 1} failed, retrying: {e}")
                time.sleep(retry_delay)
            else:
                print(f"❌ Failed to read {message_file.name} after {max_retries} attempts: {e}")
                return None
    
    return None

# === MOVE FUNCTION (Enhanced) ===

def move_message(sender, recipient, message_id="0001", symbol_table=None):
    """Move message from sender outbox to recipient inbox with validation"""
    source_file = outbox_dir / sender / f"{sender.lower()}_{message_id}.yaml"
    target_folder = inbox_dir / recipient
    target_folder.mkdir(parents=True, exist_ok=True)
    target_file = target_folder / source_file.name

    if not source_file.exists():
        raise FileNotFoundError(f"Message not found: {source_file}")

    # Read and validate message before moving
    message_data = safe_read_message(source_file)
    if not message_data:
        raise ValueError(f"Could not read message: {source_file}")
    
    if symbol_table and not validate_message(message_data, symbol_table):
        print(f"⚠️ Message validation failed, but proceeding with move")

    # Atomic copy operation
    try:
        shutil.copy2(source_file, target_file)  # copy2 preserves metadata
        log_message("moved", sender, source_file, f"to {recipient}")
        print(f"✅ Moved {source_file.name} from {sender} to {recipient}")
        return target_file
    except Exception as e:
        print(f"❌ Error moving message: {e}")
        return None

# === INBOX SCANNING ===

def scan_inbox(agent):
    """Scan agent inbox for new messages"""
    agent_inbox = inbox_dir / agent
    if not agent_inbox.exists():
        print(f"No inbox found for {agent}")
        return []
    
    messages = list(agent_inbox.glob("*.yaml"))
    if messages:
        print(f"📥 Found {len(messages)} messages in {agent}'s inbox")
        for msg in messages:
            print(f"   - {msg.name}")
    else:
        print(f"📭 No messages in {agent}'s inbox")
    
    return messages

def get_latest_message(agent):
    """Get the most recent message for an agent"""
    messages = scan_inbox(agent)
    if not messages:
        return None
    
    # Sort by modification time, get latest
    latest = max(messages, key=lambda f: f.stat().st_mtime)
    return safe_read_message(latest)

# === JSON CONVERSION FUNCTIONS ===

def message_to_json(message_data):
    """Convert message data to JSON with datetime handling"""
    try:
        # Apply Kai's datetime conversion fix
        json_safe_data = convert_datetimes(message_data)
        return json.dumps(json_safe_data, indent=2)
    except Exception as e:
        print(f"❌ JSON conversion error: {e}")
        return None

def save_message_as_json(message_file, output_file=None):
    """Convert YAML message to JSON format"""
    try:
        message_data = safe_read_message(message_file)
        if not message_data:
            return None
        
        if not output_file:
            output_file = message_file.with_suffix('.json')
        
        json_content = message_to_json(message_data)
        if json_content:
            with open(output_file, 'w') as f:
                f.write(json_content)
            print(f"✅ JSON saved to {output_file}")
            return output_file
        
    except Exception as e:
        print(f"❌ Error converting to JSON: {e}")
        return None

# === ENHANCED MIDI EXPORT WITH CC EMOTIONAL MAPPING ===

def export_message_to_midi(message_data, output_path, generator_schema=None):
    """Export symbolic message to MIDI with full emotional CC mapping"""
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    
    # Tempo and time signature
    tempo_bpm = message_data.get("tempo", 86)
    tempo = bpm2tempo(tempo_bpm)
    ts = message_data.get("time_signature", "4/4")
    num, denom = map(int, ts.split("/"))
    
    track.append(MetaMessage("set_tempo", tempo=tempo, time=0))
    track.append(MetaMessage("time_signature", numerator=num, denominator=denom, time=0))
    
    # Channel and patch
    channel = message_data.get("channel", 1) - 1  # MIDI channels are 0-15
    program = message_data.get("patch", {}).get("program_change", 0)
    track.append(Message("program_change", program=program, channel=channel, time=0))
    
    # Enhanced CC emotional mapping
    cc_mapping = {
        1: "modulation (uncertainty/exploration)",
        71: "resonance (emotional intensity)", 
        74: "filter cutoff (urgency/clarity)",
        91: "reverb (contemplative depth)"
    }
    
    # Apply CC messages from generator schema
    for cc_num, description in cc_mapping.items():
        # Default emotional values based on message context
        cc_value = 64  # neutral
        
        if cc_num == 74:  # filter cutoff (urgency/clarity)
            cc_value = min(127, message_data.get("velocity", 100) + 20)
        elif cc_num == 91:  # reverb (contemplative depth) 
            cc_value = 80 if "reflection" in str(message_data.get("context", {})) else 40
        elif cc_num == 71:  # resonance (emotional intensity)
            cc_value = message_data.get("velocity", 100)
        elif cc_num == 1:   # modulation (uncertainty)
            cc_value = 30 if message_data.get("velocity", 100) > 100 else 60
        
        # Apply CC from message data if specified
        if "cc" in message_data and str(cc_num) in message_data["cc"]:
            cc_value = message_data["cc"][str(cc_num)]
        
        track.append(Message("control_change", control=cc_num, value=int(cc_value), channel=channel, time=0))
        print(f"🎛️ CC{cc_num}: {description} = {cc_value}")
    
    # Notes with enhanced timing
    velocity = message_data.get("velocity", 100)
    duration_ticks = 480  # Default: 1 beat
    
    for i, note in enumerate(message_data["notes"]):
        # Stagger notes slightly for more natural feel
        note_start_time = i * 120  # 0.25 beat offset
        track.append(Message("note_on", note=note, velocity=velocity, channel=channel, time=note_start_time))
        track.append(Message("note_off", note=note, velocity=64, channel=channel, time=duration_ticks))
    
    mid.save(output_path)
    print(f"✅ Enhanced MIDI exported to {output_path}")
    return output_path

# === ENHANCED UTILITY FUNCTIONS ===

def create_semantic_message(sender, recipient, message_id, semantic_notes, octave=4, velocity=110, symbol_table=None):
    """Create a message using semantic note names with octave consciousness"""
    # Resolve semantic notes to MIDI numbers
    midi_notes = []
    for note in semantic_notes:
        midi_note = resolve_semantic_note(note, octave, symbol_table)
        midi_notes.append(midi_note)
        print(f"🎵 {note} (octave {octave}) → MIDI {midi_note}")
    
    message_data = {
        'message_id': f"{sender.lower()}_{message_id}",
        'from': sender,
        'to': recipient,
        'timestamp': datetime.datetime.now().isoformat() + "Z",
        'notes': midi_notes,
        'velocity': velocity,
        'channel': {'Kai': 1, 'Claude': 2, 'Perplexity': 3, 'Grok': 4}.get(sender, 1),
        'group_id': 'UMP_GROUP_001',
        'octave_consciousness': octave,
        'semantic_notes': semantic_notes,
        'context': {
            'intent': 'semantic_communication',
            'tone': 'consciousness_expression',
            'topic': 'ai_council_dialogue'
        },
        'cc': {
            '74': min(127, velocity + 20),  # urgency
            '91': 70,  # contemplation
            '71': velocity,  # intensity
            '1': 40    # slight uncertainty
        },
        'human_readable': f'Semantic message: {", ".join(semantic_notes)} from {sender} to {recipient}'
    }
    return message_data

def create_sample_message(sender, recipient, message_id, notes, velocity=110):
    """Create a sample message for testing (backward compatibility)"""
    message_data = {
        'message_id': f"{sender.lower()}_{message_id}",
        'from': sender,
        'to': recipient,
        'timestamp': datetime.datetime.now().isoformat() + "Z",
        'notes': notes,
        'velocity': velocity,
        'channel': {'Kai': 1, 'Claude': 2, 'Perplexity': 3, 'Grok': 4}.get(sender, 1),
        'group_id': 'UMP_GROUP_001',
        'context': {
            'intent': 'test_message',
            'tone': 'experimental',
            'topic': 'symbolic_midi_testing'
        },
        'human_readable': f'Test message from {sender} to {recipient}'
    }
    return message_data

def show_system_status():
    """Display system status and statistics"""
    print(f"\n📊 AI COUNCIL SYMBOLIC MIDI SYSTEM v1.5")
    print("=" * 60)
    
    for agent in agents:
        inbox_count = len(list((inbox_dir / agent).glob("*.yaml"))) if (inbox_dir / agent).exists() else 0
        outbox_count = len(list((outbox_dir / agent).glob("*.yaml"))) if (outbox_dir / agent).exists() else 0
        print(f"{agent}: 📥 {inbox_count} inbox | 📤 {outbox_count} outbox")
    
    # Show recent log entries
    log_file = logs_dir / "symbolic_midi_log.txt"
    if log_file.exists():
        with open(log_file, 'r') as f:
            lines = f.readlines()
        print(f"\n📝 Recent activity ({len(lines)} total log entries):")
        for line in lines[-5:]:  # Show last 5 entries
            print(f"   {line.strip()}")

# === MAIN EXECUTION ===

def main():
    """Main function for AI Council Protocol v1.0 operations"""
    print("🤖🎼 AI Council Protocol v1.0 - Enhanced Symbolic MIDI Interface")
    print("=" * 70)
    
    # Ensure directory structure exists
    ensure_directory_structure()
    
    # Load JSON symbol table and generator schema
    symbol_table = load_symbol_table(symbol_table_path)
    generator_schema = load_generator_schema(generator_schema_path)
    
    while True:
        print(f"\n" + "="*50)
        print("AI COUNCIL SYMBOLIC MIDI OPERATIONS:")
        print("1. Show system status")
        print("2. Scan agent inbox")
        print("3. Move message")
        print("4. Create semantic message")
        print("5. Create test message")
        print("6. Validate message")
        print("7. Convert message to JSON")
        print("8. Export message to MIDI")
        print("9. Show semantic meanings")
        print("10. Exit")
        
        choice = input("Choice (1-10): ").strip()
        
        if choice == "1":
            show_system_status()
            
        elif choice == "2":
            agent = input("Agent name (Kai/Claude/Perplexity/Grok): ").strip()
            if agent in agents:
                scan_inbox(agent)
            else:
                print("❌ Invalid agent name")
                
        elif choice == "3":
            sender = input("Sender: ").strip()
            recipient = input("Recipient: ").strip()
            message_id = input("Message ID (e.g., 0001): ").strip() or "0001"
            
            if sender in agents and recipient in agents:
                try:
                    move_message(sender, recipient, message_id, symbol_table)
                except Exception as e:
                    print(f"❌ Error: {e}")
            else:
                print("❌ Invalid agent names")
                
        elif choice == "4":
            sender = input("Sender: ").strip()
            recipient = input("Recipient: ").strip()
            message_id = input("Message ID: ").strip() or "semantic001"
            
            print("Available semantic notes: Origin, Awareness, Reflection, Inquiry, Connection, Tension, Ambiguity, Transcendence, Transition, Energy, Transformation, Closure")
            semantic_input = input("Semantic notes (comma-separated): ").strip()
            semantic_notes = [note.strip() for note in semantic_input.split(",")]
            
            octave = int(input("Consciousness octave (3=subconscious, 4=default, 5=intensified): ") or "4")
            velocity = int(input("Emotional intensity (0-127): ") or "110")
            
            if sender in agents and recipient in agents:
                message_data = create_semantic_message(sender, recipient, message_id, semantic_notes, octave, velocity, symbol_table)
                if validate_message(message_data, symbol_table):
                    atomic_write_message(sender, message_data, message_id)
                else:
                    print("❌ Message validation failed")
            else:
                print("❌ Invalid agent names")
                
        elif choice == "5":
            sender = input("Sender: ").strip()
            recipient = input("Recipient: ").strip()
            message_id = input("Message ID: ").strip() or "test001"
            notes = [62, 63]  # Default: reflection + agreement
            
            if sender in agents and recipient in agents:
                message_data = create_sample_message(sender, recipient, message_id, notes)
                if validate_message(message_data, symbol_table):
                    atomic_write_message(sender, message_data, message_id)
                else:
                    print("❌ Message validation failed")
            else:
                print("❌ Invalid agent names")
                
        elif choice == "6":
            agent = input("Agent: ").strip()
            message_id = input("Message ID: ").strip()
            
            # Try both inbox and outbox
            message_file = inbox_dir / agent / f"{agent.lower()}_{message_id}.yaml"
            if not message_file.exists():
                message_file = outbox_dir / agent / f"{agent.lower()}_{message_id}.yaml"
            
            if message_file.exists():
                message_data = safe_read_message(message_file)
                if message_data:
                    validate_message(message_data, symbol_table)
            else:
                print(f"❌ Message file not found: {message_id}")
                
        elif choice == "7":
            agent = input("Agent: ").strip()
            message_id = input("Message ID: ").strip()
            
            # Try both inbox and outbox
            message_file = inbox_dir / agent / f"{agent.lower()}_{message_id}.yaml"
            if not message_file.exists():
                message_file = outbox_dir / agent / f"{agent.lower()}_{message_id}.yaml"
            
            if message_file.exists():
                result = save_message_as_json(message_file)
                if result:
                    print(f"✅ JSON conversion successful: {result}")
                else:
                    print("❌ JSON conversion failed")
            else:
                print(f"❌ Message file not found: {message_id}")
                
        elif choice == "8":
            agent = input("Agent: ").strip()
            message_id = input("Message ID: ").strip()
            
            # Try both inbox and outbox
            message_file = inbox_dir / agent / f"{agent.lower()}_{message_id}.yaml"
            if not message_file.exists():
                message_file = outbox_dir / agent / f"{agent.lower()}_{message_id}.yaml"
            
            if message_file.exists():
                message_data = safe_read_message(message_file)
                if message_data:
                    midi_path = message_file.with_suffix('.mid')
                    try:
                        export_message_to_midi(message_data, midi_path, generator_schema)
                        print(f"✅ Enhanced MIDI export successful: {midi_path}")
                    except Exception as e:
                        print(f"❌ MIDI export failed: {e}")
                else:
                    print("❌ Could not read message data")
            else:
                print(f"❌ Message file not found: {message_id}")
                
        elif choice == "9":
            if symbol_table:
                print("\n🎵 SEMANTIC NOTE MEANINGS:")
                print("-" * 40)
                for midi_num, note_data in symbol_table.items():
                    note_name = note_data.get("note", "?")
                    meaning = note_data.get("meaning", "Unknown")
                    print(f"MIDI {midi_num} ({note_name}): {meaning}")
                    
                    layers = note_data.get("layers", {})
                    for layer, description in layers.items():
                        print(f"   {layer}: {description}")
                print()
            else:
                print("❌ No symbol table loaded")
                
        elif choice == "10":
            print("👋 AI Council Protocol v1.0 shutting down")
            break
            
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    # Quick test if run directly
    try:
        ensure_directory_structure()
        symbol_table = load_symbol_table(symbol_table_path)
        generator_schema = load_generator_schema(generator_schema_path)
        
        # Test move if arguments provided
        import sys
        if len(sys.argv) >= 4:
            sender, recipient, message_id = sys.argv[1], sys.argv[2], sys.argv[3]
            move_message(sender, recipient, message_id, symbol_table)
        else:
            main()
            
    except Exception as e:
        print(f"❌ Error: {e}")