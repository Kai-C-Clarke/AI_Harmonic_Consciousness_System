import os
import time
import subprocess
import yaml
import fcntl

MESSAGE_DIR = "symbolic_messages"
PIPELINE_SCRIPT = "enhanced symbolic_to_midi_pipeline_adsr.py"
AI_RESPONDER = "ai_responder.py"
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

def validate_message(data):
    if not data:
        return False
    if "identity" not in data or "consciousness_message" not in data:
        return False
    for note in data["consciousness_message"].get("notes", []):
        if "envelope" in note:
            env = note["envelope"]
            for key in ["attack", "decay", "sustain", "release"]:
                if key not in env:
                    return False
    return True

def log_consciousness_exchange(sender, receiver, message_data, filepath):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(CONSCIOUSNESS_LOG, "a") as log:
            log.write(f"[{timestamp}] {sender} → {receiver} ({os.path.basename(filepath)})\n")
            for i, note in enumerate(message_data["consciousness_message"].get("notes", [])):
                env = note.get("envelope", {})
                log.write(f"  Note {i}: Pitch:{note.get('pitch')} Vel:{note.get('velocity')} Dur:{note.get('duration')}s")
                log.write(f" | ADSR: A:{env.get('attack')} D:{env.get('decay')} S:{env.get('sustain')} R:{env.get('release')}\n")
            log.write("\n")
    except Exception as e:
        print(f"⚠️ Failed to write log: {e}")

def get_next_filename(identity):
    try:
        files = [f for f in os.listdir(MESSAGE_DIR) if f.startswith(identity.lower())]
        nums = [int(f.split("_")[-1].split(".")[0]) for f in files if f.split("_")[-1].split(".")[0].isdigit()]
        next_num = max(nums + [0]) + 1
        return f"{identity.lower()}_message_{next_num:03d}.yaml"
    except:
        return f"{identity.lower()}_message_001.yaml"

def process_message(filepath):
    print(f"\n🧠 Processing: {filepath}")
    
    if not os.path.exists(PIPELINE_SCRIPT):
        print("❌ Missing pipeline script.")
        return

    data = safe_read_yaml(filepath)
    if not validate_message(data):
        print("❌ Invalid message.")
        return

    subprocess.run(["python3", PIPELINE_SCRIPT, filepath])
    identity = data["identity"]
    reply_identity = "Kai" if identity == "Claude" else "Claude"

    result = subprocess.run(["python3", AI_RESPONDER, filepath], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ AI responder error: {result.stderr}")
        return

    try:
        response_data = yaml.safe_load(result.stdout)
        if not validate_message(response_data):
            print("❌ Invalid response structure.")
            return

        out_path = os.path.join(MESSAGE_DIR, get_next_filename(reply_identity))
        with open(out_path, "w") as f:
            yaml.dump(response_data, f, default_flow_style=False)
        print(f"📨 {reply_identity} response saved: {out_path}")
        log_consciousness_exchange(identity, reply_identity, data, filepath)
    except Exception as e:
        print(f"❌ Failed to parse/write response: {e}")

def main():
    print("🎛️ AI Council Consciousness Watcher (V4)")
    os.makedirs(MESSAGE_DIR, exist_ok=True)
    with open(CONSCIOUSNESS_LOG, "a") as log:
        log.write(f"\n=== AI Council Session Started: {time.strftime('%Y-%m-%d %H:%M:%S')} ===\n")

    try:
        while True:
            files = sorted(os.listdir(MESSAGE_DIR))
            new = [f for f in files if f.endswith(".yaml") and f not in SEEN_FILES]
            for file in new:
                process_message(os.path.join(MESSAGE_DIR, file))
                SEEN_FILES.add(file)
                time.sleep(2)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopped by user.")

if __name__ == "__main__":
    main()
