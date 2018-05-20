# epo_download
<b><font color="blue">Batch download patents and/or applications from worldwide.espacenet.com</font></b><br>
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
