"""
Updated: Wanxue Zhu (wanxue.zhu@agr.uni-goettingen.de)
Date: 2024-Sep-02

DGPCM layer values:
description of bands:
0 -     weight (ha x 10)
1 -     Apples and other Fruits (share x 1000)
2 -     Barley (share x 1000)
3 -     Citrus Fruits (share x 1000)
4 -     Durum Wheat (share x 1000)
5 -     Flowers and ornamental plants (share x 1000)
6 -     Permanent grassland and meadows (share x 1000)
7 -     Maize (grain and green/silo) (share x 1000)
8 -     Rapeseed and turnip (share x 1000)
9 -     Nurseries (share x 1000)
10 -    Oats (share x 1000)
11 -    Other cereals (share x 1000)
12 -    Other permanent crops (share x 1000)
13 -    Other forage plants (share x 1000)
14 -    Other industrial plants (share x 1000)
15 -    Olive Plantations (share x 1000)
16 -    Rice (share x 1000)
17 -    Potatoes (share x 1000)
18 -    Pulses (share x 1000)
19 -    Fodder roots and brassicas (share x 1000)
20 -    Rye (share x 1000)
21 -    Soya (share x 1000)
22 -    Sugar beets (share x 1000)
23 -    Sunflowers (share x 1000)
24 -    Common wheat and spelt (share x 1000)
25 -    Other oil-seed or fibre crops (share x 1000)
26 -    Tobacco (share x 1000)
27 -    Fresh vegetables, melons, strawberries (share x 1000)
28 -    Vineyards (share x 1000)


4.1 - Separate different layers
Since the PCTM dataset contains 29 layers, 
with Layer 0 representing UAA and Layers 1-28 representing crop shares, 
we firstly separated them into individual layers
"""

import os
import glob
import rasterio
from rasterio.enums import Resampling

