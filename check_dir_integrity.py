from classes.vid import Vid
from pathlib import Path
import tkinter.filedialog
import tkinter as tk
import os
import sys

def check_dir_integrity(directory=None):
    if directory == None:
        root = tk.Tk()
        root.withdraw()
        directory = tk.filedialog.askdirectory()

    for file in os.listdir(directory):
        vid = Vid(f'{directory}/{file}')
        vid.check_integrity()
        

if __name__ == "__main__":
    check_dir_integrity()


        
