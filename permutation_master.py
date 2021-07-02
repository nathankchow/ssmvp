#0. run script

#1. ask user to specify directory and log into chrome, if implementing #3 (see below ) 

#2. process all files in directory
#       need to implement quality control system (similar to autotouch one)

#3. consider using selenium to upload all files to google drive. 

from permutation_rename import permutation_rename
from permutation_process import permutation_process 
from check_dir_integrity import check_dir_integrity 

def permutation_master():
    directory = permutation_rename()
    check_dir_integrity(directory)
    permutation_process(directory)

if __name__ == '__main__':
    permutation_master()