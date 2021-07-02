from classes.vid import Vid
import os

def batch_mp4_to_mkv(src='output'):
    for file in os.listdir('output'):
        if file.lower().endswith('mp4'):
            vid = Vid(os.path.join("output",file))
            vid.mp4tomkv(os.path.join("output",file.split('.')[0] + ".mkv"))


if __name__ == '__main__':
    batch_mp4_to_mkv()
