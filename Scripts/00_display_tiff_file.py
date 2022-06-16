from PIL import Image
im = Image.open(r'0_labels_5.tif')

import numpy
imarray = numpy.array(im)
for x in imarray:
    print(x)
