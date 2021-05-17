import os, ntpath, subprocess
from os import walk


imgCodes = ["jpg", "png", "tif", "raw", "eps", "gif", "psd", "xcf", \
            "ai", "cdr", "bmp", "jpeg", "cr2", "nef", "orf", \
            "sr2", "jpe", "jif", "jfif", "jfi", "webp", "k25", \
            "nrw", "arw", "dib", "heif", "heic", "ind", "indd", \
            "indt", "jp2", "j2k", "jpf", "jpx", "jpm", "mj2", \
            "svg", "svgz"]


def no_quotes_in_names(path):
    """ Void. Rename any files that have single or duoble quotes
        in the path -- not recursive.
        path : (str) path to directory """

    # Validate Path
    if not os.path.isdir(path):
        return None
    
    dirs, cwd = os.listdir(path), os.getcwd()
    os.chdir(path)

    to_replace = {}
    for file in dirs:
        if "'" in file or '"' in file:
            to_replace[file] = file.replace("'","").replace('"', '')
    if to_replace:
        for _ in to_replace.keys(): os.rename(_, to_replace[_])

    os.chdir(cwd)
    

def get_directories(dir_name):
    """ Recursively build directory tree. Returns list of all files in 
        every directory in and below dir_name, recursively. File elements 
        are named with their path relative to the root (dir_name arg). 
        Last element in list will be the dir_name.
        Params: 
          dir_name : (str) relative path to root directory.
    """
    subfolders= [f.path for f in os.scandir(dir_name) if f.is_dir()]
    for dir_name in list(subfolders):
        subfolders.extend(get_directories(dir_name))
    subfolders.append(dir_name)

    return subfolders


def make_thumbnails(path, file, name):
    vid_path = path.strip("/") + "/" +  file
    img_name = path.strip("/") + "/" + name + ".png"

    if not os.path.isfile(vid_path[:-4] + "png"):
      try:
        subprocess.call(['ffmpeg', '-i', vid_path, '-ss', '00:00:10.000', '-vframes', '1', img_name])
      except:
        subprocess.call(['ffmpeg', '-i', vid_path, '-ss', '00:00:02.000', '-vframes', '1', img_name])


def treeify_directory(path_list):
  dir_output = {}
  for link in path_list:
      
    # Skip non-directories
    if not os.path.isdir(link):
        continue
    
    name_only = ntpath.basename(link)
    p = link.replace("\\", "/")

    contents = []
    for (dirPath, dirnames, filenames) in walk(p):
      contents.extend(filenames)
      break
    if not contents:
      continue

    video_file_types = ["webm", "mpg", "mp2", "mpeg", "mpe", "mpv", "ogg",
    "mp4", "m4p", "m4v", "avi", "wmv", "mov", ".qt", "flv", "swf", "vchd"]

    contents_dict = {}
    for fi in contents:

        # Videos Only
        code = fi.split(".")[-1:]
        if code not in video_file_types: continue
        
        base = ".".join(fi.split(".")[:-1])
        if base + ".png" not in contents and base + ".jpg" not in contents:
            make_thumbnails(p, fi, str(base))
        contents_dict[fi] = {
          "base name" : base,
          "file code" : code,
          "thumbnail" : base + ".png",
          "containing folder" : name_only,
          "containing path" : p.strip("/")+"/"
        }
        if base + ".jpg" in contents: contents_dict[fi]["thumbnail"] = base + ".jpg"
            
    dir_output[name_only] = {
      "name" : name_only,
      "path" : p.strip("/")+"/",
      "contents list" : contents,
      "content dict" : contents_dict,
      "size" : len(contents)
    }

  return dir_output


def create_dirs(path):
  path_list = get_directories(path)
  return treeify_directory(path_list)