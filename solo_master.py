'''
processes a solo song, uploads it to youtube and updates solo songs list with title + id 
'''

from classes.vid import Vid 
from classes.yt import Yt 
import tkinter.filedialog
import tkinter as tk 
import sys
import os
from pathlib import Path 

def solo_master(dir=None):
    
    root = tk.Tk()
    root.withdraw()
    if len(sys.argv) != 2 and dir == None:
        dir = tk.filedialog.askdirectory()
    elif len(sys.argv) == 2:
        dir = sys.argv[1]

    for file in [os.path.join(dir, file) for file in os.listdir(dir)]:
        vid = Vid(file)
        vid.check_integrity() ##debugging
        vid.solo_pipeline()

    for vid in [os.path.join('output', file) for file in os.listdir('output')]:
        os.rename(vid, os.path.join(dir,Path(vid).name))

if __name__ == "__main__":
    solo_master()