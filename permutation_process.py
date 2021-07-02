from classes.vid import Vid
from pathlib import Path
import tkinter.filedialog
import tkinter as tk
import os

def permutation_process(directory=None):
    if directory == None: 
        root = tk.Tk()
        root.withdraw()
        directory = tk.filedialog.askdirectory()

    for file in os.listdir(directory):
        vid = Vid(f'{directory}/{file}')
        vid.v2_pipeline()

    return directory 
        

if __name__ == "__main__":
    permutation_process()
