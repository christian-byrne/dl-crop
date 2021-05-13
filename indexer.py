import os
from os import walk
import subprocess
import ntpath


imgCodes = ["jpg", "png", "tif", "raw", "eps", "gif", "psd", "xcf", \
            "ai", "cdr", "bmp", "jpeg", "cr2", "nef", "orf", \
            "sr2", "jpe", "jif", "jfif", "jfi", "webp", "k25", \
            "nrw", "arw", "dib", "heif", "heic", "ind", "indd", \
            "indt", "jp2", "j2k", "jpf", "jpx", "jpm", "mj2", \
            "svg", "svgz"]



def no_quotes_in_names(path):
    # Validate that it is a directory
    if not os.path.isdir(path):
        return None
    dirs = os.listdir(path)
    temp = os.getcwd()
    os.chdir(path)
    replace1 = {}
    for file in dirs:
        if "'" in file or '"' in file:
            replace1[file] = file.replace("'","").replace('"', '')
    if replace1:
        for _ in replace1.keys():
            print(_)
            print(replace1[_])
            os.rename(_, replace1[_])
    os.chdir(temp)
    

def get_directories(dir_name):
    
    # Extend recursively with sub directories
    subfolders= [f.path for f in os.scandir(dir_name) if f.is_dir()]
    for dir_name in list(subfolders):
        subfolders.extend(get_directories(dir_name))
    
    # Append original path
    subfolders.append(dir_name)
    
    return subfolders


def make_thumbnails(path, file, name):
    vid_path = path.strip("/") + "/" +  file
    img_name = path.strip("/") + "/" + name + ".png"

    if not os.path.isfile(vid_path[:-4] + "png"):
      subprocess.call(['ffmpeg', '-i', vid_path, '-ss', '00:00:10.000', '-vframes', '1', img_name])
    


def make_dictionary(path_list):
  dir_output = {}
  for _ in path_list:
      
    # Validate that it is a directory
    if not os.path.isdir(_):
        continue


    # skip if there's a single apostrophe in file name
    # TODO: add filename correction for this case
    
    
    # 1st = name
    name_only = ntpath.basename(_)
    print("name_only = " + name_only)
    
    # 2nd = path
    p = _.replace("\\", "/")
    print("path = " + p)

    # 3rd = contents
    # 4th = # of contents
    contents = []
    for (dirPath, dirnames, filenames) in walk(p):
      contents.extend(filenames)
      break
    if not contents:
      continue

    # make thumbnails
    vidTypes = ["webm", "mpg", "mp2", "mpeg", "mpe", "mpv", "ogg", "mp4", "m4p", "m4v", "avi", "wmv", "mov", ".qt", "flv", "swf", "vchd"]
    non_images = []
    images = []
    for fi in contents:
        n = fi.split(".")
        f = n[len(n)-1]
        r = n[:-1]
        r = ".".join(r)
        if f not in vidTypes:
            continue
        if r + ".png" not in contents and r + ".jpg" not in contents:
            make_thumbnails(p, fi, str(r))
            
    
    
    
    dir_output[name_only] = {}
    dir_output[name_only]["name"] = name_only
    dir_output[name_only]["path"] = p.strip("/")+"/"
    dir_output[name_only]["contents"] = contents
    dir_output[name_only]["size"] = len(contents)

  return dir_output


def create_dirs(path):
  path_list = get_directories(path)
  return make_dictionary(path_list)
create_dirs("/home/bymyself/_BYMYself/bmp/static/userLibrary/Plumber_Clips")
