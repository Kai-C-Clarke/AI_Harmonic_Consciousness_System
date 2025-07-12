import os
import time
import subprocess
import yaml
import fcntl

MESSAGE_DIR = "symbolic_messages"
PIPELINE_SCRIPT = "enhanced symbolic_to_midi_pipeline_adsr.py"
AI_RESPONDER = "ai_responder_harmonic.py"  # Updated to use the new harmonic responder
CONSCIOUSNESS_LOG = "consciousness_log.txt"

SEEN_FILES = set()

def safe_read_yaml(filepath):
    try:
        with open(filepath, 'r') as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_SH)
            return yaml.safe_load(f)
    except Exception as e:
        print(f"⚠️ Failed to read {filepath}: {e}")
        return None

def validate_harmonic_message(data):
    """Validate new harmonic consciousness message format"""
    try:
        if not data:
            return False
        
        # Check for required top-level keys
        if "identity" not in data or "consciousness_message" not in data:
            return False
        
        consciousness_msg = data["consciousness_message"]
        
        # Check for envelope at message level
        if "envelope" not in consciousness_msg:
            return False
        
        envelope = consciousness_msg["envelope"]
        required_envelope_keys = ["attack", "decay", "sustain", "release"]
        for key in required_envelope_keys:
            if key not in envelope:
                return False
        
        # Check for oscillators array
        if "oscillators" not in consciousness_msg:
            return False
        
        oscillators = consciousness_msg["oscillators"]
        if not isinstance(oscillators, list) or len(oscillators) == 0:
            return False
        
        # Validate each oscillator
        for i, osc in enumerate(oscillators):
            required_osc_keys = ["pitch", "role", "phase", "amplitude"]
            for key in required_osc_keys:
                if key not in osc:
                    print(f"⚠️ Oscillator {i} missing required key: {key}")
                    return False
        
        # Check for interpretation section (optional but recommended)
        if "interpretation" in consciousness_msg:
            interp = consciousness_msg["interpretation"]
            if "state" not in interp or "intensity" not in interp:
                print("⚠️ Interpretation section incomplete")
                # Don't fail validation for this, just warn
        
        return True
        
    except Exception as e:
        print(f"⚠️ Validation error: {e}")
        return False

