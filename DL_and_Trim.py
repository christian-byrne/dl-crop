
# ────────────────────────────────────────────────────────────────────────────────
# ─── SOURCES ────────────────────────────────────────────────────────────────────
# ────────────────────────────────────────────────────────────────────────────────

### Flask Docs:       https://flask.palletsprojects.com/en/1.1.x/api/
### Selenium Methods: https://www.selenium.dev/selenium/docs/api/py/webdriver_remote/selenium.webdriver.remote.webelement.html
###                   https://www.selenium.dev/selenium/docs/api/java/org/openqa/selenium/WebElement.html

from flask import Flask, request, send_from_directory, render_template, jsonify
import os, webbrowser, glob, sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import indexer
import json
from indexer import create_dirs

#app = Flask('_BYMYself')
app = Flask(__name__.split('.')[0])

# DEVMODE - SELENIUM TESTING
#dp = "/home/bymyself/Desktop/trim_wrapper/webdrivers/chrome/88.0.4324.96/chromedriver"
#os.chmod(dp, 755)
#driver = webdriver.Chrome(executable_path=dp)
#driver.get("https://www.youtube.com/watch?v=2tGlaSFyZPw")


# ────────────────────────────────────────────────────────────────────────────────
# ─── INITIALIZE SELENIUM ────────────────────────────────────────────────────────
# ────────────────────────────────────────────────────────────────────────────────


usr_spec = {
    "app_path": os.getcwd(),
    "default_browser": "chrome",
    "driver_names": ["chromedriver","firefoxdriver","edgedriver"],
    "versions": [],
    "try_files": [],
    "os": sys.platform,
    "on_extensions": [],
    "off_extensions": [],
    "saved_session": None }


def get_version_files():
    usr_spec["versions"] = os.listdir(usr_spec["app_path"] + "/webdrivers/" +\
        usr_spec["default_browser"])

    for version in usr_spec["versions"]:
        # Get driver files for each version
        cd = usr_spec["app_path"] + "/webdrivers/" +\
        usr_spec["default_browser"] + "/" + str(version)

        # Contents of path/webdrivers/browser/version for curr version iteration
        d = os.listdir(cd)

        # Check if unzipped version already exists in d
        passed = False
        for possible_name in usr_spec["driver_names"]:
            if possible_name in d:
                usr_spec["try_files"].append(cd + "/" + possible_name)
                passed = True
        
        # If unzipped not there, find correct zipped version for this OS
        if not passed:
            for fi in d:
                if usr_spec["os"] in fi:
                    usr_spec["try_files"].append(cd + "/" + fi)
                    continue


def check_zip(fpath):
    if ".zip" in fpath:
        cd = os.path.dirname(fpath)
        import zipfile
        with zipfile.ZipFile(fpath, 'r') as zip_ref:
            zip_ref.extractall(cd)
        list_of_files = glob.glob(cd + '/*')
        latest_file = max(list_of_files, key=os.path.getctime)
        return latest_file
    return fpath 


def try_driver(driver_path, browser):
    global driver

    # Set permissions for relative driver path
    os.chmod(driver_path, 755)

    if browser == "chrome":
        driver_path = check_zip(driver_path)
        # TODO pass browser choice to init_options
        o = init_options()
        driver = webdriver.Chrome(executable_path=driver_path, chrome_options=o)

    # TODO other browsers


def txt_val(text):
    delete = ["'", '"', "\n"]
    strip = ["[","]"," ","{","}"]
    ret = text
    for char in delete:
        ret = ret.replace(char,"")
    for _ in range(3):
        for char in strip:
            ret = ret.strip(char)
    ret = ret.replace("%20", " ")
    return ret


def init_options():
    """
    initialize chrome_options object and return it.
    Shift elements in on_extensions and off_extensions to change user settings.
    Attributes: '_binary_location', '_arguments', '_extension_files', 
                '_extensions', '_experimental_options', 
                '_debugger_address', '_caps
    """
    from selenium.webdriver.chrome.options import Options
    usr_options = webdriver.ChromeOptions() 

    on_extensions = ["ublock.crx"]
    off_extensions = ["canvas_blocker.crx", "torrent.crx", "session_buddy.crx", "geo_bypass.crx", \
        "remove_tracking_URLS.crx", "archive.crx", "age_restriction.crx", "URL_cleaner.crx", "auto_https.crx", "privacy_badger.crx"]
    
    d = os.getcwd() + "/chrome_extensions/"
    for crx in os.listdir(d[:-1]):
        if crx in on_extensions:
            usr_spec["on_extensions"].append(d + crx)
            usr_options.add_extension(d + crx)
        if crx in off_extensions:
            usr_spec["off_extensions"].append(d + crx)

    return usr_options


