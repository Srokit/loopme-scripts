"Clean and move all loop files from after scraping from splice"
import os
import re
import sys

from pydub import AudioSegment
from random_word import RandomWords

def get_all_filenames_from_dir(input_dir):
    fns = []
    print('getall')
    for (root, _, filenames) in os.walk(input_dir):
        print(filenames)
        fns.extend(os.path.join(root, fn) for fn in filenames if fn.endswith('.wav'))
    return fns

def trim_to_smaller_time(segment, new_dur_in_secs):
    # Each segment section is 1 ms
    return segment[:int(new_dur_in_secs * 1000.0)]

def make_new_filename(tempo, name, key):
    return '{}_{}_{}.wav'.format(name, tempo, key)

def get_tempo(filename):
    # Just return first consecutive digits found
    minus_end = filename[:filename.index('.wav')]
    res = re.search('\d+', minus_end)
    if res is None:
        return None
    nums = res.group()
    if nums.startswith('0'):
        return None
    temp_int = int(nums)
    # Too slow or too fast mean prob didn't parse proper
    if temp_int < 70 or temp_int > 170:
        return None
    return nums

def get_random_name():
    r = RandomWords()
    return r.get_random_word().capitalize() + r.get_random_word().capitalize()

def get_key(file):
    # Look for common ways to abrev key
    minus_end = file[:file.index('.wav')]
    res = re.search('[A-G](b|#)?(min|maj|m)?', minus_end)
    if res is None:
        return None
    key = res.group()
    return clean_key(key)

def one_tone_down(orig_key):
    mapping = {
        'A': 'G',
        'B': 'A',
        'C': 'B',
        'D': 'C',
        'E': 'D',
        'F': 'E',
        'G': 'F',
    }
    return mapping[orig_key]

def clean_key(key):
    letter = key[0]
    final_seq = []
    non_mode_end = len(key)
    if 'm' in key:
        non_mode_end = key.index('m')
    not_mode_part = key[:non_mode_end]
    if len(not_mode_part) == 2 and not_mode_part[1] == 'b':
        letter = one_tone_down(letter)
    final_seq.append(letter)
    if len(not_mode_part) == 2:
        final_seq.append('#')
    mode_part = key[non_mode_end:]
    if mode_part == 'maj':
        mode_part = ''
    elif mode_part == 'min':
        mode_part = 'm'
    final_seq.extend(list(mode_part))
    return ''.join(final_seq)



def handle_file(file, output_dir):
    filebase = os.path.basename(file)
    tempo = get_tempo(filebase)
    name = get_random_name()
    key = get_key(filebase)
    if tempo is None or name is None or key is None:
        # If can't figure out the naming just skip file
        print("Skipping file '{}' because couldn't find info".format(filebase))
        return
    duration_in_secs = (60.0 / float(tempo)) * 4.0 * 8.0 # 8 bars of music
    seg = AudioSegment.from_wav(file)
    seg = trim_to_smaller_time(seg, duration_in_secs)
    new_fn = make_new_filename(tempo, name, key)
    seg.export(os.path.join(output_dir, new_fn), format='wav')


def main():
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    files = get_all_filenames_from_dir(input_dir)
    print(files)
    for f in files:
        print('f')
        handle_file(f, output_dir)

if __name__ == '__main__':
    main()