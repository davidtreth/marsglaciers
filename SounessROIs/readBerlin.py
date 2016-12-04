from bs4 import BeautifulSoup
from urllib import urlopen
import time
import random

def waittime(minw=1, maxw = 10):
    time.sleep(1 + maxw*random.random())    

def getAreoidDTMres(urlBerlin):
    waittime()
    print("Calling Berlin: {u}".format(u=urlBerlin))
    raw = urlopen(urlBerlin).read()
    soup = BeautifulSoup(raw,"lxml")
    trows = soup.table.find_all("tr")
    for t in trows:
        if "areoid" in t.contents[0].string:
            res = float(t.contents[1].string.strip())
            print("resolution: {r}m".format(r=res))
            return res

    

#urlBerlin = "http://hrscview.fu-berlin.de/cgi-bin/ion-p?page=product2.ion&code=&image=2083_0000"
