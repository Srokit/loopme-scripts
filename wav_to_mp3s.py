import sys
import os
from pydub import AudioSegment

in_dir = sys.argv[1]
out_dir = sys.argv[2]

for f in os.listdir(in_dir):
    if not f.endswith('.wav'):
        continue
    fpath = os.path.join(in_dir, f)
    seg = AudioSegment.from_wav(fpath)
    f_without_end = f[:f.index('.wav')]
    outpath = os.path.join(out_dir, f_without_end + '.mp3')
    seg.export(outpath, format='mp3')
