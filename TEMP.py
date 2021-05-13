
# ────────────────────────────────────────────────────────────────────────────────
# ─── SOURCES ────────────────────────────────────────────────────────────────────
# ────────────────────────────────────────────────────────────────────────────────

### Flask Docs:       https://flask.palletsprojects.com/en/1.1.x/api/
### Selenium Methods: https://www.selenium.dev/selenium/docs/api/py/webdriver_remote/selenium.webdriver.remote.webelement.html
###                   https://www.selenium.dev/selenium/docs/api/java/org/openqa/selenium/WebElement.html

from flask import Flask
import os, webbrowser, glob, sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

DL_and_Trim_html = "static_pages/DL_and_Trim_pages/GUI_html.html"
DL_and_Trim_header = "static_pages/DL_and_Trim_pages/GUI_head.html"

html = open(DL_and_Trim_html).read()
header = open(DL_and_Trim_header).read()

app = Flask('_BYMYself')
app = Flask(__name__.split('.')[0])

# DEVMODE - SELENIUM TESTING
#dp = "/home/bymyself/Desktop/trim_wrapper/webdrivers/chrome/88.0.4324.96/chromedriver"
#os.chmod(dp, 755)
#driver = webdriver.Chrome(executable_path=dp)
#driver.get("https://www.youtube.com/watch?v=2tGlaSFyZPw")

# TODO set up chrome crx files (1) ublock origin (2) privacy badger (3) session buddy (4) other ones in 12064
# TODO get crx-equivalent files for other browsers

# TODO check if better quality version available
# TODO check if torrent avaialble -> [use torrenting crx webapp?]
# TODO check if free download available

# TODO whole video mode
# TODO playlist mode
# TODO channel mode

# TODO add chrome_options to make the selelnium instance match the GUI
# TODO thumbnail parser
# TODO: if video player current time has a value, while True, constantly update a GUI element displyaing the time using vHS clock assets
# TODO subtitle DL option
# TODO all youtube-dl optional agumnets in GUI

# TODO session budy / get all tabs functino via webbrowser / get all tabs function via selenium

# TODO Options for other browsers (1) in try_driver



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

    on_extensions = ["ublock.crx", "auto_https.crx", "privacy_badger.crx"]
    off_extensions = ["canvas_blocker.crx", "torrent.crx", "session_buddy.crx", "geo_bypass.crx", \
        "remove_tracking_URLS.crx", "archive.crx", "age_restriction.crx", "URL_cleaner.crx"]
    
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
    "iframe": [] }


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


def start_code(iframeN, cURL):
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
# ─── CALLBACK GUI FUNCTIONS ─────────────────────────────────────────────────────
# ────────────────────────────────────────────────────────────────────────────────


def ac_connect(dom):
    """ Initialize Atlas -- Required """
    dom.inner("", html)
    dom.focus("input")


def time_btn(dom, id):
    indic = ["Get Started", "Record Start Time", "Record End Time"]
    msg = dom.get_value(id)
    if msg != indic[0]:
        if msg == indic[1]:
            dom.set_value(id, indic[2])
            by_frame()
        else:
            dom.set_value(id, indic[1])
            end_code()
    else:
        dom.set_value(id, indic[1])
        launch_selenium()
    


# def ac_submit(dom):
#   dom.alert("Hello, " + dom.get_value("input") + "!")
#   dom.focus("input")
# 
# def ac_clear(dom):
#   if ( dom.confirm("Are you sure?") ):
#     dom.set_value("input", "")
#   dom.focus("input")


# ────────────────────────────────────────────────────────────────────────────────
# ─── ATLAS INITIALIZATION ───────────────────────────────────────────────────────
# ────────────────────────────────────────────────────────────────────────────────


#  html tag: data-xdh-onevent="callback"
# callbacks(DOM-object, id of element which receives the event, action label)

callbacks = {
  "": ac_connect,  # The action label for a new connection is an empty string.
  "time_btn": time_btn
}

# launch(callbacks,createCallback=None,headContent="")
atlastk.launch(callbacks, None, header)