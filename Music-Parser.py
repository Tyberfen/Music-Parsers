#!/usr/bin/python3

import sys
import os
from mutagen.easyid3 import EasyID3

"""So, what is this supposed to be? Well, its a routine to that parses a txt-file to get the relevant (see variable defs not too far away) tags for some mp3 files and then rewrites those, before moving the finished files to an output-directory as I couldn't be bothered to spend an hour or so to do this manually. Spoiler alert: The routine took a lot longer than that..."""

titel_nr = 0
cwd = os.getcwd() #current working folder
interpret = ''   #interpret of file - a being just a placeholder to define the string
album = ''   # ...
genre = ''   # ...
year = 0      #of importance only for mp3. Gonna that distinction later

#get_elementary_data: Parses input-txt, Initilizes interpret, album, year and genre
def get_elementary_data():
    datasheet = open(sys.argv[1], 'r')
    datasheet_list = datasheet.readlines()
    check = 0  #used to prevent the list from iterating through the whole doc


    for i in datasheet_list:
        if("genre" in i):
            substr = i.split(': ')
            global genre
            genre = substr[1].replace("\n","")
            check +=1

        if("interpret" in i):
            substr = i.split(': ')
            global interpret
            interpret = substr[1].replace("\n","")
            check+=1

        if("album" in i):
            substr = i.split(': ')
            global album
            album = substr[1].replace("\n","")
            check+=1
        if("year" in i):
            substr = i.split(': ')
            global year
            year = int(substr[1])
            check +=1
        if (check == 4):
            return

#gets the file_number from filename directly
def get_count(filename):
    substr = filename.split(".")
    count = int(substr[0])
    return count

# gets the titel from the txt file
def get_titel(count):
    datasheet = open(sys.argv[1], 'r')
    datasheet_list = datasheet.readlines() #file to list
    disc2 = 0
    list2 = 0

    #see what disc on. Comment out if not required
    if count > 25:
        count -=25
        disc2 = 1

    #split string in 2 Parts [mark for the "return-if" later, titel], see what part of the list in txt on
    for i in datasheet_list:
        substr = i.split(" - ")
        if 'DISC 2' in i:
            list2 = 1

        if(disc2 == 0):
            #define mark for "return if"
            if count < 10 and count >= 1: # 2 -> 02
                controll_string = 'Track 0' + str(count)
            else:
                controll_string = 'Track ' + str(count)


            if(controll_string in substr[0]):
                return_str = substr[1].replace("\n","")
                return return_str
        else:
            #looks for titel in 2nd part of list, after the DISC 2
            if(list2 == 1):
            #define mark for "return if"
                if count < 10 and count >= 1: # 2 -> 02
                    controll_string = 'Track 0' + str(count)
                else:
                    controll_string = 'Track ' + str(count)


                if(controll_string in substr[0]):
                    return_str = substr[1].replace("\n","")
                    return return_str
            pass

#checks, if the input  string contains illegal letters, such as {?/\:<>|"*}
def chk_string(str):
    illegal = ['?', "/", '\\', ':', '<','>', '|', '*', '"' ]
    for i in illegal:
        if i in str:
            rstr = str.replace(i, "_")
            return rstr
    return str

def main():

    if(len(sys.argv)<2):
        print("Error: No Input file for data")
        print("Try the command: ./music-parser.py some-txt-file-with-the-data.txt")
        print("Necessary format:\n\nalbum: albumname\ngenre: musicgenre\ninterpret: some-fantastic-artist\nyear: 1984\nTrack xy - name of title\n ...")
        return -1


    global titel_nr
    global album
    global genre
    global interpret
    global cwd
    global year

    get_elementary_data()

    #Missing outputfolder handling
    if not(os.path.exists(cwd+'/output')):
        os.mkdir(cwd+'/output')
        directory = os.fsencode(cwd)

    """ goes through all files in the cwd, checks for the metadata and then replaces everything,
    before moving the files to the output folder. Terrible solution, but it gets the job done"""

    for file in os.listdir(cwd):
        filename = os.fsdecode(file)
        if filename.endswith(".mp3"):

            titel_nr = get_count(filename)
            titel = get_titel(titel_nr)# + ' (SYMTB)'
            src_str = cwd + '/' + filename
            titel = chk_string(titel)

            # turns 1 to 01
            if titel_nr < 10 and titel_nr >= 1:
                dest_str = cwd + '/output/' + album + ' 0' + str(titel_nr) + ' - ' + str(titel) + ".mp3"
            else:
                dest_str = cwd + '/output/' + album + ' ' + str(titel_nr) + ' - ' + str(titel) + ".mp3"



            audio = EasyID3(filename)
            audio['genre'] = genre
            audio['artist'] = interpret
            audio['album'] = album
            audio['title'] = titel
            audio['tracknumber'] = str(titel_nr)
            audio.save()
            os.rename(src_str, dest_str)

if __name__ == "__main__":
    main()
"""
Spagetti code:

get normal stuff from txt file (interpret, album, Year, genre)

for loop {

    if(beginns with number)
        counter = that number
        get unique stuff from txt file (titel, titel_nr)
        rename songname
        rename file
        reset titel_nr

    else break

}

"""
