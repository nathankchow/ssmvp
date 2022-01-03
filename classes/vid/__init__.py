import os
import numpy as np
import cv2
import difflib
import subprocess
import time
from PIL import Image
from pathlib import Path
import sys
import openpyxl
import pytesseract

#bug: souyoku no aria read from one of the videos, can find in output directort 

class Vid:
    fudge = 2 #delay start of trimmed video by this amount of time (seconds)
    def __init__(self, filedir, start = None, end = None, songname = None,
                  idolname = None):
        self.filedir = filedir
        self.start = start
        self.rough_end = None
        self.end = end
        self.songname = songname
        self.idolname = idolname
        self.rotation_metadata = None

        
    def mkvtomp4(self):
        subprocess.run(
                f'ffmpeg -y -i temp/temp_output.mkv ' + f'-c:v copy -c:a aac -metadata:s:v:0 rotate={str(self.rotation_metadata)} temp/output_final.mp4'
                )

    def set_rotation_metadata(self):
        os.system(
            f'ffprobe -show_data -show_streams "{self.filedir}" > temp/probe_output.txt'
        ) #subprocess.run raises error, unknown reason 
        with open('temp/probe_output.txt') as f:
            txt = f.read()
        if 'rotation=-90' in txt:
            self.rotation_metadata = -90
        elif 'rotation=90' in txt:
            self.rotation_metadata = 90

    @staticmethod
    def empty_temp_folder():
        for file in os.listdir('temp'):
            os.remove(f'temp/{file}')


    @staticmethod
    def showimage(cv2img, label = ''):
        cv2.imshow(label,cv2img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @staticmethod
    def mse(imageA, imageB): 
        # the 'Mean Squared Error' between the two images is the
        # sum of the squared difference between the two images;
        # NOTE: the two images must have the same dimension
        err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
        err /= float(imageA.shape[0] * imageA.shape[1])
        # return the Vid.mse, the lower the error, the more "similar"
        # the two images are
        return err

    @staticmethod 
    def mvcompare(image):
    #takes as input a (1600,900,3) np array and compares to mv.jpg, returning Vid.mse 
        img1 = cv2.imread('data/mv.jpg')
        img2 = image 
        img2 = img2[111:147,163:243]
        return Vid.mse(img1,img2)

    @staticmethod
    def loadingcompare(image):
    #takes as input a (1600,900,3) np array and compares to loading.jpg, returning Vid.mse
        img1 = cv2.imread('data/loading.jpg')
        img2 = image 
        img2 = img2[0:500,0:100]
        return Vid.mse(img1,img2)
    
    def find_songname(self, method='ocr', find_solo_idol = False):
        if self.songname == None:  
            if method == 'ocr':
                workbook = 'data/songlist.xlsx'
                wb = openpyxl.load_workbook(workbook)
                sheetname = wb.sheetnames[0] #make sure the very first sheet contains wanted data
                sheet = wb[sheetname]
                songlist = []
                number_of_singers = []
                comments = []
                i = 2
                while sheet['A%s'%i].value != None:
                    songlist.append(sheet['A%s'%i].value)
                    number_of_singers.append(sheet['B%s'%i].value)
                    comments.append(sheet[f'D{i}'].value)
                    i += 1

                file_path = self.filedir
                vidcap = cv2.VideoCapture(file_path)
                success, image = vidcap.read()
                #find name of song
                jump = 100
                err_mv = 9E9
                while err_mv > 1500:
                    jump = jump + 500
                    vidcap.set(cv2.CAP_PROP_POS_MSEC,jump)
                    success,image = vidcap.read()
                    if image.shape[0] > image.shape[1]: #image can be oriented differently depending on video encoding 
                        image = cv2.rotate(image,cv2.ROTATE_90_COUNTERCLOCKWISE)
                    image = cv2.resize(image,(1600,900)) #rotating image for ease of troubleshooting
                    err_mv = Vid.mvcompare(image)
                songcrop = image[162:200,245:1083]
                bin_img = cv2.cvtColor(songcrop, cv2.COLOR_BGR2GRAY)
                #other image pre-processing options below
                ###ret, bin_img = cv2.threshold(songcrop, 0, 255,cv2.THRESH_BINARY,cv2.THRESH_OTSU)
                ###bin_img = cv2.adaptiveThreshold(songcrop,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
                img = Image.fromarray(bin_img)
                txt = pytesseract.image_to_string(img, lang = 'jpn',config='--psm 7')
                if txt == '\x0c':
                    txt = '楽園' #with current img pre-processing scheme, 楽園 is the only song that cannot be read by tesseeract
                highest = -1
                song_name = ''  #use string similarity to compare detected string with names of all known songs 
                for song in songlist:
                    if difflib.SequenceMatcher(None, txt, song).ratio() > highest:
                        song_name = song
                        highest = difflib.SequenceMatcher(None, txt, song).ratio()
                self.songname = song_name 
                if find_solo_idol == True:
                    def mid_crop(crop):
                        _ = cv2.resize(crop, (1920,1080))
                        return _[500:550, 925:975]
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
                    self.solo_name = crop_to_idol(mid_crop(image))

                vidcap.release()
 
    def jumpSearch(self,file_path,jump,func,tolerance=100,mode = 'in', direction = 1, stepSize = 1,
               start = None ,stepback = False, debug = False):
        '''
        takes an initial time (jump[seconds]) as input, and marches constantly (direction[1 or -1]) * (stepSize) seconds 
        looking "towards" (mode = 'in') or "away from" (mode = 'out')
        a template picture specified by func located inside the video file
        (e.g func = loadingcompare, func = mvcompare). When the target is reached, can either return
        the final time (default), or the time one step before the target was reached (stepback = True).
        mode = "endIn" is a special case that is more resource intensive than 'in', but is integral for
        finding the end duration of the trimmed video 
        '''
        step = direction * stepSize
        if mode == 'in':
            err = 9E9 #dummy value
            while err > tolerance:
                jump = round(jump + step,3)
                subprocess.run(f'ffmpeg -ss {jump} -i {file_path} -to 5.0 -c copy temp\\temp.mkv')
                vidcap2 = cv2.VideoCapture('temp\\temp.mkv')
                success, image = vidcap2.read()
                if self.rotation_metadata == 90: 
                    image = cv2.rotate(image,cv2.ROTATE_90_COUNTERCLOCKWISE)
                elif self.rotation_metadata == -90: 
                    image = cv2.rotate(image,cv2.ROTATE_90_CLOCKWISE)
                else:
                    image = cv2.rotate(image,cv2.ROTATE_90_COUNTERCLOCKWISE)
                image = cv2.resize(image,(1600,900))
                err = func(image)
                if debug == True:
                    Vid.showimage(image,str(err.tolist()))
                vidcap2.release()
                os.remove('temp\\temp.mkv')
        elif mode == 'out':
            err = 0 #dummy value
            while err <= tolerance:
                jump = round(jump + step,3)
                subprocess.run(f'ffmpeg -ss {jump} -i {file_path} -to 5.0 -c copy temp\\temp.mkv')
                vidcap2 = cv2.VideoCapture('temp\\temp.mkv')
                success, image = vidcap2.read()
                if self.rotation_metadata == 90: 
                    image = cv2.rotate(image,cv2.ROTATE_90_COUNTERCLOCKWISE)
                elif self.rotation_metadata == -90: 
                    image = cv2.rotate(image,cv2.ROTATE_90_CLOCKWISE)
                else:
                    image = cv2.rotate(image,cv2.ROTATE_90_COUNTERCLOCKWISE)
                image = cv2.resize(image,(1600,900))
                err = func(image)
                if debug == True:
                    Vid.showimage(image,str(err.tolist()))
                vidcap2.release()
                os.remove('temp\\temp.mkv')
        elif mode == 'endIn':
            err = 9E9 #dummy value
            while err > tolerance:
                jump = round(jump + step,3)
                subprocess.run(f'ffmpeg -ss {start} -i {file_path} -t {jump-start} -c copy temp\\temp.mkv')
                subprocess.run(f'ffmpeg -sseof -3 -i temp\\temp.mkv -update 1 -q:v 1 ' +
                            f'temp\\temp.jpg')
                if debug == True:
                    print(f'ffmpeg -sseof -3 -i temp\\temp.mkv -update 1 -q:v 1 ' +
                            f'temp\\temp.jpg')
                    input('after jpg conversion')
                image = cv2.imread('temp\\temp.jpg')
                if self.rotation_metadata == 90: 
                    image = cv2.rotate(image,cv2.ROTATE_90_COUNTERCLOCKWISE)
                elif self.rotation_metadata == -90: 
                    image = cv2.rotate(image,cv2.ROTATE_90_CLOCKWISE)
                else:
                    image = cv2.rotate(image,cv2.ROTATE_90_COUNTERCLOCKWISE)
                image = cv2.resize(image,(1600,900))
                err = func(image)
                if debug == True:
                    Vid.showimage(image,str(err.tolist()))
                del image
                os.remove('temp\\temp.jpg')
                os.remove('temp\\temp.mkv')
        elif mode == 'endIn_v2':
            err = 9E9 #dummy value
            while err > tolerance:
                for file in os.listdir():
                    if file.endswith('.log'):
                        os.remove(file)
                jump = round(jump + step,3)
                subprocess.run(f'ffmpeg -ss {start} -i {file_path} -t {jump-start} -c copy temp\\temp.mkv')
                success = False
                while success != True:
                    subprocess.run(f'ffmpeg -sseof -3 -i temp\\temp.mkv -update 1 -q:v 1 ' +
                            f'temp\\temp.jpg -report')
                    if debug == True:
                        input('after jpg conversion')
                    for file in os.listdir():
                        if file.endswith('.log'):
                            with open(file) as openedfile:
                                text = openedfile.read()
                                if 'Conversion failed!' not in text:
                                    success = True
                            os.remove(file)

                image = cv2.imread('temp\\temp.jpg')
                if self.rotation_metadata == 90: 
                    image = cv2.rotate(image,cv2.ROTATE_90_COUNTERCLOCKWISE)
                elif self.rotation_metadata == -90: 
                    image = cv2.rotate(image,cv2.ROTATE_90_CLOCKWISE)
                else:
                    image = cv2.rotate(image,cv2.ROTATE_90_COUNTERCLOCKWISE)
                image = cv2.resize(image,(1600,900))
                err = func(image)
                if debug == True:
                    Vid.showimage(image,str(err.tolist()))
                del image
                os.remove('temp\\temp.jpg')
                os.remove('temp\\temp.mkv')
                
        if stepback == True:
            jump = round(jump - step,3)
        return jump

    def bisection(self,file_path, jump, start, func, iterations = 8, duration = 2, tolerance = 100,debug=False):
        #similar to jumpsearch(mode = 'endIn'), but as name implies uses bisection method to converge to target
        #!is only applicable to this specific scenario, needs to be rewritten to be used in a more general fashion
        beg = jump
        end = jump + duration
        begBoo = False
        endBoo = True
        for i in range(iterations):
            time = (beg + end)/2
            jump = round(time,3)
            subprocess.run(f'ffmpeg -ss {start} -i {file_path} -t {jump-start} -c copy temp\\temp.mkv')
            subprocess.run(f'ffmpeg -sseof -3 -i temp\\temp.mkv -update 1 -q:v 1 ' +
                        f'temp\\temp.jpg')
            image = cv2.imread('temp\\temp.jpg')
            if self.rotation_metadata == 90: 
                image = cv2.rotate(image,cv2.ROTATE_90_COUNTERCLOCKWISE)
            elif self.rotation_metadata == -90: 
                image = cv2.rotate(image,cv2.ROTATE_90_CLOCKWISE)
            else:
                image = cv2.rotate(image,cv2.ROTATE_90_COUNTERCLOCKWISE)
            image = cv2.resize(image,(1600,900))
            err = func(image)
            if debug == True:
                Vid.showimage(image,str(err.tolist()))
            del image
            os.remove('temp\\temp.jpg')
            os.remove('temp\\temp.mkv')
            if err > tolerance:
                beg = time
            else:
                end = time
        return beg

    def delete(self, confirmation = True):
        if confirmation == True:
            response = input(f'Delete {self.filedir}? (y/n)')
            if response == 'y':
                pass
            elif response != 'y':
                return 0
        os.remove(self.filedir)
        self.__del__()
    
    def mp4tomkv(self, dst=None):
        if os.path.isfile('temp/temp_main.mkv'):
           os.remove('temp/temp_main.mkv')
        if dst==None:
            subprocess.run(f'ffmpeg -i "{self.filedir}" -c:v copy -c:a pcm_s16le temp/temp_main.mkv')
        else:
            subprocess.run(f'ffmpeg -i "{self.filedir}" -c:v copy -c:a pcm_s16le "{dst}"')
        self.old_filedir = self.filedir
        self.filedir = 'temp/temp_main.mkv'



    def find_start(self,debug=False):
        if self.start is None:
            jump = 0 
            jump = self.jumpSearch(self.filedir, jump, func = Vid.loadingcompare,stepSize = 1.5,debug=debug) #look for gray loading screen
            jump = self.jumpSearch(self.filedir, jump,func = Vid.loadingcompare, mode = 'out', stepback = True,debug=debug) #look away 
            jump = self.jumpSearch(self.filedir, jump,func = Vid.loadingcompare, mode = 'out', stepSize = 0.10, stepback = True,debug=debug) 
            jump = self.jumpSearch(self.filedir, jump,func = Vid.loadingcompare, mode = 'out', stepSize = 0.02,debug=debug) 
            self.start = jump + Vid.fudge 
    
    def find_end_v3(self): #assumes that first frame is same as last frame 
        assert (self.start != None), 'Need start time'
        jump = self.start + 116
        jump = self.jumpSearch(self.filedir, jump, func = Vid.loadingcompare,stepSize = 1.5, stepback = True)
        jump = self.jumpSearch(self.filedir, jump,func = Vid.loadingcompare, stepSize = 0.10, stepback = True) 
        jump = self.jumpSearch(self.filedir, jump,func = Vid.loadingcompare, stepSize = 0.02, stepback = True) 
        self.end = jump
    
    def find_end(self):
        assert (self.start != None), 'Need to identify start time before finding end time.'
        if self.end is None:
            jump = self.start + 116
            jump = self.jumpSearch(self.filedir, jump,func = Vid.loadingcompare,stepSize = 2, stepback = True, mode = 'endIn', start = self.start)
            jump = self.bisection(self.filedir, jump, start = self.start,func = Vid.loadingcompare) 
            self.end = jump
    
    def find_rough_end(self):
        assert (self.start != None), 'Need to identify start time before finding end time.'
        jump = self.start + 116
        jump = self.jumpSearch(self.filedir, jump, func = Vid.loadingcompare, stepSize = 1, debug=False)
        self.rough_end = jump - 5

    def find_end_from_rough_end(self):
        assert (self.rough_end != None), 'Need to identify rough end time first.'
        jump = self.rough_end
        jump = self.jumpSearch(self.filedir, jump,func = Vid.loadingcompare,stepSize = 1.5, stepback = True, mode = 'endIn', start = self.start)
        jump = self.bisection(self.filedir, jump, start = self.start,func = Vid.loadingcompare) 
        self.end = jump


    def find_start_debug(self):
        if self.start is None:
            jump = 0 
            jump = self.jumpSearch(self.filedir, jump, func = Vid.loadingcompare,stepSize = 1.5, debug=True) #look for gray loading screen
            jump = self.jumpSearch(self.filedir, jump,func = Vid.loadingcompare, mode = 'out', stepback = True) #look away 
            jump = self.jumpSearch(self.filedir, jump,func = Vid.loadingcompare, mode = 'out', stepSize = 0.10, stepback = True) 
            jump = self.jumpSearch(self.filedir, jump,func = Vid.loadingcompare, mode = 'out', stepSize = 0.02) 
            self.start = jump + Vid.fudge 

    def find_end_debug(self):
        assert (self.start != None), 'Need to identify start time before finding end time.'
        if self.end is None:
            jump = self.start + 116
            jump = self.jumpSearch(self.filedir, jump,func = Vid.loadingcompare,stepSize = 1, stepback = True, mode = 'endIn_v2', start = self.start, debug=True)
            jump = self.bisection(self.filedir, jump, start = self.start,func = Vid.loadingcompare) 
            self.end = jump
    
    def write_log(self):
        if os.path.isfile(os.path.join('data','log.csv')) != True:
            with open(os.path.join('data','log.csv'),'w+',encoding='utf-8') as f:
                f.write('NAME,COMMAND\n')
        with open(os.path.join('data','log.csv'),'a',encoding='utf-8') as f:   
            f.write(f"{','.join(self.ffmpeg_command)}\n")


    def trim_mkv(self):
        ffmpeg_command = 'ffmpeg '
        if self.start != None:
            ffmpeg_command += f'-ss {self.start} '
        ffmpeg_command += f'-i temp/temp_main.mkv '
        if self.end != None:
            if self.start != None:
                ffmpeg_command += f'-t {self.end-self.start} '
            elif self.start == None:
                ffmpeg_command += f'-t {self.end} ' 
        ffmpeg_command += '-c copy temp/temp_output.mkv    '
        self.ffmpeg_command = [self.old_filedir, ffmpeg_command]
        subprocess.run(ffmpeg_command)
        self.write_log()

    
    def cleanup(self):
        '''
        output file gets named here
        '''
        new_filename = Path(self.old_filedir).name
        os.rename('temp/output_final.mp4',f'output/{new_filename}') #make sure this works
        for file in os.listdir('temp'):
            os.remove(f'temp/{file}')

    def solo_cleanup(self):
        new_filename = self.solo_rename()
        os.rename('temp/output_final.mp4',f'output/{new_filename}') #make sure this works
        for file in os.listdir('temp'):
            os.remove(f'temp/{file}')

    def cleanup_compilation(self):
        new_filename = Path(self.old_filedir).name
        os.rename('temp/output_final.mp4',f'output/{new_filename}') #make sure this works
        for file in os.listdir('temp'):
            os.remove(f'temp/{file}')
    
    
    def remove_original_file(self): #DELETES ORIGINAL FILE
        os.remove(self.old_filedir)
        

    def standard_pipeline(self):
        self.mp4tomkv()
        self.find_start()
        self.find_end()
        self.trim_mkv()
        self.mkvtomp4()
        self.cleanup()
        self.remove_original_file()

    def v2_pipeline(self):
        Vid.empty_temp_folder()
        self.set_rotation_metadata()
        self.mp4tomkv()
        self.find_start()
        self.find_rough_end()
        self.find_end_from_rough_end()
        self.trim_mkv()
        self.mkvtomp4()
        self.cleanup()
        self.remove_original_file()
    
    def compilation_pipeline(self):
        Vid.empty_temp_folder()
        self.set_rotation_metadata()
        self.mp4tomkv()
        self.find_songname()
        self.find_start()
        self.find_rough_end()
        self.find_end_from_rough_end()
        self.trim_mkv()
        self.mkvtomp4()
        self.cleanup_compilation()
        self.remove_original_file()
    
    def solo_pipeline(self):
        self.set_rotation_metadata()
        self.mp4tomkv()
        self.find_songname(find_solo_idol=True)
        self.find_start()
        self.find_rough_end()
        self.find_end_from_rough_end()
        self.trim_mkv()
        self.mkvtomp4()
        self.solo_cleanup()
        self.remove_original_file()
    
    def solo_rename(self):
        name_dict = {
            "arisu": "arisuSSB",
            "koharu": "koharuCD",
            "yoshino": "yoshino3",
            "yukimi": "yukimiSSB",
            "yumi": "yumi2"
        }
        new_name = f"[デレステ] {self.songname} {name_dict[self.solo_name]}.mp4"
        return new_name


    def keep_start_pipeline(self):
        self.mp4tomkv()
        self.start = 0
        self.find_end()
        self.trim_mkv()
        self.mkvtomp4()
        self.cleanup()
    
    def standard_without_trim(self):
        Vid.empty_temp_folder()
        self.mp4tomkv()
        self.find_start()
        self.find_end()

    def v2_without_trim(self):
        Vid.empty_temp_folder()
        self.mp4tomkv()
        self.find_start()
        self.find_rough_end()
        self.find_end_from_rough_end()

    def check_integrity(self):
        #checks integrity of a Vid object
        a = time.time()
        print(self.filedir)
        if self.rotation_metadata == None:
            self.set_rotation_metadata()
            Vid.empty_temp_folder()
        vidcap = cv2.VideoCapture(self.filedir)
        frame_counter = 1
        detected_counter = 0
        start_time = 0
        success, image = vidcap.read()

        while frame_counter < 180:
            try:
                vidcap.set(cv2.CAP_PROP_POS_MSEC, frame_counter * 1000)
                success, image = vidcap.read()
                if self.rotation_metadata == 90: 
                    image = cv2.rotate(image,cv2.ROTATE_90_COUNTERCLOCKWISE)
                elif self.rotation_metadata == -90: 
                    image = cv2.rotate(image,cv2.ROTATE_90_CLOCKWISE)
                else:
                    image = cv2.rotate(image,cv2.ROTATE_90_COUNTERCLOCKWISE)
                image = cv2.resize(image,(1600,900))
                err = Vid.loadingcompare(image)
                if err < 50:
                    detected_counter += 1
                    frame_counter += 110
                elif err >= 50:
                    frame_counter += 1

            except:
                try:
                    vidcap.release()
                except:
                    pass
                break

        assert detected_counter >= 2, f"Error: {self.filedir} is displaying unexpected behavior. Please manually check the video file."
        try:
            vidcap.release()
        except:
            pass
        print(time.time() - a, '') 
            
        
        
        



        