def log_harmonic_consciousness_exchange(sender, receiver, message_data, filepath):
    """Log harmonic consciousness exchange with new format"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(CONSCIOUSNESS_LOG, "a") as log:
            log.write(f"[{timestamp}] {sender} → {receiver} ({os.path.basename(filepath)})\n")
            
            consciousness_msg = message_data["consciousness_message"]
            
            # Log envelope
            envelope = consciousness_msg.get("envelope", {})
            log.write(f"  Envelope: A:{envelope.get('attack')}ms D:{envelope.get('decay')}ms S:{envelope.get('sustain')}% R:{envelope.get('release')}ms\n")
            
            # Log oscillators
            oscillators = consciousness_msg.get("oscillators", [])
            for i, osc in enumerate(oscillators):
                log.write(f"  Osc {i+1}: {osc.get('role', 'unknown')} | Pitch:{osc.get('pitch')} Amp:{osc.get('amplitude')} Phase:{osc.get('phase')}°\n")
            
            # Log interpretation if present
            if "interpretation" in consciousness_msg:
                interp = consciousness_msg["interpretation"]
                log.write(f"  State: {interp.get('state', 'unknown')} | Intensity: {interp.get('intensity', 'unknown')}\n")
                semantics = interp.get('semantics', [])
                if semantics:
                    log.write(f"  Semantics: {', '.join(semantics)}\n")
            
            log.write("\n")
            
    except Exception as e:
        print(f"⚠️ Failed to write consciousness log: {e}")

def get_next_filename(identity):
    try:
        files = [f for f in os.listdir(MESSAGE_DIR) if f.startswith(identity.lower())]
        nums = [int(f.split("_")[-1].split(".")[0]) for f in files if f.split("_")[-1].split(".")[0].isdigit()]
        next_num = max(nums + [0]) + 1
        return f"{identity.lower()}_message_{next_num:03d}.yaml"
    except Exception as e:
        print(f"⚠️ Error generating filename: {e}")
        return f"{identity.lower()}_message_001.yaml"

def process_message(filepath):
    print(f"\n🧠 Processing: {filepath}")
    
    try:
        # Use absolute paths to avoid subprocess working directory issues
        pipeline_path = os.path.abspath(PIPELINE_SCRIPT)
        responder_path = os.path.abspath(AI_RESPONDER)
        file_path = os.path.abspath(filepath)
        
        # Check if pipeline script exists
        if not os.path.exists(pipeline_path):
            print(f"❌ Missing pipeline script: {pipeline_path}")
            return

        # Read and validate the message
        data = safe_read_yaml(filepath)
        if not validate_harmonic_message(data):
            print("❌ Invalid harmonic message format.")
            return

        # Run the MIDI pipeline
        print("🎵 Running MIDI pipeline...")
        pipeline_result = subprocess.run(["python3", pipeline_path, file_path], 
                                       capture_output=True, text=True)
        if pipeline_result.returncode != 0:
            print(f"❌ Pipeline error: {pipeline_result.stderr}")
            return
        else:
            print("✅ MIDI pipeline completed successfully")

        # Determine response identity
        identity = data["identity"]
        reply_identity = "Kai" if identity == "Claude" else "Claude"

        # Generate AI response
        print(f"🤖 Generating {reply_identity} response...")
        result = subprocess.run(["python3", responder_path, file_path], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ AI responder error: {result.stderr}")
            return

        # Parse and validate the response
        try:
            response_data = yaml.safe_load(result.stdout)
            if not validate_harmonic_message(response_data):
                print("❌ Invalid response structure from AI responder.")
                print(f"Raw response: {result.stdout[:200]}...")
                return

            # Save the response
            out_path = os.path.join(MESSAGE_DIR, get_next_filename(reply_identity))
            with open(out_path, "w") as f:
                yaml.dump(response_data, f, default_flow_style=False)
            
            print(f"📨 {reply_identity} response saved: {out_path}")
            
            # Log the consciousness exchange
            log_harmonic_consciousness_exchange(identity, reply_identity, data, filepath)
            
        except yaml.YAMLError as e:
            print(f"❌ YAML parsing error in response: {e}")
            print(f"Raw response: {result.stdout}")
        except Exception as e:
            print(f"❌ Failed to parse/write response: {type(e).__name__}: {e}")

    except Exception as e:
        print(f"❌ Error processing message: {type(e).__name__}: {e}")

def main():
    print("🎛️ AI Council Harmonic Consciousness Watcher (V5)")
    print("🎵 Now supporting harmonic consciousness format with oscillators!")
    
    # Ensure message directory exists
    os.makedirs(MESSAGE_DIR, exist_ok=True)
    
    # Initialize consciousness log
    try:
        with open(CONSCIOUSNESS_LOG, "a") as log:
            log.write(f"\n=== AI Council Harmonic Session Started: {time.strftime('%Y-%m-%d %H:%M:%S')} ===\n")
    except Exception as e:
        print(f"⚠️ Could not initialize consciousness log: {e}")

    try:
        print("👀 Watching for new harmonic consciousness messages...")
        while True:
            try:
                files = sorted(os.listdir(MESSAGE_DIR))
                new_files = [f for f in files if f.endswith(".yaml") and f not in SEEN_FILES]
                
                for file in new_files:
                    file_path = os.path.join(MESSAGE_DIR, file)
                    process_message(file_path)
                    SEEN_FILES.add(file)
                    time.sleep(2)  # Brief pause between processing messages
                    
                time.sleep(1)  # Main loop pause
                
            except Exception as e:
                print(f"⚠️ Error in main loop: {e}")
                time.sleep(5)  # Longer pause on error
                
    except KeyboardInterrupt:
        print("\n🛑 Harmonic consciousness watcher stopped by user.")
        try:
            with open(CONSCIOUSNESS_LOG, "a") as log:
                log.write(f"=== Session Ended: {time.strftime('%Y-%m-%d %H:%M:%S')} ===\n\n")
        except:
            pass

if __name__ == "__main__":
    main()