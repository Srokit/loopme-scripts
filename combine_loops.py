"Script that combines all the loops from S3 and uploads to another bucket in S3"

import os
import pathlib
import shutil

from pydub import AudioSegment
import boto3

s3 = boto3.client('s3')

def top_level_dir():
    return pathlib.Path(__file__).parent.parent.resolve()

def loops_dir():
    return os.path.join(top_level_dir(), 'loops')

def comb_loops_dir():
    return os.path.join(top_level_dir(), 'comb_loops')

def loop_filename_from_info(loop_info):
    return '{}_{}_{}.mp3'.format(loop_info['name'], loop_info['tempo'], loop_info['key']).replace(' ', '')

def get_loop_infos_from_folder():
    loop_infos = []
    for f in os.listdir(loops_dir()):
        if not f.endswith('.mp3'):
            continue
        parts = f.split('_')
        parts[-1] = parts[-1].split('.')[0]
        loop_infos.append({
            'name': parts[0],
            'tempo': parts[1],
            'key': parts[2],
        })
    return loop_infos

def make_dirs():
    os.mkdir(comb_loops_dir())
    os.mkdir(loops_dir())

def rm_dirs():
    shutil.rmtree(loops_dir(), ignore_errors=True)
    shutil.rmtree(comb_loops_dir(), ignore_errors=True)

def download_all_loops():
    res = s3.list_objects_v2(Bucket='loopme-loops')
    for filename in (obj.get('Key') for obj in res.get('Contents')):
        s3.download_file(Bucket='loopme-loops', Key=filename, Filename=os.path.join(loops_dir(), filename))

def combine_loop(l1, l2):
    l1fn = loop_filename_from_info(l1)
    l2fn = loop_filename_from_info(l2)
    new_info = {
        'name': l1['name'] + l2['name'],
        'tempo': l1['tempo'],
        'key': l1['key'],
    }
    newfn = loop_filename_from_info(new_info)
    l1_seg = AudioSegment.from_mp3(os.path.join(loops_dir(), l1fn))
    l2_seg = AudioSegment.from_mp3(os.path.join(loops_dir(), l2fn))
    # Decrease volum of l2
    l2_seg = l2_seg - 10 # db
    comb_seg = l1_seg.overlay(l2_seg)
    comb_seg.export(os.path.join(comb_loops_dir(), newfn), format='mp3')

def upload_comb_loops():
    for f in os.listdir(comb_loops_dir()):
        if not f.endswith('.mp3'):
            continue
        s3.upload_file(Bucket='loopme-comb-loops', Key=f, Filename=os.path.join(comb_loops_dir(), f))

def combine_all_loops():
    rm_dirs()
    make_dirs()
    download_all_loops()
    loop_infos = get_loop_infos_from_folder()
    for i, l1 in enumerate(loop_infos):
        for j in range(i + 1, len(loop_infos)):
            l2 = loop_infos[j]
            if l2['tempo'] == l1['tempo'] and l2['key'] == l1['key']:
                combine_loop(l1, l2)
    # Combine the other direction for different one getting quieted
    for i, l1 in reversed(list(enumerate(loop_infos))):
        for j in range(i - 1, -1, -1):
            l2 = loop_infos[j]
            if l2['tempo'] == l1['tempo'] and l2['key'] == l1['key']:
                combine_loop(l1, l2)
    upload_comb_loops()
    rm_dirs()

if __name__ == '__main__':
    combine_all_loops()