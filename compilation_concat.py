import os
from moviepy.editor import VideoFileClip
import datetime
import time
import os.path
from os import path
import sys
import openpyxl
import copy
import subprocess
def compilation_concat():

    outputdir = 'output' 

    def initialize_songlist(return_num_singers = False):
        workbook = 'data/songlist.xlsx'
        wb = openpyxl.load_workbook(workbook)
        sheetname = wb.sheetnames[0] #make sure the very first sheet contains wanted data
        sheet = wb[sheetname]
        songlist = []
        number_of_singers = []
        i = 2
        while sheet['A%s'%i].value != None:
            songlist.append(sheet['A%s'%i].value)
            number_of_singers.append(sheet['B%s'%i].value)
            i += 1
        if return_num_singers == True:
            return songlist, number_of_singers
        else:
            return songlist

    songlist = initialize_songlist()
    print(songlist)

    video_default_order = []
    videos = [video for video in os.listdir(outputdir) if video.lower().endswith('.mkv')]
    print(videos)

    while len(videos) != 0: #loop a second time around to account for duo songs
        print(len(videos))
        for song in songlist:
            for video in videos:
                if video.lower().endswith('mkv'):
                    if song == video.rsplit('.',1)[0].split(',')[-1]:
                        video_default_order.append(video)
                        videos.remove(video)
                        break

    names=[]
    durations = []
    timestamps = []
    summation = 0

    with open(outputdir + '\\mylist.txt',mode = 'w+',encoding = 'utf-8') as text_file:
        filelist = copy.deepcopy(video_default_order)
        filelist = [f"file '{file}'" for file in filelist]
        string = '\n'.join(filelist)
        text_file.write(string)

    for video in video_default_order: #make sure there is only mkv
        if video.lower().endswith('mkv'):      
            clip = VideoFileClip(outputdir + '/' + video)
            names.append(video)
            timestamps.append(summation)
            durations.append(clip.duration)
            summation += durations[-1]
            clip.close()

    ts_int = list(map(int,timestamps))
    ts_real = ['0' + str(datetime.timedelta(seconds = i)) for i in ts_int]

    txt = ''
    for i in range(len(names)):
        if '-' not in names[0].split(',',1)[0]:
            txt = txt + f'{ts_real[i]} - {names[i].rsplit(".",1)[0].split(",")[1]}\n'
        else: #for duo songs
            txt = txt + f'{ts_real[i]} - {names[i].rsplit(".",1)[0].replace(","," ")}\n'
        

    with open('C:/users/natha/desktop/timestamps.txt',mode = 'w+',encoding = 'utf-8') as text_file:
        text_file.write(txt)


    subprocess.run(f'ffmpeg -f "concat" -safe 0 -i "{outputdir}/mylist.txt" -codec:v "libx264" -filter:v fps=fps=60.000 -crf:v 18 -preset:v "superfast" -tune:v "film" -profile:v "high" -codec:a "aac" -movflags "+faststart" C:/users/natha/desktop/output_superfast18.mkv')
    #os.remove(f"{outputdir}/mylist.txt")
    subprocess.run(
        f'ffmpeg -y -i C:/users/natha/desktop/output_superfast18.mkv -c:v copy -c:a aac -metadata:s:v:0 rotate=90 C:/users/natha/desktop/output_final.mp4'
        )
        
if __name__ == "__main__":
    compilation_concat()



