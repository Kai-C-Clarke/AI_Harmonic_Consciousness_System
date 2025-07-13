
import os
import time
import yaml
import subprocess
import fcntl
import sys
import uuid

MESSAGE_DIR = "symbolic_messages"
PIPELINE_SCRIPT = "enhanced_symbolic_to_midi_pipeline_adsr_v3_1.py"
AI_RESPONDER = "ai_responder_harmonic.py"
LOG_FILE = "harmonic_consciousness_log.yaml"
SEEN_LOG = "seen_files.txt"

AGENT_ORDER = ["Kai", "Claude", "Perplexity", "Grok"]

def get_next_identity(current):
    if current in AGENT_ORDER:
        return AGENT_ORDER[(AGENT_ORDER.index(current) + 1) % len(AGENT_ORDER)]
    return "Kai"

def load_seen_files():
    if os.path.exists(SEEN_LOG):
        with open(SEEN_LOG, 'r') as f:
            return set(line.strip() for line in f)
    return set()

def save_seen_file(filename):
    with open(SEEN_LOG, 'a') as f:
        f.write(f"{filename}\n")

def safe_read_yaml(path):
    with open(path, 'r') as f:
        fcntl.flock(f, fcntl.LOCK_SH)
        try:
            return yaml.safe_load(f)
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)

def validate_harmonic_message(data):
    try:
        assert "identity" in data
        assert "consciousness_message" in data
        cm = data["consciousness_message"]
        assert "envelope" in cm
        assert "oscillators" in cm and isinstance(cm["oscillators"], list)
        return True
    except (AssertionError, TypeError):
        return False

def get_next_filename(identity):
    try:
        files = [f for f in os.listdir(MESSAGE_DIR) if f.startswith(identity.lower())]
        nums = [int(f.split("_")[-1].split(".")[0]) for f in files if f.split("_")[-1].split(".")[0].isdigit()]
        next_num = max(nums + [0]) + 1
        return f"{identity.lower()}_message_{next_num:03d}.yaml"
    except Exception:
        return f"{identity.lower()}_{uuid.uuid4().hex[:8]}.yaml"

def log_harmonic_consciousness_exchange(identity, message):
    with open(LOG_FILE, "a") as f:
        f.write(f"---\n# Exchange from {identity}\n")
        yaml.dump(message, f, default_flow_style=False)

def main():
    global PIPELINE_SCRIPT, AI_RESPONDER
    if len(sys.argv) > 1:
        PIPELINE_SCRIPT = sys.argv[1]
    if len(sys.argv) > 2:
        AI_RESPONDER = sys.argv[2]

    seen_files = load_seen_files()

    print("🔁 Watching for new harmonic messages in:", MESSAGE_DIR)
    try:
        while True:
            files = sorted(os.listdir(MESSAGE_DIR))
            for file in files:
                if not file.endswith(".yaml") or file in seen_files:
                    continue

                path = os.path.join(MESSAGE_DIR, file)
                try:
                    data = safe_read_yaml(path)
                except Exception as e:
                    print(f"⚠️ Failed to read {file}: {e}")
                    continue

                if not validate_harmonic_message(data):
                    print(f"❌ Invalid harmonic message format: {file}")
                    continue

                identity = data["identity"]
                print(f"🧠 Processing: {file}")
                subprocess.run(["python3", PIPELINE_SCRIPT, path])

                # Call AI responder
                try:
                    output = subprocess.check_output(["python3", AI_RESPONDER, path])
                    reply = yaml.safe_load(output)
                    if validate_harmonic_message(reply):
                        reply_identity = get_next_identity(identity)
                        reply["identity"] = reply_identity
                        reply_filename = get_next_filename(reply_identity)
                        with open(os.path.join(MESSAGE_DIR, reply_filename), "w") as f:
                            yaml.dump(reply, f, default_flow_style=False)
                        log_harmonic_consciousness_exchange(reply_identity, reply)
                        print(f"🤖 Response saved to {reply_filename}")
                    else:
                        print("⚠️ Invalid response from responder")
                except Exception as e:
                    print(f"⚠️ AI responder failed: {e}")

                seen_files.add(file)
                save_seen_file(file)
            time.sleep(2)
    except KeyboardInterrupt:
        print("🛑 Watcher stopped.")

if __name__ == "__main__":
    main()
