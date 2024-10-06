

import rasterio
import numpy as np
import glob
import os
os.chdir(r"E:\01_Reseach_papers\FA_Pre_irrigation_grid_map\Depository") 

def sum_geotiffs(input_folder, output_file, max_value):
    """
    Reads all GeoTIFF files from the specified folder, sums their pixel values,
    caps values greater than max_value, and saves the result as a new GeoTIFF file.

    Parameters:
    - input_folder (str): Path to the folder containing GeoTIFF files.
    - output_file (str): Path where the summed GeoTIFF file will be saved.
    - max_value (float): Maximum allowed value for the pixels in the output GeoTIFF.
    """
    geotiff_files = glob.glob(os.path.join(input_folder, '*.tif'))
    if not geotiff_files:
        raise ValueError("No GeoTIFF files found in the specified directory.")
    with rasterio.open(geotiff_files[0]) as src:
        profile = src.profile
        sum_array = np.zeros((src.height, src.width), dtype=np.float32)
    for file in geotiff_files:
        with rasterio.open(file) as src:
            data = src.read(1)  
            sum_array += data
    sum_array[sum_array > max_value] = max_value
    profile.update(dtype=rasterio.float32, count=1)
    with rasterio.open(output_file, 'w', **profile) as dst:
        dst.write(sum_array, 1)
    print(f"Summed GeoTIFF saved as: {output_file}")


for i in range(11):
    year = 2010 + i
    input_folder = f'ECIRA/{year}'
    output_file = f'ECIRA/Total_AAI/Total_AAI_1km_{year}.tif'
    sum_geotiffs(input_folder, output_file,100)

