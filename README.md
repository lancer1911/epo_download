# epo_download
<b><font color="blue">Batch download patents and/or applications from worldwide.espacenet.com. NO NEED FOR EPO OPS.</font></b><br>
written by lancer1911<br>
May 20, 2018

<b>Usage:</b><br>
python epo_download.py option PatentNumber<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;option: -n, or -l<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;PatentNumber: [-n] patent numbers seperated by comma, or [-l] text file

<b>Examples:</b><br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Example 1: python epo_download.py -n WO2009012346,CN101208412A,WO2009012347A1<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Example 2: python epo_download.py -l list.txt

<b>content of list.txt:</b><br>
WO2009012346<br>
CN101208412A<br>
WO2009012347A1<br>

# Requirements (MacOS as an example)
<b>Python 3</b> for Mac OS X<br>
https://www.python.org/downloads/mac-osx/<br>

<b>Brew</b>, if not installed<br>
https://brew.sh/ <br>
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"<br>

<b>Tesseract</b><br>
brew install tesseract<br>

<b>ChromeDriver</b><br>
http://chromedriver.chromium.org/downloads, e.g.<br>
https://chromedriver.storage.googleapis.com/index.html?path=2.38/<br>
extract chromedriver_mac64.zip to /usr/local/bin

<b>Pip</b>, if not installed<br>
sudo easy_install pip<br>

<b>PIL</b><br>
pip install pillow<br>

<b>pytesseract</b><br>
pip install pytesseract<br>

<b>Selenium</b><br>
pip install selenium<br>

<b>tqdm</b><br>
pip install tqdm<br>
