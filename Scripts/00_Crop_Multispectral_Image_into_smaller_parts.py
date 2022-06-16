from osgeo import gdal

filepath = r'Raw_Images\noida_full.tif'
dataset = gdal.Open(filepath)
width = dataset.RasterXSize
height = dataset.RasterYSize
tilesize = 64
count = 0
for i in range(0, width, tilesize):
    for j in range(0, height, tilesize):
        gdal.Translate('Split_images_test\\' + str(count) + '.tif', filepath, srcWin = (i, j, tilesize, tilesize))
        count += 1