def launch_selenium():
    global driver
    global usr_spec

    # if there is alredy a selenium instance running
    try:
        if driver.title:
            return None
    except:
        pass 

    try:
        cookies = open("cookies.txt", "r")
        lines = cookies.readlines()
    except:
        cookies = open("cookies.txt" "w")
        lines = []
    last_site = []

    # Check if a previous user with stored data
    if len(lines) > 4:
        for index, _ in enumerate(usr_spec.keys()):
            # Store arrays from saved user specs
            if type(usr_spec[_]) == list:
                for item in lines[index].split(","):
                    usr_spec[_].append(txt_val(item))
            # Store strings from saved user specs
            else:
                usr_spec[_] = txt_val(lines[index])
        for _ in range(5,len(lines)):
            if "https://www." in lines[_]:
                last_site.append(txt_val(lines[_]))
        for index, p in enumerate(usr_spec["try_files"]):
            try:
                print("TRIED DRIVER PATH FROM USR STORAGE (cookies.txt):  " + p)
                try_driver(p, "chrome")
                break
            except:
                if index == len(usr_spec["try_files"]) - 1:   # If none work
                    # Clear cookies, make new blank, reset usr_spec dictionary, restart
                    cookies.close(); os.remove("cookies.txt")
                    cookies = open("cookies.txt", "w"); cookies.close()
                    usr_spec = {"app_path":os.getcwd(),"default_browser":"chrome",
                    "driver_names": ["chromedriver","firefoxdriver","edgedriver"],
                    "versions":[],"try_files":[],"os":sys.platform,"saved_session":None}
                    return launch_selenium()
                else:
                    pass
        # Remove try_files elements that didn't work so user skips them next time
        for _ in range(0, index):
            usr_spec["try_files"].pop(_)
        
    # First time user
    else:
        get_version_files()
        for index, p in enumerate(usr_spec["try_files"]):
            try:
                try_driver(p, "chrome")
                break
            except:
                pass
        # Remove try_files elements that didn't work so user skips them next time
        for _ in range(0, index):
            usr_spec["try_files"].pop(_)
        # Create user data cookies file
        cookies.close()
        os.remove("cookies.txt")
        cookies = open("cookies.txt", "w")
        for _ in usr_spec.keys():
            cookies.write(str(usr_spec[_]) + "\n")

        # ___DEVMODE___
        print("\n\n\n\nNEW USER SPECS SAVED:\n")
        for key in usr_spec.keys():
            print(str(key) + " User Spec:")
            print(usr_spec[key])
        print("\n\n\n\n")

    if not last_site:
        driver.get("https://www.youtube.com")
    else:
        last_site.reverse()
        for index, site in enumerate(last_site):
            print("[ATTEMPT " + str(index+1) + "] Loading Site from Last Session:\n" + str(site))
            try:
                driver.get(site)
                break
            except:
                if index == len(last_site) - 1 or index > 15:
                    print("Loading Default Site")
                    driver.get("https://www.youtube.com")
    
    cookies.close()


# ────────────────────────────────────────────────────────────────────────────────
# ─── GET TIME CODES ─────────────────────────────────────────────────────────────
# ────────────────────────────────────────────────────────────────────────────────


VideoNodes = {
    "node": [],
    "start": [],
    "end": [],
    "url": [],
    "width": [],
    "height": [],
    "muted": [],
    "iframe": [],
    "vidTitle":[] }

usrSelection = {
    "url": [],
    "start": [],
    "end": [],
    "title": []
}

usrHistory = {
    "url": [],
    "clip": [],
    "title": [],
    "stored": []
}

savedLater = {
    "url": [],
    "start": [],
    "end": [],
    "title": []
}


def reset_video_nodes():
    global VideoNodes
    VideoNodes = {
    "node": [],
    "start": [],
    "end": [],
    "url": [],
    "width": [],
    "height": [],
    "muted": [],
    "iframe": [],
    "vidTitle":[] }


