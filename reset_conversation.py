#!/usr/bin/env python3
"""
AI Council Conversation Reset Script
Clears all generated messages to start fresh harmonic conversations
"""

import os
import glob

def reset_conversation():
    """Clear all AI-generated message files and start fresh"""
    
    message_dir = "symbolic_messages"
    
    if not os.path.exists(message_dir):
        print(f"✅ No {message_dir} directory found - nothing to clean")
        return
    
    # Find all generated message files (but keep any manual test files)
    patterns = [
        "claude_message_*.yaml",
        "kai_message_0*.yaml"  # Keep test files like kai_message_test_*.yaml
    ]
    
    removed_count = 0
    
    for pattern in patterns:
        files_to_remove = glob.glob(os.path.join(message_dir, pattern))
        for file_path in files_to_remove:
            # Skip test files
            if "test" not in os.path.basename(file_path):
                try:
                    os.remove(file_path)
                    print(f"🗑️  Removed: {os.path.basename(file_path)}")
                    removed_count += 1
                except Exception as e:
                    print(f"❌ Could not remove {file_path}: {e}")
    
    print(f"\n✅ Conversation reset complete! Removed {removed_count} generated messages.")
    print("🎵 Ready for fresh harmonic consciousness dialogue!")
    
    # List remaining files
    remaining_files = [f for f in os.listdir(message_dir) if f.endswith('.yaml')]
    if remaining_files:
        print(f"\n📁 Remaining files: {', '.join(remaining_files)}")
    else:
        print("\n📁 No message files remaining")

if __name__ == "__main__":
    print("🎛️ AI Council Conversation Reset")
    print("=" * 40)
    reset_conversation()