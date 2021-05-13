###  
###   _____                                      _   _______   _           
###  |  __ \                                    | | |__   __| (_)          
###  | |__) |_ _ _ __ ___  ___    __ _ _ __   __| |    | |_ __ _ _ __ ___  
###  |  ___/ _` | '__/ __|/ _ \  / _` | '_ \ / _` |    | | '__| | '_ ` _ \ 
###  | |  | (_| | |  \__ \  __/ | (_| | | | | (_| |    | | |  | | | | | | |
###  |_|   \__,_|_|  |___/\___|  \__,_|_| |_|\__,_|    |_|_|  |_|_| |_| |_|
###  __      ___     _                
###  \ \    / (_)   | |               
###   \ \  / / _  __| | ___  ___  ___ 
###    \ \/ / | |/ _` |/ _ \/ _ \/ __|
###     \  /  | | (_| |  __/ (_) \__ \
###      \/   |_|\__,_|\___|\___/|___/
###                                   
###                                          [i]Bymyself
###                                          [10]shots
###  
###
###  |___<INSTRUCTIONS>_____________________________________|
###  |(1) Open or Create text file called "URLs-to-crop.txt"|    
###  |    in same directory as this script                  |           
###  |(2) Paste in URLS                                     |     
###  |(3) After each URL, on a new line, put the start time |
###  |(4) on the next line, put the end line                |    
###  |    Example:                                          |    
###  |    youtube.com/v/video                               |            
###  |    1:23                                              |     
###  |    1:50                                              |                                 
###  |(5) Save text file. Run script                        |                 
###   
###
###  |__<DEPENDENCIES>_________|
###  | - linux                 |   
###  | - python3               |   
###  | - os, pathlib, datetime |  
###  | - moviepy               |   
###  | - ffmpeg, imageio       |   
###  | - ytdl, [atomicparsley] |   
###   
###  

# TODO make settings changeable via arguments
# ─── SETTINGS ───────────────────────────────────────────────────────────────────
write_log_file = True          # False or True
dev_mode = True                # False or True
print_progress = True          # False or True
no_progress = False            # False or True
ignore_errors = True           # False or True
auto_title = False             # False or True
auto_artist = False            # False or True
autonumber = False             # False or True
playlist_start = False         # False or index to start at
playlist_end = False           # False or index to end on
autonumber = False             # False or True
move_to_new_directory = False  # False or path to final location (use esc characters for \)
audio_only = False             # False or True
metadata_from_title = False    # False or format (e.g., r"%(artist)s | %(title)s") PUT r before str
embed_thumb = False            # False or True (requires atomic parsley)
min_views = False              # False or int
max_views = False              # False or int
min_filesize = False           # False or int
max_filesize = False           # False or int
# ────────────────────────────────────────────────────────────────────────────────

    # TODO implement error checking
    # on errors:
    # try "--no-check-certificate"
    #     "--force-ipv4"
    # remove "--hls-prefer-ffmpeg"
    #     proxy from other country
    #     recode to mp4 
    #     on keyframe ffmpeg
    # handle the WARNING: Requested formats are incompatible for merge and will be merged into mkv. errror -> change name

import os
import pathlib
from datetime import datetime
from datetime import date
# from os import walk
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

if write_log_file:
    n = "Parse_and_Trim_log.txt"
    file_list = os.listdir()
    if n not in file_list:
        log_file = open(n, "w")
    else:
        log_file = open(n, "a")


def format_user_input():
    input_file = open("URLs-to-crop.txt", "r")
    raw_list = input_file.readlines()
    
    # Strip \n from lines
    i = 0
    while i < len(raw_list):
        raw_list[i] = raw_list[i].replace("%20", "").strip("\n").strip()
        i += 1
        
    # Search for empty lines
    empty_indices = []
    for index, element in enumerate(raw_list):
        if not element:
            empty_indices.append(index)

    # Remove empty lines
    shift = 0
    for i in empty_indices:
        raw_list.pop(i - shift)
        shift += 1
    return raw_list


def ytdl_command():
    ytdl_settings = " --add-metadata --hls-prefer-ffmpeg"
    s = check_for_settings(ytdl_settings)
    s += get_ytdl_outputC()
    return "youtube-dl " + s


