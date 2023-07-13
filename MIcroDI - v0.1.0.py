# This file is part of MIcroDI. 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may use this file in compliance with the License. 
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.

import sys
import mido
from mido import MidiFile
import pretty_midi
import tkinter as tk
from tkinter import filedialog
 # Constants
MICROBIT_TEMPO_TEMPLATE = "music.setTempo({})"
MICROBIT_PAUSE_TEMPLATE = "basic.pause({})"
MICROBIT_TONE_TEMPLATE = "music.ringTone({})"
def extract_midi_info(filename):
    midi = MidiFile(filename)
    tempo_changes = []
    notes = []
    for track in midi.tracks:
        for msg in track:
            if msg.is_meta and msg.type == 'set_tempo':
                tempo_changes.append(mido.tempo2bpm(msg.tempo))
            if not msg.is_meta and msg.type == 'note_on':
                freq = pretty_midi.note_number_to_hz(msg.note)
                notes.append((freq, msg.time))
    return tempo_changes, notes
def convert_to_microbit_code(tempo_changes, notes):
    microbit_code = []
    if tempo_changes:
        microbit_code.append(MICROBIT_TEMPO_TEMPLATE.format(tempo_changes[0]))
    for note, duration in notes:
        rounded_note = round(note)
        microbit_code.append(MICROBIT_TONE_TEMPLATE.format(rounded_note))
        microbit_code.append(MICROBIT_PAUSE_TEMPLATE.format(duration))
    return microbit_code
def choose_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path
def save_to_file(output_text):
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    with open(file_path, "w") as f:
        f.write(output_text)
def main():
    if len(sys.argv) < 2:
        midi_file = choose_file()
    else:
        midi_file = sys.argv[1]
    tempo_changes, notes = extract_midi_info(midi_file)
    microbit_code = convert_to_microbit_code(tempo_changes, notes)
    output_text = "\n".join(microbit_code)
    save_to_file(output_text)
if __name__ == "__main__":
    main()
