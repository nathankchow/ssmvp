from classes.vid import Vid
import tkinter.filedialog
import tkinter as tk 
import os
import cv2
import sys


def permutation_rename(confirm=True):
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
    else:
        songname = sys.argv[1]
        singers = int(sys.argv[2])
        directory = sys.argv[3]
        if confirm == True:
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
        try_reverse = False
        crops = []
        vidcap = cv2.VideoCapture(os.path.join(directory,vid))
        success,image = vidcap.read()
        if Vid.mvcompare(cv2.resize(image, (1600,900))) > 1500:
            i = 0 
            jump = 0
            while True:
                jump += 1000
                vidcap.set(cv2.CAP_PROP_POS_MSEC,jump)
                success,image = vidcap.read()
                if Vid.mvcompare(cv2.resize(image, (1600,900))) < 1500:
                    break
                elif i == 15:
                    try_reverse = True
                    break
                i += 1
        if try_reverse:
            i = 0 
            jump = 0
            while True:
                jump += 1000
                vidcap.set(cv2.CAP_PROP_POS_MSEC,jump)
                success,image = vidcap.read()
                image = cv2.rotate(image, cv2.ROTATE_180) #try flipping?
                # cv2.imshow("flipping did happen", image)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
                if Vid.mvcompare(cv2.resize(image, (1600,900))) < 1500:
                    break
                elif i == 15:
                    raise Exception("flipping doesnt work ig")
                i += 1

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
            print(f'{vid} renamed to {new_filename}')
        elif new_filename == os.path.join(directory,vid):
            print(f"no change in naming of {new_filename}")
        elif os.path.exists(new_filename):
            print(f"{new_filename} already exists, duplicate video. no renaming was performed.")
            
        

    return directory 

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

if __name__ == '__main__':
    permutation_rename()



