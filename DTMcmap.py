import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import glob

DTMs = glob.glob("*DTM*png")

for d in DTMs:
    img = mpimg.imread(d)
    fig, axes = plt.subplots(1)
    
    imgplot=plt.imshow(img)
    imgplot.set_cmap('magma')


    axes.set_axis_off()
    plt.savefig(d, transparent=True)
    fig.clf()
    #plt.show()
