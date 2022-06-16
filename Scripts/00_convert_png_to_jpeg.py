from PIL import Image
import os

path = "Dataset\_temp\Dataset"

for folders in os.listdir(path):
    print(folders)
    for images in os.listdir(path + '\\' + folders):
        img_path = path + '\\' + folders + '\\' + images
        img = Image.open(img_path)
        rgb_img = img.convert('RGB')
        rgb_img.save(img_path.split('.')[0] + ".jpeg")