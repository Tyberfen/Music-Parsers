#!/usr/bin/python3

import os

"""
short routine to correct a mistake a made in another programm
by adding ".mp3" to filename to all files in cwd (well, not all, just 48, as it concers just 48 files in this perticular case)
"""

def main():
    cwd = os.getcwd()
    chk = 0
    for file in os.listdir(cwd + '/parser/'):
        filename = os.fsdecode(file)
        if filename.endswith(".mp3"):
            chk += 1
            continue
        if chk ==48:
            return
        src_str = cwd + '/parser/' + filename
        dst_str = src_str + ".mp3"
        os.rename(src_str, dst_str)

if __name__ == '__main__':
    main()
