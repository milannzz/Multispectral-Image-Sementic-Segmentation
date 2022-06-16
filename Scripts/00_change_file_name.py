import os

folder = r"H:\DEEP LEARNING BASED BUILT-UP EXTRACTION USING MULTISPECTRAL SATELLITE IMAGERY\Dataset\_temp\Dataset"

for filename in os.listdir(folder):
    count = 1
    for count , files in enumerate(os.listdir(str(folder) + "\\" + str(filename))):
        src = str(str(folder) + "\\" + str(filename) + "\\" + files)
        dst = str(str(folder) + "\\" + str(filename) + "\\" + filename + '_' + str(count) + '.tif')
        os.rename(src, dst)
        count += 1
print("Done")