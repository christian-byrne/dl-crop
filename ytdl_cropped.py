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
###  |(1) Open or Create text file called "URL-batch.txt"   |    
###  |    in same directory as this script                  |           
###  |(2) Paste in URLS                                     |     
###  |(3) After each URL, on a new line, put the start time |
###  |(4) on the next line, put the end line                |    
###  |    Example:                                          |    
###  |    youtube.com/v/video                               |            
###  |    1:23                                              |     
###  |    1:50                                              |                                 
###  |(5) Save text file in this directory. Run script      |                 
###   
###
###  |__<DEPENDENCIES>_________|
###  | - linux                 |   
###  | - python3               |   
###  | - moviepy               |   
###  | - ffmpeg                |   
###  | - ytdl, [atomicparsley] |   
###   
###  


import os, pathlib
from datetime import datetime, date
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from termcolor import colored
from fig_print import to_figlet


def format_user_input(batch_file="URL-batch.txt", legal_characters=[], filetype=".mp4"):
    """ Reads links from batch file, ignores empty lines, strips newline characters and whitespace.
        Returns list of dicts for each link with items for url, start time, end time,
        title, and file name.

        Params:
            batch_file :       (str) path/filename to batch file. should be a file with list of 
                               links separated by newlines. Default is 'URL-batch.txt'
            legal_characters : (list) any characters that should not be removed from file names
    """

    stripped = [
        line.replace("%20","").replace(" ","").strip("\n") for \
            line in open(batch_file, "r").readlines() if line
    ]
    illegal_chars = ["#", "%", "&", "{", "}", "\\", "<", ">", "*", "?", "/", "$",
    "ﾉ"," ","!", "'", '"', ":", "@", "+", "~", "`", "|", "=", "(", ")", ".", "-"]
    for _ in legal_characters: illegal_chars.remove(_)
    videos = []
    i = 0

    while i <= len(stripped) - 3:
        current_video = {}
        current_video["url"] = stripped[i]
        current_video["start"] = timecode_to_sec(
            validate_timecodes(
                stripped[i+1]
            )
        )
        current_video["end"] = timecode_to_sec(
            validate_timecodes(
                stripped[i+2]
            )
        )
        current_video["title"] = \
            stripped[i].split("/")[-1:] if stripped[i].split("/")[-1:] else stripped[i].split("/")[-2:]

        current_video["file name"] = \
            current_video["title"].replace("+", "_").replace("%20", "_").lower()
        for character in illegal_chars:
            current_video["file name"] = \
                current_video["file name"].replace(character, "_") 
        # Add iterator to file name if file name already exists in cd
        while not duplicate_names(current_video["file name"]):
            current_video["file name"] += str(i)
        current_video["file name"] += filetype if filetype[0] == "." else "." + filetype 
        
        videos.append(current_video)
        i += 3

    return videos


def format_from_webapp(videos, filetype=".mp4"):

    illegal_chars = ["#", "%", "&", "{", "}", "\\", "<", ">", "*", "?", "/", "$",
    "ﾉ"," ","!", "'", '"', ":", "@", "+", "~", "`", "|", "=", "(", ")", ".", "-"]

    for current_video in videos:
        current_video["file name"] = \
            current_video["title"].replace("+", "_").replace("%20", "_").lower()
        for character in illegal_chars:
            current_video["file name"] = \
                current_video["file name"].replace(character, "_") 
        # Add iterator to file name if file name already exists in cd
        while not duplicate_names(current_video["file name"]):
            current_video["file name"] += str(i)
        current_video["file name"] += filetype if filetype[0] == "." else "." + filetype 


def format_ytdl_stdin(settings):
    """ Formats command to pass to ytdl in stdin based on options specifications.
        Returns the string that goes to stdin.
    """

    bool_options = {
    "ignore errors" : " --ignore-errors",
    "audio only" : " -f bestaudio",
    "embed thumb" : " --embed-thumbnail",
    }
    narg_options = {
    "playlist start" :  " --playlist-start ",
    "playlist end" : " --playlist-end ",
    "metadata from title" : " --metadata-from-title ",
    "min views" :  " --min-views ",
    "max views" : " --max-views ",
    "min filesize" : " --min-filesize ",
    "max filesize" : " --max-filesize "
    }
    base = "--add-metadata --hls-prefer-ffmpeg"

    for setting, value in settings.items():
        if value:
            try:
                base += bool_options[setting]
            except:
                try:
                    base += narg_options[setting] + "'" + str(value) + "'"
                except: continue
    
    title = []
    if settings["autonumber"]: title.append(r"%(autonumber)s")
    if settings["auto artist"]: title.append(r"%(artist)s")
    if settings["auto title"]: title.append(r"%(title)s")
    if len(title) > 1: base += " -o " + " - ".join(title) + r".%(ext)s"
    elif title: base += " -o " + title[0] + r".%(ext)s"

    return "youtube-dl " + base


def duplicate_names(potential_file_name, dir=False):
    """ Checks if file already exists (excluding file code). Returns Bool.

        Params:
            potential_file_name: (str) if not in cd, specify dir with 2nd arg.
            dir :                default uses cd. otherwise specify a path (str)
    """

    directory_list = os.listdir() if not dir else dir
    for file in directory_list:
        if potential_file_name == file[:-3] or potential_file_name == file[:-4]:
            return False
    return True