def check_for_settings(z):
    cmd = str(z)
    if ignore_errors:
        cmd += " --ignore-errors"
    if playlist_start:
        cmd += " --playlist-start " + str(playlist_start)
    if playlist_end:
        cmd += " --playlist-end " + str(playlist_end)
    if audio_only:
        cmd += " -f bestaudio"
    if metadata_from_title:
        cmd += " --metadata-from-title " + "'" + str(metadata_from_title) + "'"
    if embed_thumb:
        cmd += " --embed-thumbnail"
    if min_views:
        cmd += " --min-views " + "'" + str(min_views) + "'"
    if max_views:
        cmd += " --max-views " + "'" + str(max_views) + "'"
    if max_filesize:
        cmd += " --max-filesize" + "'" + str(max_filesize) + "'"
    if min_filesize:
        cmd += " --min-filesize" + "'" + str(min_filesize) + "'"
    if no_progress:
        cmd += " --no-progress"
    return cmd


def get_ytdl_outputC():
    # get title and output path
    p = " -o "
    
    # TODO implement ability to have autonumbers and custom titles
    # TODO and update the filename in later functions
    if autonumber:
        if auto_title:
            if auto_artist:
                p += r"%(autonumber)s - %(artist)s - %(title)s.%(ext)s"
            else:
                p += r"%(autonumber)s - %(title)s.%(ext)s"
        else:
            if auto_artist:
                p += r"%(autonumber)s - %(artist)s.%(ext)s"
            else:
                p += r"%(autonumber)s" + " - "
    if auto_title and not autonumber and not auto_artist:
            p += r"%(title)s.%(ext)s"
    if auto_artist and not autonumber and not auto_title:
            p += r"%(artist)s.%(ext)s"
    if auto_title and auto_artist:
                p += r"%(artist)s - %(title)s.%(ext)s"

    return p


def duplicate_names(potential_file_name):
    file_list = os.listdir()
    for file in file_list:
        if potential_file_name == file[:-3]:
            return False
    return True


def get_title_box(name, url3):
    fill = 0
    fill = (30 - len(str(name))) // 2
    n = str(name)
    j = "|" + " " * 29 + " " * fill + n + " " * fill + " " * 29 + "|"
    u_template = "|    URL:           |   {}    "
    u = str(url3)
    if u[:5] == "https":
        u = str(url3)[8:]
    return "\n\n" + "-"*90 + "\n" + "|" + " "*88 + "|\n" + j + "\n" + "|"\
         + " "*88 + "|\n" + "-"*90 + "\n\n" + u_template.format(u) + "\n"


def to_figlet(msg, font=None, justification=None, size=None):
    '''
    font: banner, term, smslant, smshadow, smscript, slant, shadow,
          script, mnemonic, mini, lean, ivrit, digital, bubble,
          block, big, all (print in every font)
    justification: close, spaced, right, left, center, paragraph
    size: small, big (only works with default font)
    '''
    font_list = ["banner", "term", "smslant", "smshadow", "smscript", "slant", "shadow", "small",\
        "script", "mnemonic", "mini", "lean", "ivrit", "digital", "bubble", "block", "big", "all"]
    cm2 = "figlet "
    
    # Font and Size
    fontC = " -f standard"
    if font:
        fontC = " -f " + str(font)
    if font == True and font not in font_list:
        fontC = " -f big"
    if font and size:
        fontC = " -f " + str(size)
        if str(size) not in font_list:
            fontC = " -f big"
    if size and not font:
        if str(size) not in font_list:
            fontC = " -f big"
        else:
            fontC = " -f " + str(size)

    # Justification
    if justification:
        j = str(justification[:1])
        i = 0
        while not str(justification)[i:i+1].isalpha() and i < len(str(justification)):
            j = str(justification)[i:i+1]
            i += 1
        if j == "s":
            j = "k"
        if j == "c":
            j = "s"
        jc = " -" + j
        if j not in ["r", "c", "s", "S", "k", "l"]:
            jc = " -c"
        justification = " -" + str(justification[:1])
    if not justification:
        jc = " -c"

    cm2 += jc + fontC + " " + str(msg)  
    if font == "all":
        cm2 = "showfigfonts " + str(msg)
    os.system(cm2)


