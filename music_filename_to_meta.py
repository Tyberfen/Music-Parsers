#!/usr/bin/python3

import sys
import os
import re
from mutagen.easyid3 import EasyID3
from mutagen.mp4 import MP4

"""
immediate todos:
    implement context to meta_data in get_meta_from_filename
    (to make sure it's added to meta_data['songtitle'] if necessary)

"""

meta_data = {
    'songtitle' : '',
    'artist' : '',
    'album' : '',
    'songnumber' : '',
    'context':''

}

"""
Gets the pattern of the filename and a filename as an input and 'returns' (changes the dict meta_data) the appropriate values
The pattern describes 1 of 3 predefined cases:
'Artist -- Songtitle' = 0
'Album xy -- Songtitle.mp3' = 1
'Artist -- Album xy -- Songtitle' = 2
"""
def get_meta_from_filename(pattern_mark, file_name):

    file_name = file_name.replace(".mp3","")
    file_name = file_name.replace(".m4a", "")
    substr = file_name.split(' -- ')
    potential_number = ''


    if(pattern_mark == 0):
        meta_data['artist'] = substr[0]
        meta_data['songtitle'] = substr[1]

    elif(pattern_mark == 1):
        sub_sub_str = substr[0].split(' ')
        potential_number = sub_sub_str[len(sub_sub_str)-1]
        if(potential_number.isnumeric()):
            substr[0] = substr[0].replace(" " + potential_number, '')
            meta_data['songnumber'] = potential_number
        meta_data['album'] = substr[0]
        meta_data['songtitle'] = substr[1]

    elif(pattern_mark == 2):
        sub_sub_str = substr[1].split(' ')
        potential_number = sub_sub_str[len(sub_sub_str)-1]
        if(potential_number.isnumeric()):
            substr[1] = substr[1].replace(" " + potential_number, '')
            meta_data['songnumber'] = potential_number

        meta_data['album'] = substr[1]
        meta_data['songtitle'] = substr[2]


    print('\n' + 'Sontitle: "' + meta_data['songtitle'] + '" succesfully identified')
    print('Albumtitle: "' + meta_data['album'] + '" succesfully identified')
    if(potential_number != ''):
        print('Songnumber: "' + meta_data['songnumber'] + '" succesfully identified')

    return


def main():

    context = ""
    pattern_marker = -1
    programmname = __file__
    cwd = os.getcwd()
    programmname = programmname.replace(cwd, '')
    #programmname = programmname.replace('\', '' )
    #programmname = programmname.replace('/', '') #Those 2 functions dont work and I cannot fathom why. Glad I dont need them

    if(sys.argv[0] in programmname):
        sys_var = 0
    else:
        sys_var = 1



    for i in sys.argv:

        #declares, if required e.g ' (ciconia)' to Songtitle
        if('context'in i):
            substr = i.split('=')
            meta_data['context'] =" (" + substr[1] + ")"

        #specifies the used filenaming pattern - 3 different patterns planned
        if('pattern' in i):
            substr = i.split('=')
            pattern_marker = int(substr[1])

    if(pattern_marker == -1):
        #The german input mainly for my dad, who might use the programm as well
        input_query = "Bitte eine von 3 Varianten wählen(welches 'Namensmuster' hat das Eingabefile)" +"\n" + "(xy steht für beliebige Zahl)(statt mp3 auch m4a moeglich):"
        input_query = input_query + "\n"+ "0: 'Artist -- Songtitle.mp3'" + "\n" +"1: 'Album xy -- Songtitle.mp3'"
        input_query = input_query + "\n" + "2: 'Artist -- Album -- Songtitle.mp3'" + "\n" + "Bitte entsprechende Nummer tippen:"
        pattern_marker = input(input_query)


    for file in os.listdir(cwd):
        filename = os.fsdecode(file)

        meta_data['songtitle'] = ''
        meta_data['artist'] = ''
        meta_data['album'] = ''
        meta_data['songnumber'] = ''

        if(filename.endswith('.mp3')):
            get_meta_from_filename(int(pattern_marker), filename)

            audio = EasyID3(filename)
            audio['artist'] = meta_data['artist']
            audio['album'] = meta_data['album']
            audio['title'] = meta_data['songtitle'] + meta_data['context']
            audio['tracknumber'] = meta_data['songnumber']
            audio.save()


        if(filename.endswith('.m4a')):
            get_meta_from_filename(int(pattern_marker), filename)

            audio = MP4(filename).tags
            audio["\xa9nam"] = meta_data['songtitle'] + meta_data['context']
            audio["\xa9alb"] = meta_data['album']
            audio["\xa9ART"] = meta_data['artist']
            #audio['trkn'] = meta_data['songnumber'] #No idea, why it makes me trouble, but it's work without as well. not pretty, but sufficent (for now)
            audio.save(filename)

    os.system("pause")
    return

if __name__ == '__main__':
    main()


    """
    general pattern:
    Read out file with one of 3 naming patterns:
    'Album xy -- Songtitle.mp3'
    'Artist -- Songtitle'
    'Artist -- Album xy -- Songtitle'
    xy, songnumber if available
    ggf noch ein Tag in Commandline setzen, das bsp (Ciconia) zu Songtitle added.
    Vlt nach dem Muster: 'context=Ciconia'

    Split Fileprogrammnamestring in die entsprechenden Parts

    -> identify Artists
    -> identify Albumtitle
    -> Identify number (if available) - check if its there to beginn with

    Stores Values
    rewrites the meta via mutagen
    """