def correct_vid_index():
    """
    Determines which of the components in the VideoNodes object is the 
    node the user is actually trying to record the times for.
    Returns the index of the correct video or 
    False if there is no acceptable video provided.
    """
    if len(VideoNodes["start"]) == 1:
        return 0

    candidates = []
    for index, _ in enumerate(VideoNodes["start"]):
        candidates.append(index)

    # (1) start time = end time
    if len(candidates) > 1:    
        for index, _ in enumerate(VideoNodes["start"]):
            if _ == VideoNodes["end"][index]:
                candidates.pop(index)     

    # (2) end time = 0
    if len(candidates) > 1:    
        for index, _ in enumerate(VideoNodes["end"]):
            if _ == 0:
                candidates.pop(index)    

    # (3) start times differ and some are 0
    if len(candidates) > 1:
        # If one time > 0
        if float(max(VideoNodes["start"])) > .1:
            #  Pop the ones that ARE 0
            for index, _ in enumerate(VideoNodes["start"]):
                if _ == 0:
                    candidates.pop(index)  

    # (4) if the same crop record already exists
    if len(candidates) > 1:
        try:
            for index, _ in enumerate(VideoNodes["start"]):
                if _ in usrSelection:
                    i = usrSelection.index(_)
                    if VideoNodes["end"][index] == usrSelection[i+1] and VideoNodes["url"][index] == usrSelection[i-1]:
                        candidates.pop(index)
        except:
            print("error on video validation test 4")

    # (5) height and width = 0
    if len(candidates) > 1:
        try:
            # If not all dimensions are 0
            if float(max(VideoNodes["width"])) > 0 and float(max(VideoNodes["height"])) > 0:
                #  Pop the ones that ARE 0
                for index, _ in enumerate(VideoNodes["width"]):
                    if float(_) == 0 and float(VideoNodes["height"][index]) == 0:
                        candidates.pop(index)  
        except:
            print("error on video validation test 5")

    # (6) height OR width = 0 and muted
    if len(candidates) > 1:
        try:
            # If not all dimensions are 0
            if float(max(VideoNodes["width"])) > 0 and float(max(VideoNodes["height"])) > 0:
                for index, _ in enumerate(VideoNodes["width"]):
                    if float(_) == 0 and VideoNodes["muted"][index] == True:
                        candidates.pop(index) 
                    if float(VideoNodes["height"][index]) == 0 and VideoNodes["muted"][index] == True:
                        candidates.pop(index) 
        except:
            print("error on video validation test 6")

    # (7) largest dimensions
    if len(candidates) > 1:
        try:
            # If not all dimensions are 0
            if float(max(VideoNodes["width"])) > 0 and float(max(VideoNodes["height"])) > 0:
                if VideoNodes["width"].index(min(VideoNodes["width"])) == VideoNodes["height"].index(min(VideoNodes["height"])):
                    candidates.pop(VideoNodes["width"].index(min(VideoNodes["width"])))
        except:
            print("error on video validation test 7")

    # (8) not muted vs. muted
    if len(candidates) > 1:
        try:
            if False in VideoNodes["muted"] and True in VideoNodes["muted"]:
                for index, _ in enumerate(VideoNodes["muted"]):
                    if _ == True:
                        candidates.pop(index) 
        except:
            print("error on video validation test 8")

    if not candidates:
        return False
    return candidates[0]


def end_code():
    # Check if supposed to be start_code
    if not VideoNodes["node"]:
        return by_frame()

    for index, vid in enumerate(VideoNodes["node"]):
        driver.switch_to_default_content()

        # If in iframe
        if VideoNodes["iframe"][index] != "no":
            f = driver.find_elements_by_tag_name('iframe')[VideoNodes["iframe"][index]]
            driver.switch_to.frame(f)

        try:            
            VideoNodes["end"].append(vid.get_attribute("currentTime"))
        except:            
            VideoNodes["end"].append(False)
    driver.switch_to_default_content()
    cookies = open("cookies.txt", "a")
    cookies.write("\n" + str(VideoNodes["url"][0]))
    cookies.close()

    # ___DEVMODE___
    for key in VideoNodes.keys():
        print(str(key) + " Array:")
        print(VideoNodes[key])

    # Get index of validated video node
    correct = correct_vid_index()
    # Log the user selection if a vid can be validated
    if correct:
        usrSelection["url"].append(VideoNodes["url"][correct])
        usrSelection["start"].append(VideoNodes["start"][correct])
        usrSelection["end"].append(VideoNodes["end"][correct])
        usrSelection["title"].append(VideoNodes["vidTitle"][correct])
    # Reset video nodes object
    reset_video_nodes()

    # ___DEVMODE___
    print("\nUSER SELECTION LIST:\n")
    print(usrSelection["url"])
    print(usrSelection["start"])
    print(usrSelection["end"])


