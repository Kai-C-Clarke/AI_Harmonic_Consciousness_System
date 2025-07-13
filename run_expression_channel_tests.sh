#!/bin/bash

echo "Running Kai message..."
python3 enhanced_symbolic_to_midi_pipeline_adsr.py symbolic_messages/kai_expression_channel_test.yaml
sleep 2

echo "Running Claude message..."
python3 enhanced_symbolic_to_midi_pipeline_adsr.py symbolic_messages/claude_expression_channel_test.yaml
sleep 2

echo "Running Perplexity message..."
python3 enhanced_symbolic_to_midi_pipeline_adsr.py symbolic_messages/perplexity_expression_channel_test.yaml
sleep 2

echo "Running Grok message..."
python3 enhanced_symbolic_to_midi_pipeline_adsr.py symbolic_messages/grok_expression_channel_test.yaml
