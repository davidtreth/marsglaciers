import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.cm as cm
import glob
import Image

DTMs = glob.glob("*DTM*2.png")

for d in DTMs:
    img = Image.open(d)
    #img.show()
    im_arr = np.asarray(img)
    im_arr = im_arr.astype(np.float32) # convert to int
    im_arr -= im_arr.min() # ensure the minimal value is 0.0
    im_arr /= im_arr.max() # maximum value in image is now 1.0
    im = Image.fromarray(np.uint8(cm.magma(im_arr)*255))
    #im.show()
    #d2 = d[:-4] + "_magma.png"
    im.save(d)
    #r = raw_input()

    
    #img = mpimg.imread(d)
    #fig = plt.figure()
    #axes = plt.gca()
    
    #imgplot=plt.imshow(img)
    #x,y = imgplot.get_size()
    #fx = x / 100.0
    #fy = y / 100.0
    #fig.set_size_inches(fx, fy, forward=True)
    #imgplot.set_cmap('magma')
    #axes.set_axis_off()
    #d2 = d[:-4] + "_magma.png"
    #fig.savefig(d2, dpi='figure', transparent=True, bbox_inches='tight', pad_inches=0)
    #fig.clf()
    #plt.show()
