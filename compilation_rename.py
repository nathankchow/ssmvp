import os
import tkinter.filedialog
import tkinter as tk
import itertools
import openpyxl

def generate_video_name_list(name1,name2):
    pass

def compilation_rename():
    #change directory to folder containing vids
    root = tk.Tk()
    root.withdraw()
    directory = tk.filedialog.askdirectory()
    os.chdir(directory)
    print(directory)

    #ask user for name of idols
    default_idol_names= ['arisu','koharu','yoshino','yukimi','yumi']
    idol_names = []
    print(f'Use default names (y/n)? {default_idol_names}\n')
    answer = input()
    if answer == 'y':
        idol_names = default_idol_names
    elif answer == 'n':
        print('Enter idol names in alphabetical order, followed by "end".')
        while True:
            idol_name = input()
            if idol_name != 'end':
                idol_names.append(idol_name)
            else:
                break
    elif answer != 'n':
        raise Exception('Unexpected answer')

    print(idol_names)

    #ask user for song name
    song_name = input('Please input song name.\n')

    #get list of videos in directory, sorted by date created
    filelist = sorted([f'{file}' for file in os.listdir() if file.lower().endswith('.mp4')], key = os.path.getmtime)

    #get list of permutations
    permutations = list(itertools.permutations(idol_names))

    #make sure number of permunations is equal to number of videos
    if len(filelist) == 120:
        new_filenames = [f'[デレステ] {song_name} {"-".join(permutation)}.mp4' for permutation in permutations]
    elif len(filelist) == 23:
        preset60 = [
            ['koharu', 'yoshino', 'yukimi'],
            ['koharu', 'yoshino', 'yumi'],
            ['koharu', 'yukimi', 'yoshino'],
            ['koharu', 'yukimi', 'yumi'],
            ['koharu', 'yumi', 'yoshino'],
            ['koharu', 'yumi', 'yukimi'],
            ['yoshino', 'koharu', 'yukimi'],
            ['yoshino', 'koharu', 'yumi'],
            ['yoshino', 'yukimi', 'koharu'],
            ['yoshino', 'yukimi', 'yumi'],
            ['yoshino', 'yumi', 'koharu'],
            ['yoshino', 'yumi', 'yukimi'],
            ['yukimi', 'koharu', 'yoshino'],
            ['yukimi', 'koharu', 'yumi'],
            ['yukimi', 'yoshino', 'koharu'],
            ['yukimi', 'yoshino', 'yumi'],
            ['yukimi', 'yumi', 'koharu'],
            ['yukimi', 'yumi', 'yoshino'],
            ['yumi', 'koharu', 'yoshino'],
            ['yumi', 'koharu', 'yukimi'],
            ['yumi', 'yoshino', 'koharu'],
            ['yumi', 'yoshino', 'yukimi'],
            ['yumi', 'yukimi', 'koharu'],
            ['yumi', 'yukimi', 'yoshino'],
            ['arisu', 'yoshino', 'yukimi'],
            ['arisu', 'yoshino', 'yumi'],
            ['arisu', 'yukimi', 'yoshino'],
            ['arisu', 'yukimi', 'yumi'],
            ['arisu', 'yumi', 'yoshino'],
            ['arisu', 'yumi', 'yukimi'],
            ['yoshino', 'arisu', 'yukimi'],
            ['yoshino', 'arisu', 'yumi'],
            ['yoshino', 'yukimi', 'arisu'],
            ['yoshino', 'yumi', 'arisu'],
            ['yukimi', 'arisu', 'yoshino'],
            ['yukimi', 'arisu', 'yumi'],
            ['yukimi', 'yoshino', 'arisu'],
            ['yukimi', 'yumi', 'arisu'],
            ['yumi', 'arisu', 'yoshino'],
            ['yumi', 'arisu', 'yukimi'],
            ['yumi', 'yoshino', 'arisu'],
            ['yumi', 'yukimi', 'arisu'],
            ['arisu', 'koharu', 'yukimi'],
            ['arisu', 'koharu', 'yumi'],
            ['arisu', 'yukimi', 'koharu'],
            ['arisu', 'yumi', 'koharu'],
            ['koharu', 'arisu', 'yukimi'],
            ['koharu', 'arisu', 'yumi'],
            ['koharu', 'yukimi', 'arisu'],
            ['koharu', 'yumi', 'arisu'],
            ['yukimi', 'arisu', 'koharu'],
            ['yukimi', 'koharu', 'arisu'],
            ['yumi', 'arisu', 'koharu'],
            ['yumi', 'koharu', 'arisu'],
            ['arisu', 'koharu', 'yoshino'],
            ['arisu', 'yoshino', 'koharu'],
            ['koharu', 'arisu', 'yoshino'],
            ['koharu', 'yoshino', 'arisu'],
            ['yoshino', 'arisu', 'koharu'],
            ['yoshino', 'koharu', 'arisu']
                    ]
        with open('C:/users/natha/desktop/temp.txt',encoding='utf-8') as f:
            txt = f.read()
            preset60 = txt.split('\n')
        new_filenames = [f'{permutation}.mp4' for permutation in preset60]
        
    #rename
    for video_file in filelist:
        os.rename(video_file, new_filenames[filelist.index(video_file)])
    return directory

if __name__ == '__main__':
    compilation_rename()


