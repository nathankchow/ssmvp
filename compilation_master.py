import tkinter.filedialog
import tkinter as tk
import os
import openpyxl
from permutation_process import permutation_process
from compilation_concat import compilation_concat
from batch_mp4_to_mkv import batch_mp4_to_mkv

def compilation_master():

    def generate_vid_namelist(name1,name2):
        #sample name kozue-yumi,(Shiki-Asuka),バベル.mkv 
        workbook = 'data/songlist.xlsx'
        wb = openpyxl.load_workbook(workbook)
        sheetname = wb.sheetnames[0] #make sure the very first sheet contains wanted data
        assert (sheetname=='duos'), "Excel sheet may have been updated, please double check."
        sheet = wb[sheetname]
        i = 2 
        namelist = []
        while sheet['A%s'%i].value != None:
            namelist.append(f'{name1}-{name2},({sheet[f"C{i}"].value}),{sheet[f"A{i}"].value}')
            i += 1
        return namelist
    
    def rename_videos(dir, namelist): #assumes videos were recorded in standard order 
        assert (len(os.listdir(dir)) == len(namelist)), 'Number of files in directory is not equal to number of names in name list.'
        filelist = sorted([os.path.join(dir,file) for file in os.listdir(dir) if file.lower().endswith('.mp4')], key = os.path.getmtime)
        results = zip(filelist,namelist)
        for result in results:
            os.rename(result[0],os.path.join(dir, result[1] + '.mp4'))
    
    #1. enter name of two idols, and specify two directories containing videos for the two sets
    root = tk.Tk()
    root.withdraw()
    dir1 = tk.filedialog.askdirectory()
    dir2 = tk.filedialog.askdirectory()
    name1 = input('Please enter the name of the left idol in dir1.\n')
    name2 = input('Please enter the name of the right idol in dir1.\n')

    #2. rename videos
    list1 = generate_vid_namelist(name1,name2)
    list2 = generate_vid_namelist(name2,name1)
    rename_videos(dir1,list1)
    rename_videos(dir2,list2)

    #3. process videos
    permutation_process(dir1)
    permutation_process(dir2) 

    #4. concatenate, and rotate if enough space is available (~15 GB per file) 
    batch_mp4_to_mkv()
    compilation_concat()

if __name__ == '__main__':
    compilation_master()