from osgeo import gdal
import numpy as np
import skimage
from skimage.io import imread
from numpy import pad
from tensorflow.keras.models import load_model
from tqdm import tqdm


# input files
path_to_image = r"Images\10_bands_2.tif"
path_to_model = r"Temp_Models\10_band_Models\vgg_ms_from_scratch_final.15-0.742.hdf5"

# output files
path_to_label_image = r"H:\Multi-Spectral-Satelite-Image-Classification\Temp_Output\vgg_10_bands_labels_5.tif"
path_to_prob_image = r"H:\Multi-Spectral-Satelite-Image-Classification\Temp_Output\vgg_10_bands_probabilities_5.tif"

# read image and model
image = np.array(imread(path_to_image), dtype=float)

_, num_cols_unpadded, _ = image.shape
model = load_model(path_to_model)

print("-------------------------------------------------------------")

print(image.shape)

print(model.layers[0].input_shape)

print(model.layers[-1].output_shape)

# get input shape of model
_, input_rows, input_cols, input_channels = model.layers[0].input_shape[0]
_, output_classes = model.layers[-1].output_shape
in_rows_half = int(input_rows/2)
in_cols_half = int(input_cols/2)

print("Input row: " + str(input_rows))
print("Input Col: " + str(input_cols))
print("Input Channels: " + str(input_channels))
print("Output Classes: " + str(output_classes))

# import correct preprocessing
if input_channels == 3:
    from image_functions import preprocessing_image_rgb as preprocessing_image
else:
    from image_functions import preprocessing_image_ms as preprocessing_image

# pad image
image = pad(image, ((input_rows, input_rows),
                    (input_cols, input_cols),
                    (0, 0)), 'symmetric')

# don't forget to preprocess
image = preprocessing_image(image)
num_rows, num_cols, _ = image.shape
print("No of row: " + str(num_rows))
print("No of Col: " + str(num_cols))

# sliding window over image
image_classified_prob = np.zeros((num_rows, num_cols, output_classes))
row_images = np.zeros((num_cols_unpadded, input_rows,
                       input_cols, input_channels))

print(input_rows, num_rows-input_rows)
for row in tqdm(range(input_rows, num_rows-input_rows), desc="Processing..."):
    # get all images along one row
    for idx, col in enumerate(range(input_cols, num_cols-input_cols)):
        # cut smal image patch
        row_images[idx, ...] = image[row-in_rows_half:row+in_rows_half,
                                     col-in_cols_half:col+in_cols_half, :]
    # classify images
    row_classified = model.predict(row_images, batch_size=1024, verbose=0) 
    # put them to final image
    image_classified_prob[row, input_cols:num_cols-input_cols, : ] = row_classified


# crop padded final image
image_classified_prob = image_classified_prob[input_rows:num_rows-input_rows,
                                              input_cols:num_cols-input_cols, :]
image_classified_label = np.argmax(image_classified_prob, axis=-1)
image_classified_prob = np.sort(image_classified_prob, axis=-1)[..., -1]

# write image as Geotiff for correct georeferencing
# read geotransformation
image = gdal.Open(path_to_image, gdal.GA_ReadOnly)
geotransform = image.GetGeoTransform()

# create image driver
driver = gdal.GetDriverByName('GTiff')
# create destination for label file
file = driver.Create(path_to_label_image,
                     image_classified_label.shape[1],
                     image_classified_label.shape[0],
                     1,
                     gdal.GDT_Byte,
                     ['TFW=YES', 'NUM_THREADS=1'])
file.SetGeoTransform(geotransform)
file.SetProjection(image.GetProjection())

# write label file
file.GetRasterBand(1).WriteArray(image_classified_label)
file = None

# create destination for probability file
file = driver.Create(path_to_prob_image,
                     image_classified_prob.shape[1],
                     image_classified_prob.shape[0],
                     1,
                     gdal.GDT_Float32,
                     ['TFW=YES', 'NUM_THREADS=1'])
file.SetGeoTransform(geotransform)
file.SetProjection(image.GetProjection())
# write label file
file.GetRasterBand(1).WriteArray(image_classified_prob)
file = None
image = None
print("-------------------------------------------------------------")
print("                     DONE                                    ")
print("-------------------------------------------------------------")