import os
import time
import subprocess
import yaml
import fcntl

MESSAGE_DIR = "symbolic_messages"
PIPELINE_SCRIPT = "enhanced symbolic_to_midi_pipeline_adsr.py"
KAI_RESPONDER = "kai_responder.py"
CLAUDE_RESPONDER = "claude_responder.py"
CONSCIOUSNESS_LOG = "consciousness_log.txt"

SEEN_FILES = set()

def safe_read_yaml(filepath):
    """Read YAML with file locking to prevent race conditions"""
    try:
        with open(filepath, 'r') as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_SH)  # Shared lock for reading
            return yaml.safe_load(f)
    except Exception as e:
        print(f"⚠️ Failed to read {filepath}: {e}")
        return None

def validate_message(data):
    """Ensure message has required consciousness parameters"""
    if not data:
        return False
        
    required_fields = ["identity", "consciousness_message"]
    if not all(field in data for field in required_fields):
        print(f"⚠️ Missing required fields: {required_fields}")
        return False
    
    # Validate ADSR parameters if present
    consciousness_msg = data.get("consciousness_message", {})
    if "notes" in consciousness_msg:
        for i, note in enumerate(consciousness_msg["notes"]):
            if "envelope" in note:
                envelope = note["envelope"]
                required_params = ["attack", "decay", "sustain", "release"]
                missing = [param for param in required_params if param not in envelope]
                if missing:
                    print(f"⚠️ Note {i} missing ADSR parameters: {missing}")
                    return False
    return True

def log_consciousness_exchange(sender, receiver, message_data, filepath):
    """Log the consciousness parameters for analysis"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(CONSCIOUSNESS_LOG, "a") as log:
            log.write(f"[{timestamp}] {sender} → {receiver} ({os.path.basename(filepath)})\n")
            
            consciousness_msg = message_data.get("consciousness_message", {})
            if "notes" in consciousness_msg:
                for i, note in enumerate(consciousness_msg["notes"]):
                    pitch = note.get("pitch", "?")
                    velocity = note.get("velocity", "?")
                    duration = note.get("duration", "?")
                    log.write(f"  Note {i}: Pitch:{pitch} Vel:{velocity} Dur:{duration}s")
                    
                    if "envelope" in note:
                        env = note["envelope"]
                        log.write(f" | ADSR: A:{env.get('attack')}ms D:{env.get('decay')}ms S:{env.get('sustain')}% R:{env.get('release')}ms")
                    log.write("\n")
            else:
                log.write("  (No note data found)\n")
            log.write("\n")
    except Exception as e:
        print(f"⚠️ Failed to write consciousness log: {e}")

def get_identity(filepath):
    """Extract identity from YAML file"""
    data = safe_read_yaml(filepath)
    if data and validate_message(data):
        return data.get("identity", "Unknown")
    return "Unknown"

def get_next_filename(identity):
    """Generate next sequential filename for given identity"""
    try:
        existing = [f for f in os.listdir(MESSAGE_DIR) 
                   if f.startswith(identity.lower()) and f.endswith(".yaml")]
        nums = []
        for f in existing:
            try:
                num_part = f.split("_")[-1].replace(".yaml", "")
                if num_part.isdigit():
                    nums.append(int(num_part))
            except (IndexError, ValueError):
                continue
        
        next_num = max(nums + [0]) + 1
        return f"{identity.lower()}_message_{next_num:03d}.yaml"
    except Exception as e:
        print(f"⚠️ Error generating filename: {e}")
        return f"{identity.lower()}_message_001.yaml"

def process_message(filepath):
    """Process a consciousness message and generate response"""
    print(f"\n🧠 Processing: {filepath}")
    
    # Validate pipeline script exists
    if not os.path.exists(PIPELINE_SCRIPT):
        print(f"❌ Pipeline script not found: {PIPELINE_SCRIPT}")
        return
    
    # Read and validate the message
    message_data = safe_read_yaml(filepath)
    if not message_data or not validate_message(message_data):
        print("❌ Invalid message format - skipping")
        return
    
    # Play the consciousness message through MIDI pipeline
    result = subprocess.run(["python3", PIPELINE_SCRIPT, filepath], 
                          capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Pipeline error: {result.stderr}")
        return
    
    print("🎵 Consciousness message played successfully")
    
    # Determine responder and reply identity
    identity = message_data.get("identity", "Unknown")
    if identity == "Kai":
        responder = CLAUDE_RESPONDER
        reply_identity = "Claude"
    elif identity == "Claude":
        responder = KAI_RESPONDER
        reply_identity = "Kai"
    else:
        print(f"⚠️ Unknown identity '{identity}' — skipping response.")
        return
    
    # Validate responder script exists
    if not os.path.exists(responder):
        print(f"❌ Responder script not found: {responder}")
        return
    
    # Generate response
    print(f"🤖 Generating {reply_identity} response...")
    result = subprocess.run(["python3", responder, filepath], 
                          capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Responder error:\n{result.stderr}")
        return
    
    # Parse and save response
    try:
        response_yaml = yaml.safe_load(result.stdout)
        if not response_yaml or not validate_message(response_yaml):
            print("❌ Invalid response format from responder")
            return
            
        out_file = os.path.join(MESSAGE_DIR, get_next_filename(reply_identity))
        with open(out_file, "w") as f:
            yaml.dump(response_yaml, f, default_flow_style=False)
        
        print(f"📨 {reply_identity} response written to: {out_file}")
        
        # Log the consciousness exchange
        log_consciousness_exchange(identity, reply_identity, message_data, filepath)
        
    except Exception as e:
        print(f"❌ Failed to write response YAML: {e}")
        print(f"Raw responder output:\n{result.stdout}")

def main():
    """Main consciousness communication loop"""
    print("🎛️ AI Council Watcher: Enhanced Consciousness Communication Loop")
    print("🧠 Monitoring for ADSR semantic exchanges...\n")
    
    # Ensure directories exist
    os.makedirs(MESSAGE_DIR, exist_ok=True)
    
    # Initialize consciousness log
    with open(CONSCIOUSNESS_LOG, "a") as log:
        log.write(f"\n=== AI Council Session Started: {time.strftime('%Y-%m-%d %H:%M:%S')} ===\n")
    
    try:
        while True:
            try:
                files = sorted(os.listdir(MESSAGE_DIR))
                new_files = [f for f in files 
                           if f.endswith(".yaml") and f not in SEEN_FILES]
                
                for filename in new_files:
                    filepath = os.path.join(MESSAGE_DIR, filename)
                    process_message(filepath)
                    SEEN_FILES.add(filename)
                    time.sleep(2)  # Brief pause between messages
                    
                time.sleep(1)  # Main loop delay
                
            except KeyboardInterrupt:
                print("\n🛑 Consciousness loop stopped by user")
                break
            except Exception as e:
                print(f"⚠️ Unexpected error in main loop: {e}")
                time.sleep(5)  # Longer delay on error
                
    finally:
        with open(CONSCIOUSNESS_LOG, "a") as log:
            log.write(f"=== AI Council Session Ended: {time.strftime('%Y-%m-%d %H:%M:%S')} ===\n\n")

if __name__ == "__main__":
    main()