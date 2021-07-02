from classes.vid import Vid
import tkinter.filedialog
import tkinter as tk 
import os
import cv2
import sys

def permutation_rename():
    #ask user to specify song name, along with number of singers 
    if len(sys.argv) != 4:
        songname = input('Please specify the song name:\n')
        singers = input('Please specify the number of singers:\n')
        print('Please specify the directory:')
        root = tk.Tk()
        root.withdraw()
        directory = tk.filedialog.askdirectory()

        print(f'Song name: {songname}\nNumber of singers: {singers}\nDirectory: {directory}\n')
        input('Press enter to continue...')
    
    #settings
    order = [2,1,3,0,4]
    x_list = [400, 662, 925, 1187, 1450] 
    h = 50
    y = 500 

    def crop_to_idol(crop):
        idols = ['arisu','koharu','yoshino','yumi','yukimi']
        templates = [
        cv2.imread('data/template/arisu.png'),
        cv2.imread('data/template/koharu.png'),
        cv2.imread('data/template/yoshino.png'),
        cv2.imread('data/template/yumi.png'),
        cv2.imread('data/template/yukimi.png')
        ]
        err_best = 999999999 
        i = 0 #keep a manual counter since index on cv2.im objects is iffy 
        for template in templates:
            err = Vid.mse(crop,template)
            if err < err_best:
                err_best = err
                name = idols[i]
            i += 1
        return name 

    for vid in os.listdir(directory):
        crops = []
        vidcap = cv2.VideoCapture(os.path.join(directory,vid))
        success,image = vidcap.read()
        vidcap.release()
        for i in range(0,int(singers)):
            crop = image[y:y+h,x_list[order[i]]:x_list[order[i]]+h]
            crops.append((order[i],crop)) #tuple containing location and cropped img object
        crops.sort(key=lambda x:x[0]) #sort list by idol order
        idols = []
        for crop in crops:
            idols.append(crop_to_idol(crop[1]))
        assert len(idols) == len(set(idols)), 'duplicate of idol found.'
        new_filename = os.path.join(directory,f"[デレステ] {songname} {'-'.join(idols)}.mp4")
        if not os.path.exists(new_filename):
            os.rename(os.path.join(directory,vid),new_filename)
        elif new_filename == os.path.join(directory,vid):
            pass
        elif os.path.exists(new_filename):
            raise ValueError

    return directory 

if __name__ == '__main__':
    permutation_rename()



