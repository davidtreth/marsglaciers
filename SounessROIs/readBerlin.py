from bs4 import BeautifulSoup
import sys
if sys.version_info[0] < 3:
	from urllib import urlopen
else:
	from urllib.request import urlopen
import time
import random

def waittime(minw=1, maxw = 10):
    time.sleep(minw + maxw*random.random())    

def getAreoidDTMres(urlBerlin):
    waittime()
    print("Calling Berlin: {u}".format(u=urlBerlin))
    try:
        raw = urlopen(urlBerlin).read()
    except:
        retries = 5
        print("reading url failed, retrying")        
        while retries > 0:            
            try:
                waittime()
                raw = urlopen(urlBerlin).read()            
                retries = 0
            except:
                retries -= 1
                if retries == 0:
                    print("run out of attempts")
    soup = BeautifulSoup(raw,"lxml")
    trows = soup.table.find_all("tr")
    for t in trows:
        if "areoid" in t.contents[0].string:
            res = float(t.contents[1].string.strip())
            print("resolution: {r}m".format(r=res))
            return res

    

#urlBerlin = "http://hrscview.fu-berlin.de/cgi-bin/ion-p?page=product2.ion&code=&image=2083_0000"
