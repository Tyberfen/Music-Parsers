#!/usr/bin/python3

"""
Short programm to replace a certain string in all filenames of a given directory
"""


import sys
import os

def main():

    #Checks if code is executed in linux (./Repl...) or win (python Repl...)
    if("Replace_all_string_in_directory.py" in sys.argv[0]):
        sys_var = 0
    else:
        sys_var = 1

    if(len(sys.argv) < (2 + sys_var)):
        print("Old String not defined./nAdd string, that is to replaced in command. Should look something like:/n/./Replace_all_string_in_directory.py 'old_str' 'new_str'")
        return
    else:
        old_str = sys.argv[1 + sys_var]

    if(len(sys.argv) < 3 + (sys_var)):
        new_str = ""

    else:
        new_str = sys.argv[2 + sys_var]

    cwd = os.getcwd()

    for file in os.listdir(cwd):
        filename = os.fsdecode(file)
        new_filename = filename.replace(old_str, new_str)
        src_str = cwd + '/' + filename
        dst_str = cwd + '/' + new_filename
        os.rename(src_str, dst_str)
    return

if __name__ == '__main__':
    main()