def dl(url, start_time, end_time, name, link_index):
    ytdl_c = ytdl_command()
    cm = ytdl_c + str(name) + ".mp4 " + str(url)
    if print_progress:
        print("Command Passed to Youtube-dl:\n" + cm + "\n")
        to_figlet(str(link_index), "small", "right")
        to_figlet(str(name)[-10:], "small")
        to_figlet(str(start_time) + " => " + str(end_time))
    if write_log_file:
        log_file.write(get_title_box((str(link_index) + "  " + name), str(url)))
        t_template = "|    Start Time:    |       {}       |     End Time:     |       {}       |\n"
        log_file.write(t_template.format(str(start_time), str(end_time)))
    os.system(cm)
    to_figlet(("finished: " + str(link_index)), "small", "right")
    time_stamp = str(date.today()) + "  " + datetime.now().strftime("%H:%M:%S")
    f_template = "|    Finished On:   |       {}    \n"
    log_file.write(f_template.format(time_stamp))


def validate_timecodes(time_code):
    t = str(time_code).strip()
    if dev_mode:
        print(time_code)
        print(t)
    if ":" not in t:
        if " " in t:
            print("pass")
            t = t.replace(" ", ":")
        else:
            if len(t) == 4:
                t = "0" + t[:1] + ":" + t[1:]
            elif len(t) == 3:
                t = "0" + t[:1] + ":" + t[1:]
            else:
                t = t[:2] + ":" + t[2:]
    t = t.replace(" ","")
    for character in t:
        if character.isalpha() == True:
            print("illegal time code for video:  " + t)
            t = "05:00"
    if dev_mode:
        print("time code after validation: " + t)
    return t


def timecode_to_sec(time_code):
    seconds = 1
    t = time_code.split(":")
    seconds += int(int(t[0]) * 60) + int(t[1])
    return seconds


def crop(files):
    os.system("for i in *.mkv; do ffmpeg -i '$i' -codec copy '${i%.*}.mp4'; done")
    i = 0
    cd = "/" + str(pathlib.Path().absolute()).strip("/") + "/"
    while i <= len(files) - 3:
        p = cd + files[i]

        if ".mkv" in p:
            p = p[:-4] + ".mp4"
        s = files[i+1]
        e = files[i+2]
        temp_name = files[i][:-4] + "__________temp.mp4"
        if dev_mode:
            print(p, s, e, temp_name)
        #cmd1 = "ffmpeg -avoid_negative_ts 1 -ss " + str(s) + " -i " + str(p) + " -c copy -to " + str(e) + " " + new
        #os.system(cmd1)

        

        ffmpeg_extract_subclip(p, s, e, targetname=temp_name)

        # Delete Original File
        rmCommand = "rm " + files[i]
        os.system(rmCommand)
        
        # Rename back to original name
        mvCommand = "mv " + temp_name + " " + files[i]
        os.system(mvCommand)

        # Move to new Directory 
        if move_to_new_directory:
            mvCommand = "mv " + files[i] + " " + move_to_new_directory + "/" + files[i]
            os.system(mvCommand) 

        # Close log file on last iteration
        if i == len(files) - 3 and write_log_file:
            time_stamp = str(date.today()) + " " + datetime.now().strftime("%H:%M:%S")
            f_template = "|    ALL DONE AT:   |     {}"
            log_file.write(f_template.format(time_stamp))
            log_file.close()
            if print_progress:
                print(f_template.format(time_stamp))

        # Print progress
        if print_progress:
            to_figlet(("Cropped  " + str((i//3)+1)), "small")

        i += 3


def main():
    raw_list = format_user_input()
    i = 0; link_index = 1; file_list = []
    to_figlet("Downloading")
    while i <= len(raw_list) - 3:
        url = str(raw_list[i]).strip().replace(" ","")
        start = validate_timecodes(raw_list[i+1])
        end = validate_timecodes(raw_list[i+2])
        nameP = url.split("/")
        name = nameP[len(nameP)-1].replace("+", "_").replace("%20", "_").lower()
        illegalCharacters = ["#", "%", "&", "{", "}", "\\", "<", ">", "*", "?", "/", "$", "ﾉ"," ",\
                            "!", "'", '"', ":", "@", "+", "~", "`", "|", "=", "(", ")", ".", "-"]
        for character in illegalCharacters:
            if character in name:
                name = name.replace(character, "_")
        
        while not duplicate_names(name):
            name += str(i)
        dl(url, start, end, name, link_index)
        i += 3
        link_index += 1
        
        # File list to pass to crop function
        file_list.append(name + ".mp4")
        file_list.append(timecode_to_sec(start))
        file_list.append(timecode_to_sec(end))

    if print_progress:
        to_figlet("Finished Downloading", "small", "right")
    if dev_mode:
        to_figlet("FILE LIST", "banner", "center")
        print("File List Passed to Crop Function:\n")
        print(file_list)
    crop(file_list)
        

main()