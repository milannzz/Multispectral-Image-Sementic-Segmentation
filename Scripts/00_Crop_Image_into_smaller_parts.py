import PIL
from PIL import Image

PIL.Image.MAX_IMAGE_PIXELS = 923711251

file_location = r'Images\extbymask.tif'
save_location = r"Temp_Data"
chopsize = 64

img = Image.open(file_location)
width, height = img.size

count = int(0)

# Save Chops of original image
for x0 in range(0, width, chopsize):
   for y0 in range(0, height, chopsize):
      box = (x0, y0,
             x0+chopsize if x0+chopsize <  width else  width - 1,
             y0+chopsize if y0+chopsize < height else height - 1)
      print('%s %s' % (file_location, box))
      img.crop(box).save(save_location + '/' + str(count) + '.png')
      count = count + 1