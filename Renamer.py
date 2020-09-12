#!/usr/bin/python3
"""
Short script to add "(glorious-input-name)"  (yes, including the brackets) to all songnames
No way I could identify the Source if read some word, I probably
recognize
"""

import sys
import os
from mutagen.mp4 import MP4 #not a standart library

def main():
    cwd = os.getcwd()
    check = 0
    for file in os.listdir(cwd):
        filename = os.fsdecode(file)
        if filename.endswith(".m4a"):

            #get stuff
            songname = MP4(filename).tags.get("\xa9nam", [None])[-1] + " (" + sys.argv[1] + ")"
            audio = MP4(filename).tags

            #rewrite and save stuff
            print("Songname: " + songname + "successfully extracted")
            audio["\xa9nam"] = songname
            audio.save(filename)

            print(filename + "has been successfully modified")

            check+=1
            if check == 196 :
                return

if __name__ == '__main__':
    main()