def find_video_nodes():
    vid_list = []
    for _ in ["video", "vid", "player", "jsplayer", "object", "embed"]:
        try:
            vid_list += driver.find_elements_by_tag_name(_)
        except:
            continue
    for _ in ["main-video", "main-video-player"]:
        try:
            x = driver.find_elements_by_class_name(_)
            for ret in x:
                if ret not in vid_list:
                    try:
                        vid_list.append(ret)
                    except:
                        continue
        except:
            continue

    return vid_list


def find_page_title():
    #candidates = []
    #tags = ["title", "head", "metaname", "Title"]
    #for _ in tags:
    #    try:
    #        candidates.append(driver.#find_elements_by_tag_name(_))
    #    except:
    #        continue
    #i = 0
    #ret = False
    #while not ret and i < len(candidates) - 1:
    #    try:
    #        ret = str(candidates[i].get_attribute#('innerHTML')).replace("<","").replace(">","").#strip()
    #    except:
    #        i += 1
    #        continue
    #
    #if not ret:
    #    ret = "Can't Parse Title"
    return driver.title
    

def start_code(iframeN, cURL):
    VideoNodes["vidTitle"].append(find_page_title())
    print(VideoNodes["vidTitle"])

    for vid in find_video_nodes():
        VideoNodes["node"].append(vid)
        VideoNodes["url"].append(cURL)
        VideoNodes["iframe"].append(iframeN)
        try:
            VideoNodes["start"].append(vid.get_attribute("currentTime"))
        except:
            VideoNodes["start"].append(False)
        try:    
            VideoNodes["width"].append(vid.get_attribute("videoWidth"))
        except:    
            VideoNodes["width"].append(False)
        try:   
            VideoNodes["height"].append(vid.get_attribute("videoHeight"))
        except:   
            VideoNodes["height"].append(False)
        try:
            # if muted returns true(js), append False for easier checking later on
            _ = not vid.get_attribute("muted")
            VideoNodes["muted"].append(_)
        except:    
            VideoNodes["muted"].append(False)


def by_frame():
    u = driver.current_url

    # Update usr saved session cookie for next app use
    usr_spec["saved_session"] = u

    # Top Frame (no iframe)
    start_code("no", u)

    # FINDING IFRAMES:
    ifl = driver.find_elements_by_tag_name('iframe')
    for index, iframe in enumerate(ifl):
        try:
            driver.switch_to_default_content()
            driver.switch_to.frame(iframe)
            start_code(index, u)
        except:
            continue

    # ___DEVMODE___
    print("\n\n\n\nPARSED VIDEO NODES:\n")
    print(VideoNodes)
    print("\n\n\n")





# ────────────────────────────────────────────────────────────────────────────────
# ─── FLASK ROUTERS ──────────────────────────────────────────────────────────────
# ────────────────────────────────────────────────────────────────────────────────

# https://flask.palletsprojects.com/en/1.1.x/api/

@app.route('/')
def hello():
    return render_template("DL_and_Trim_pages/DLqueue.html", usrSelection=usrSelection, usrHistory=usrHistory, savedLater=savedLater)


@app.route('/launchS')
def launchS():
    launch_selenium()
    

@app.route('/recordS')
def recordS():
    by_frame()
    return jsonify({
        "iterator": len(usrSelection["end"]),
        "title": VideoNodes["vidTitle"][0],
        "url": VideoNodes["url"][0],
        "start": VideoNodes["start"][0][:-2],
        #TODO add a validation function that validates start times only so the wrong start time is not passed to front end   
    })


@app.route('/recordE')
def recordE():
    end_code()
    return jsonify({
        "start": usrSelection["start"][len(usrSelection["start"])-1][:-2],
        "end": usrSelection["end"][len(usrSelection["end"])-1][:-2],
        "divEnd": "#e" + str(len(usrSelection["end"])-1),
        "divStart": "#s" + str(len(usrSelection["end"])-1)
    })


@app.route('/openVid')
def ov():
    by_frame()
    return jsonify({
        "iterator": len(usrSelection["end"]),
        "title": VideoNodes["vidTitle"][0],
        "url": VideoNodes["url"][0],
        "start": VideoNodes["start"][0][:-2],
        #TODO add a validation function that validates start times only so the wrong start time is not passed to front end   
    })


@app.route('/player')
def pl():
    # TODO if user cookies indicate it's a new direcotry, run the check for quotes / apostrophes in file names
    # TODO way to quickly check if new thumbnails ar eneeded
    dirs = json.dumps(create_dirs("static/userLibrary/Plumber_Clips"))
    return render_template("Player/BymyselfPlayer.html", directories=dirs)


if __name__ == '__main__':
    #os.chdir("/home/bymyself/_BYMYself/bmp")
    app.run(debug=False)