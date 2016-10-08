# This program uses matplotlib colour maps
# and the Image class of PIL
# to convert a grayscale DTM image to a
# pseudocolour version

import numpy as np
import matplotlib.cm as cm
import glob
import Image

# pattern for input files is curently hard-coded
DTMs = glob.glob("*DTM*2.png")

for d in DTMs:
    img = Image.open(d)
    #img.show()
    im_arr = np.asarray(img)
    im_arr = im_arr.astype(np.float32) # convert to int
    im_arr -= im_arr.min() # ensure the minimal value is 0.0
    im_arr /= im_arr.max() # maximum value in image is now 1.0
    # the 'magma' colourmap is hard-coded at the moment
    im = Image.fromarray(np.uint8(cm.magma(im_arr)*255))
    im.save(d)
