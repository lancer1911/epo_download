"""
Batch download patents and/or applications from worldwide.espacenet.com
written by lancer1911
May 20, 2018

Usage: python epo_download.py option PatentNumber
    option: -n, or -l
    PatentNumber: [-n] patent numbers seperated by comma, or [-l] text file

Example 1: python epo_download.py -n WO2009012346,CN101208412A,WO2009012347A1
Example 2: python epo_download.py -l list.txt

content of list.txt:
WO2009012346
CN101208412A
WO2009012347A1
    
"""

from PIL import Image
import sys
import argparse
import pytesseract
import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By
import os
from io import BytesIO
import tkinter as tk
from tkinter import filedialog
from os import path
from tqdm import tqdm

root = tk.Tk()
root.withdraw()

# specifies the path of tesseract, if not in %PATH%
#pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
if not "tesseract" in os.environ["PATH"]:
    os.environ["PATH"] = os.environ["PATH"] + ";C:\\Program Files (x86)\\Tesseract-OCR"
    os.environ["TESSDATA_PREFIX"] = "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"

# initializes webdriver
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
options.add_argument("--disable-infobars")  #removing infobar "chrome is controlled by automated ..."
options.binary_location = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"

Usage = "\nUsage: python epo_download.py option PatentNumber\n\
    option: -n, or -l \n    PatentNumber: [-n] patent numbers seperated by comma, or [-l] text file\n\n\
Example 1: python epo_download.py -n WO2009012346,CN101208412A,WO2009012347A1\n\
Example 2: python epo_download.py -l list.txt\n\n\
content of list.txt:\nWO2009012346\nCN101208412A\nWO2009012347A1"

def get_captcha(driver, element, path):
    location = element.location
    size = element.size

    # saves screenshot of entire page
    #driver.save_screenshot(path)
    png = driver.get_screenshot_as_png()
    
    # uses PIL library to open image in memory
    #image = Image.open(path)
    image = Image.open(BytesIO(png))
    
    # IMPORTANT! resize the image to the resolution of the browser, from those of the screen
    image = image.resize((driver.execute_script('return window.innerWidth;'), driver.execute_script('return window.innerHeight;')))
       
    left = location['x'] 
    top = location['y'] 
    right = location['x'] + size['width'] 
    bottom = location['y'] + size['height'] 

    image = image.crop((left, top, right, bottom))  # defines crop points

    #image.save(path, 'png')  # saves new cropped image, for debugging
    return pytesseract.image_to_string(image, lang='eng',\
           config='--psm 6 outputbase nobatch digits')

def every_downloads_chrome(driver):
    driver.maximize_window()
    if not driver.current_url.startswith("chrome://downloads"):
        driver.get("chrome://downloads/")
    return driver.execute_script("""
        var items = downloads.Manager.get().items_;
        if (items.every(e => e.state === "COMPLETE"))
            return items.map(e => e.file_url);
        """)

def highlight(driver,element):
    """Highlights (blinks) a Selenium Webdriver element"""
    def apply_style(s):
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                              element, s)
    original_style = element.get_attribute('style')
    #apply_style("background: yellow; border: 2px solid #eea0a0;@-webkit-keyframes blink { from { opacity: 1; } to { opacity: 0; } }")
    time.sleep(.3)
    apply_style("filter: invert(100%);")
    time.sleep(.3)
    apply_style(original_style)

def specify_file(arg1,arg2,arg3):
    file_path = None
    while not file_path:
       file_path= filedialog.askopenfilename(initialdir = arg1, title = arg2, filetypes = arg3)
       if file_path:
           return file_path
    
arg_names = ['command', 'option', 'filename']
args = dict(zip(arg_names, sys.argv))

d = path.dirname(__file__)

try:
    if args['option'] == "-n" and args['filename'] != None:
        CC_NR = args['filename'].split(',') # splits string (argument in command line) by comma
    elif args['option'] == "-l" and args['filename'] != None:
        with open(args['filename']) as f:
            CC_NR = f.read().splitlines() # splits string from the text file
    else:
        print(Usage)
        sys.exit()
except KeyError:
    #print(Usage)
    filename = specify_file(path.join(d, './'), 'Select TEXT file containing the patent/application numbers', (('text files','*.txt'),('all files','*.*')))
    with open(filename) as f:
        CC_NR = f.read().splitlines() # splits string from the text file
    #sys.exit()

driver = webdriver.Chrome(chrome_options=options)
driver.set_window_size(480, 450)
driver.set_window_position(20, 20)


for i in CC_NR:
    
    print(str("\nDownloading " + i + " from:"))

    # extracts CC, NR and KC from each patent number, KC may be absent
    CC = i[:2]
    NR = i[2:]
    for j in range(-1,-3,-1):  # reads the last two letters, to find if alphabet occurs
        if i[j].isalpha() == True:
            KC = i[j:]
            NR = i[2:j]
            break
    else:
        KC = None

    # generates URL based on CC, NR and KC, if any
    URL = str("https://worldwide.espacenet.com/data/espacenetDocument.pdf?flavour=trueFull&CC=" \
              + CC + "&NR=" + NR)
    if KC != None:
        URL = str(URL + "&KC=" + KC)
    
    print(URL)
    driver.get(URL)

    count = 0
    while True:
        count += 1
        captcha_text = captcha_text1 = ""
        img = driver.find_element_by_id("watermark")
        highlight(driver,img)
        
        captcha_text = get_captcha(driver, img, "captcha.png")
        captcha_text = captcha_text.replace(" ", "")

        captcha_form = driver.find_element_by_id("response")
        captcha_form.send_keys(captcha_text)

        driver.find_element_by_id("submitBtnId").click()
    
        time.sleep(1)
        wait(driver, 10).until(EC.presence_of_element_located((By.ID, "watermark")))
    
        img1 = driver.find_element_by_id("watermark")
        captcha_text1 = get_captcha(driver, img1, "captcha1.png")
        captcha_text1 = captcha_text1.replace(" ", "")

        if captcha_text == captcha_text1:
            print(str("Captcha found after "+ str(count)+ " attempt(s)!"))

            print("\nTo prevent from blocking by the servers, we have to wait for 10 seconds.")
            for i in tqdm(range(10)):
                time.sleep(1)

            count = 0
            break

wait(driver, 120, 1).until(every_downloads_chrome)
print("\nDownload complete!\nThe patents/applications are now in your default download directory.")
driver.close()

