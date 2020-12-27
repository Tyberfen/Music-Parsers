#!/usr/bin/python3

"""
Short programm to replace a certain string in all filenames of a given directory
"""


import sys
import os

def main():

    if(len(sys.argv) < 2):
        print("Old String missing./nName str, that is to replaced as argv[1]")
        return
    else:
        old_str = sys.argv[1]

    if(len(sys.argv) < 3):
        new_str = ""

    else:
        new_str = sys.argv[2]

    cwd = os.getcwd()

    for file in os.listdir(cwd):
        filename = os.fsdecode(file)
        src_str = cwd + '/' + filename

        dst_str = src_str.replace(old_str, new_str)

        os.rename(src_str, dst_str)
    return

if __name__ == '__main__':
    main()
