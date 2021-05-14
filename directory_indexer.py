import os, ntpath, subprocess
from os import walk


imgCodes = ["jpg", "png", "tif", "raw", "eps", "gif", "psd", "xcf", \
            "ai", "cdr", "bmp", "jpeg", "cr2", "nef", "orf", \
            "sr2", "jpe", "jif", "jfif", "jfi", "webp", "k25", \
            "nrw", "arw", "dib", "heif", "heic", "ind", "indd", \
            "indt", "jp2", "j2k", "jpf", "jpx", "jpm", "mj2", \
            "svg", "svgz"]


def no_quotes_in_names(path):
    """ Rename any files that have single or duoble quotes in the path -- not recursive.
        Void - Returns None if not os.path.isdir(path).
        path : (str) path to directory """

    # Validate Path
    if not os.path.isdir(path):
        return None
    
    dirs, temp = os.listdir(path), os.getcwd()
    os.chdir(path)

    replace1 = {}
    for file in dirs:
        if "'" in file or '"' in file:
            replace1[file] = file.replace("'","").replace('"', '')
    if replace1:
        for _ in replace1.keys():
            os.rename(_, replace1[_])

    os.chdir(temp)
    

def get_directories(dir_name):
    """ 
    """
    
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
      
    # Skip non-directories
    if not os.path.isdir(_):
        continue
    
    name_only = ntpath.basename(_)
    p = _.replace("\\", "/")

    contents = []
    for (dirPath, dirnames, filenames) in walk(p):
      contents.extend(filenames)
      break
    if not contents:
      continue

    video_file_types = ["webm", "mpg", "mp2", "mpeg", "mpe", "mpv", "ogg",
    "mp4", "m4p", "m4v", "avi", "wmv", "mov", ".qt", "flv", "swf", "vchd"]

    for fi in contents:
        code = fi.split(".")[-1:]
        base = ".".join(fi.split(".")[:-1])
        if code not in video_file_types: continue
        if base + ".png" not in contents and base + ".jpg" not in contents:
            make_thumbnails(p, fi, str(base))
            
    dir_output[name_only] = {}
    dir_output[name_only]["name"] = name_only
    dir_output[name_only]["path"] = p.strip("/")+"/"
    dir_output[name_only]["contents"] = contents
    dir_output[name_only]["size"] = len(contents)

  return dir_output


def create_dirs(path):
  path_list = get_directories(path)
  return make_dictionary(path_list)