def dl(video, settings, log):
    """ 
    """
    stdin_cmd = format_ytdl_stdin(settings)

    # TODO:
    if "(ext)s" in stdin_cmd:
        pass
    # if the output is automated with autonumber | auto artist | auto title,
    # update "file name" item for this video's dict 
    # The file name will not be accessible until after passed to ytdl because
    # it has to be parsed first. Can access by getting most recent file in directory 
    # as with the unzip function in main py program 

    else: stdin_cmd += " -o " + str(video["file name"])
    stdin_cmd += " " + video["url"]

    if settings["verbose"] or settings["dev mode"]:
        print(
            "Command Passed to Youtube-dl: ",
            stdin_cmd,
            "\nOutput File Name: ",
            video["file name"],
            "\nVideo Title: ",
            video["title"]
        )
        to_figlet(str(video["start"]) + " => " + str(video["end"]))

    if settings["write log file"]:
        log.write(
            "IRL Time Finished: ",
            str(date.today()) + "  " + datetime.now().strftime("%H:%M:%S"),
            "\nCommand Passed to Youtube-dl: ",
            stdin_cmd,
            "\nURL: ",
            str(video["url"]),
            "\nOutput File Name: ",
            video["file name"],
            "\nVideo Title: ",
            video["title"],
            "\nStart Time: ",
            str(video["start"]),
            "\nEnd Time: ",
            str(video["end"]),
            "\n\n\n\n\n\n"
        )

    os.system(stdin_cmd)
    
    return "Done: " + video["title"]


def validate_timecodes(time_code):
    t = str(time_code).strip()
    if ":" not in t:
        if " " in t:
            t = t.replace(" ", ":")
        else:
            if len(t) == 4:
                t = "0" + t[:1] + ":" + t[1:]
            elif len(t) == 3:
                t = "0" + t[:1] + ":" + t[1:]
            else:
                t = t[:2] + ":" + t[2:]
    t = t.replace(" ","")
    replace = ""
    for index, character in enumerate(t):
        if character.isalpha() == True:
            replace += str(index)
    if replace:
        for _ in replace: 
            t = t[:int(_)] + "1" + t[int(_)+1:] 
    
    return t


def timecode_to_sec(time_code):
    seconds = 1
    t = time_code.split(":")
    seconds += int(int(t[0]) * 60) + int(t[1])
    return seconds


def crop(videos, settings):
    """ Convert all videos in cd to mp4 then crop them according to the time
        codes in the videos dict. Delete original files
    """

    try:
        os.system("for i in *.mkv; do ffmpeg -i '$i' -codec copy '${i%.*}.mp4'; done")
        os.system("for i in *.webm; do ffmpeg -i '$i' -codec copy '${i%.*}.mp4'; done")
    except: print("couldn't convert all videos to mp4 before attempting crop")

    for vid in videos:
        ffmpeg_extract_subclip(
            vid["file name"],
            vid["start"],
            vid["end"],
            targetname=( vid["title"] + "_________temp.mp4" )
        )
        # Troubleshooting try these:
        #cmd1 = "ffmpeg -avoid_negative_ts 1 -ss " + str(s) + " -i " + str(p) + " -c copy -to " + str(e) + " " + new
        #os.system(cmd1)

        os.remove(
            vid["file name"]
        )
        if settings["move to new directory"]:
            os.rename(
                vid["title"] + "_________temp.mp4",
                ( settings["move to new directory"] + vid["file name"] )
            )
        else:
            os.rename(
                vid["title"] + "_________temp.mp4",
                vid["file name"]
            )

        if settings["verbose"]:
            print("Cropped: ", vid["title"])


# ────────────────────────────────────────────────────────────────────────────────

def dl_crop(custom_settings=False, from_webapp=False):

    settings = {
        "write log file" : True,
        "dev mode" : True,
        "verbose" : True,
        "ignore errors" : True,
        "auto title" : False,
        "auto artist" : False,
        "autonumber" : False,
        "playlist start" : False,
        "playlist end" : False,
        "autonumber" : False,
        "move to new directory" : False,
        "audio only" : False,
        "metadata from title" : False,
        "embed thumb" : False,
        "min views" : False,
        "max views" : False,
        "min filesize" : False,
        "max filesize" : False
    }
    if custom_settings: settings.update(custom_settings)
    if settings["write log file"]:
        if not os.path.isfile("dl-crop-log.txt"):
            log_file = open("dl-crop-log.txt", "w")
        else: log_file = open("dl-crop-log.txt", "a")
    if settings["verbose"]: to_figlet("Downloading")

    if not from_webapp: videos = format_user_input()
    else: format_from_webapp(from_webapp)

    print(
        colored(
            dl(videos, settings, log_file),
            "green"
        )
    )

    if settings["verbose"]:
        to_figlet("DL Done", "roman")
    if settings["dev mode"]:
        print("File List Passed to Crop Function:\n")
        print(videos)

    crop(videos)


if __name__ == "__main__":
    dl_crop()