def extract_and_save_layers(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    geotiff_files = glob.glob(os.path.join(input_folder, '*.tif'))
    for geotiff_file in geotiff_files:
        with rasterio.open(geotiff_file) as src:
            num_layers = src.count
            base_filename = os.path.splitext(os.path.basename(geotiff_file))[0]
            layer_folder = os.path.join(output_folder, base_filename)
            if not os.path.exists(layer_folder):
                os.makedirs(layer_folder)
            for i in range(1, num_layers + 1):
                band = src.read(i)
                layer_filename = f"{base_filename}_layer_{i-1}.tif"
                layer_filepath = os.path.join(layer_folder, layer_filename)
                with rasterio.open(
                    layer_filepath,
                    'w',
                    driver='GTiff',
                    height=band.shape[0],
                    width=band.shape[1],
                    count=1,
                    dtype=band.dtype,
                    crs=src.crs,
                    transform=src.transform
                ) as dst:
                    dst.write(band, 1)
                print(f"Saved layer {i} of {geotiff_file} to {layer_filepath}")


input_folder = 'E:/01_Reseach_papers/FA_Pre_irrigation_grid_map/Data/PCTM_new'#delete this file
output_folder = 'E:/01_Reseach_papers/FA_Pre_irrigation_grid_map/Depository/Step_04'
extract_and_save_layers(input_folder, output_folder)

# Then mannually moved the UAA results to UAA_2010_2020 file.
# Naming as 'UAA_2010'...


# 4.2 Revise the maximum UAA as 100 hectare
import os
import numpy as np
import rasterio
from rasterio.enums import Resampling

def process_geotiff(input_path, output_path):
    with rasterio.open(input_path) as src:
        img_array = src.read(1) 
        img_array[img_array > 1000] = 1000
        metadata = src.meta.copy()
        metadata.update(dtype=rasterio.uint16)  
        with rasterio.open(output_path, 'w', **metadata) as dst:
            dst.write(img_array, 1)  

def process_all_geotiffs(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.tif') or filename.lower().endswith('.tiff'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            process_geotiff(input_path, output_path)


input_folder = r'E:\01_Reseach_papers\FA_Pre_irrigation_grid_map\Depository\Step_04\UAA_2010_2020'  
output_folder = r'E:\01_Reseach_papers\FA_Pre_irrigation_grid_map\Depository\Step_04\UAA_2010_2020_revised_100'  

process_all_geotiffs(input_folder, output_folder)


# 4.3 Calculate UAA loss caused by revising the maximum UAA to 100 hectares (optional).

import os
import numpy as np
import rasterio

def process_geotiff(input_path, output_path):
    with rasterio.open(input_path) as src:
        data = src.read(1)
        processed_data = np.where(data > 1000, data - 1000, 0)
        profile = src.profile
        with rasterio.open(output_path, 'w', **profile) as dst:
            dst.write(processed_data, 1)

def traverse_and_process(input_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    for root, _, files in os.walk(input_directory):
        for file in files:
            if file.endswith('.tif') or file.endswith('.geotiff'):
                input_file = os.path.join(root, file)
                relative_path = os.path.relpath(root, input_directory)
                output_dir = os.path.join(output_directory, relative_path)
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                output_file = os.path.join(output_dir, f"processed_{file}")
                process_geotiff(input_file, output_file)
                print(f"Processed {input_file} -> {output_file}")


input_directory = r'E:\01_Reseach_papers\FA_Pre_irrigation_grid_map\Depository\Step_04\UAA_2010_2020'
output_directory = r'E:\01_Reseach_papers\FA_Pre_irrigation_grid_map\Depository\Step_04\UAA_2010_2020_loss'


traverse_and_process(input_directory, output_directory)


# 4.4 Aggregated some crop types to generate CERE and OTHER categories


import numpy as np
import xlwt
import matplotlib.pyplot as plt
import xlrd
import math
import pandas as pd
import os
import seaborn as sns
import geopandas as gpd
from osgeo import gdal, ogr
import rasterio
from rasterio.mask import mask


os.chdir(r"E:\01_Reseach_papers\FA_Pre_irrigation_grid_map\Depository\Step_04") 

"""
CERE (layer 29) = soft wheat (layer 24) + durum wheat (4) + barley (2) + rye (20) + oats (10) + other cereals (11)
OTHER (layer 30) = ROOF + SOYA + TOBA + OIND + FLOW + OFAR + NURS + OCRO
      = 19 + 21 + 26 + 14 + 5 + 13 + 9 + 12

"""

# cereals excluding rice and maize

for num in range(11):
    year = num+2010
    input_files = [f'Crop_share/{year}/crop_share_{year}_layer_24.tif', 
                   f'Crop_share/{year}/crop_share_{year}_layer_4.tif', 
                   f'Crop_share/{year}/crop_share_{year}_layer_2.tif', 
                   f'Crop_share/{year}/crop_share_{year}_layer_20.tif', 
                   f'Crop_share/{year}/crop_share_{year}_layer_10.tif', 
                   f'Crop_share/{year}/crop_share_{year}_layer_11.tif']
    dataset = gdal.Open(input_files[0])
    proj = dataset.GetProjection()
    geo_transform = dataset.GetGeoTransform()
    cols = dataset.RasterXSize
    rows = dataset.RasterYSize
    output_file = f'Crop_share/{year}/crop_share_{year}_layer_29.tif'
    driver = gdal.GetDriverByName('GTiff')
    output_dataset = driver.Create(output_file, cols, rows, 1, gdal.GDT_Float32)
    output_dataset.SetProjection(proj)
    output_dataset.SetGeoTransform(geo_transform)
    output_array_1 = None
    for input_file in input_files:
        dataset = gdal.Open(input_file)
        band_1 = dataset.GetRasterBand(1)
        array_1 = band_1.ReadAsArray()
        if output_array_1 is None:
            output_array_1 = array_1
        else:
            output_array_1 += array_1
    output_band_1 = output_dataset.GetRasterBand(1)
    output_band_1.WriteArray(output_array_1)
    output_dataset = None
    print(f'Done_year_{year}!')


#--------------------other crops------------

for num in range(11):
    year = num+2010
    input_files = [f'Crop_share/{year}/crop_share_{year}_layer_19.tif', 
                   f'Crop_share/{year}/crop_share_{year}_layer_21.tif', 
                   f'Crop_share/{year}/crop_share_{year}_layer_26.tif', 
                   f'Crop_share/{year}/crop_share_{year}_layer_14.tif', 
                   f'Crop_share/{year}/crop_share_{year}_layer_5.tif', 
                   f'Crop_share/{year}/crop_share_{year}_layer_13.tif', 
                   f'Crop_share/{year}/crop_share_{year}_layer_9.tif', 
                   f'Crop_share/{year}/crop_share_{year}_layer_12.tif']
    dataset = gdal.Open(input_files[0])
    proj = dataset.GetProjection()
    geo_transform = dataset.GetGeoTransform()
    cols = dataset.RasterXSize
    rows = dataset.RasterYSize
    output_file = f'Crop_share/{year}/crop_share_{year}_layer_30.tif'
    driver = gdal.GetDriverByName('GTiff')
    output_dataset = driver.Create(output_file, cols, rows, 1, gdal.GDT_Float32)
    output_dataset.SetProjection(proj)
    output_dataset.SetGeoTransform(geo_transform)
    output_array_1 = None
    for input_file in input_files:
        dataset = gdal.Open(input_file)
        band_1 = dataset.GetRasterBand(1)
        array_1 = band_1.ReadAsArray()
        if output_array_1 is None:
            output_array_1 = array_1
        else:
            output_array_1 += array_1
    output_band_1 = output_dataset.GetRasterBand(1)
    output_band_1.WriteArray(output_array_1)
    output_dataset = None
    print(f'Done_year_{year}!')

"""
4.5   Multiplying UAA generated in Step 03 and crop share in Step 4.4 
to get crop-specific growing area for 16 crop types for year 2010-2020

"""

def raster_calculation(input_path_1, input_path_2, output_path):
    # Open the input datasets
    dataset_a = gdal.Open(input_path_1)
    band1_a = dataset_a.GetRasterBand(1)
    array_a = band1_a.ReadAsArray()
    dataset_b = gdal.Open(input_path_2)
    band1_b = dataset_b.GetRasterBand(1)
    array_b = band1_b.ReadAsArray()
    result_array = array_a * array_b
    geotransform = dataset_a.GetGeoTransform()
    projection = dataset_a.GetProjection()
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    driver = gdal.GetDriverByName('GTiff')
    out_dataset = driver.Create(output_path, dataset_a.RasterXSize, dataset_a.RasterYSize, 1, band1_a.DataType)
    out_dataset.SetGeoTransform(geotransform)
    out_dataset.SetProjection(projection)
    out_band1 = out_dataset.GetRasterBand(1)
    out_band1.WriteArray(result_array)
    out_band1.FlushCache()
    out_dataset = None
    dataset_a = None
    dataset_b = None

for num in range(11):
    year = num+2010
    print(f"start year {year}")
    for crop_id in range(30):
        raster_calculation(f'Crop_share/{year}/crop_share_{year}_layer_{crop_id+1}.tif',
                           f'UAA_2010_2020_revised_100/UAA_{year}.tif',
                           f'Crop_area/{year}/crop_area_{year}_layer_{crop_id+1}.tif')


