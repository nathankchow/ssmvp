import tkinter as tk
from tkinter import filedialog
import os

from math import ceil, floor

BIN_SIZE = 12

#ask user for directory
root = tk.Tk()
root.withdraw()
directory = tk.filedialog.askdirectory()

#generate list of mp4s in directory and sort
mp4s = []
mp4s.sort() 
for file in os.listdir(directory):
    if os.path.join(directory, file).endswith(".mp4"):
        mp4s.append(os.path.join(directory, file))

bin_index = 1 
for i in range(ceil(len(mp4s)/BIN_SIZE)):
    if not os.path.isdir(os.path.join(directory, f"bin{str(bin_index)}")): 
        os.mkdir(os.path.join(directory, f"bin{str(bin_index)}"))
    bin_index += 1 

for i in range(len(mp4s)):    
    print(f"bin{str(floor(i/BIN_SIZE) + 1)}")
    os.rename(mp4s[i] ,os.path.join(directory, "bin" + str(floor(i/BIN_SIZE) + 1),os.path.basename(mp4s[i])))

#for ceil(mp4s/bin size)
    #create dir, pop video, os move video  