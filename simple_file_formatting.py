import os

path = "C:\\Users\\12064\\OneDrive\\School\\UA\\MATH125\\6_Constructing_Antiderivatives"
exclude = "Resource" # e.g., "pdf", "mp3, "2019"

def get_file_list():
  files = os.listdir(path)
  vids = []
  for _ in files:
    if exclude not in _:
      vids.append(_)
  return vids


def add_iterator(file_list):
  final = []
  for index, _ in enumerate(file_list):
    new = _[8:]
    new = new.replace(" ","_").replace("&","and").strip().replace("_-_", "-").replace(",","")
    iterator = "(" + str(index+1) + ")--"
    final.append(iterator + new)
  return final


def replace_w_iter(file_list, id):
  final = []
  for index, _ in enumerate(file_list):
    iterator = "(" + str(index+1) + ")--"
    final.append(str(id) + " " + iterator)
  return final


def rename(og_files, renamed_files):
  output_path = path.strip("\\") + "\\{}"
  for og, n in zip(og_files, renamed_files):
    original = output_path.format(og)
    new = output_path.format(n)
    os.rename(original, new)


def create_name_dictionary(renamed_files):
  ret = {}
  for _ in renamed_files:
    tmp = _[:4]
    tmp = tmp.replace("_","").strip().replace(")","").replace("(","").replace("-","")
    value = _[4:-4].strip().replace("_", " ").strip("-").strip("-")
    ret[tmp] = value

  print("fileNames = ")
  print(ret)


def main():
  msg = "Do you want to add an iterator to the beginning of original file names?\n[TYPE 1]\nOr do you want to rename the files with the iterator?\n[TYPE 2]\n"
  decision = int(input(msg))
  while decision != 1 and decision != 2:
    decision = int(input(msg))
  if decision == 2:
    id = input("Type Word to Start all file namees with (before the iterator\n")
  vid_list = get_file_list()
  if decision == 1:
    new_list = add_iterator(vid_list)
  else:
    new_list = replace_w_iter(vid_list, id)
  rename(vid_list, new_list)

  updated_list = get_file_list()
  create_name_dictionary(updated_list)


def create_dictionary_ONLY():
  vid_list = get_file_list()
  create_name_dictionary(vid_list)


if __name__ == "__main__":
  #main()
  create_dictionary_ONLY()