from flask import Flask, request, send_file, jsonify
import yaml
from mido import MidiFile, MidiTrack, Message, MetaMessage
import io

app = Flask(__name__)

@app.route('/api/generate-midi', methods=['POST'])
def generate_midi():
    try:
        yaml_data = request.data.decode('utf-8')
        data = yaml.safe_load(yaml_data)

        mid = MidiFile()
        tempo_bpm = data.get('tempo', 120)
        tempo_us = int(60_000_000 / tempo_bpm)

        track = MidiTrack()
        mid.tracks.append(track)

        # Tempo and time signature
        track.append(MetaMessage('set_tempo', tempo=tempo_us))
        if 'time_signature' in data:
            num, denom = data['time_signature']
            track.append(MetaMessage('time_signature', numerator=num, denominator=denom))

        # Tracks
        for t in data.get('tracks', []):
            channel = t.get('channel', 0)
            program = t.get('program', 0)
            track.append(Message('program_change', program=program, channel=channel, time=0))

            for note in t.get('notes', []):
                note_val = note.get('note', 60)
                velocity = note.get('velocity', 64)
                start = int(note.get('start', 0) * 480)
                duration = int(note.get('duration', 1) * 480)

                track.append(Message('note_on', note=note_val, velocity=velocity, time=start, channel=channel))
                track.append(Message('note_off', note=note_val, velocity=0, time=duration, channel=channel))

        # Save to memory
        output = io.BytesIO()
        mid.save(file=output)
        output.seek(0)

        return send_file(output, as_attachment=True, download_name='melody_scribe.mid', mimetype='audio/midi')

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(port=5000)
