
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


os.chdir(r"E:\01_Reseach_papers\FA_Pre_irrigation_grid_map\Depository") 

# 5.1  Generate 1km gridded crop-specific AEI

def raster_calculation(input_path_1, input_path_2, output_path):
    # Open the input datasets
    dataset_a = gdal.Open(input_path_1)
    band1_a = dataset_a.GetRasterBand(1)
    array_a = band1_a.ReadAsArray()
    dataset_b = gdal.Open(input_path_2)
    band1_b = dataset_b.GetRasterBand(1)
    array_b = band1_b.ReadAsArray()
    result_array = array_a * array_b/100
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
        raster_calculation(f'Step_04/Crop_area/{year}/crop_area_{year}_layer_{crop_id+1}.tif',
                           f'Step_03/AEI_share_2010_1km_revised_100.tif',
                           f'Step_05/{year}/Crop_AEI_1km_grid/crop_AEI_{year}_layer_{crop_id+1}.tif')


# 5.2 Conduct NUTS2 level zonal statistics



import numpy as np
import xlwt
import matplotlib.pyplot as plt
import xlrd
import math
import pandas as pd
import seaborn as sns
import geopandas as gpd
from osgeo import gdal, ogr
import rasterio
from rasterio.mask import mask
from rasterstats import zonal_stats
from shapely.geometry import box

os.chdir(r"E:\01_Reseach_papers\FA_Pre_irrigation_grid_map\Depository\Step_05") 


#---------------使用NUTS2 shapefile对Crop-specific AEI进行分区统计


def add_field_shapfile(shapefile_path,tif_path,output_path,field_name):
    gdf = gpd.read_file(shapefile_path)
    with rasterio.open(tif_path) as src:
        affine = src.transform
        array = src.read(1)  # 读取第一个波段的数据
    stats = zonal_stats(gdf.geometry, array, affine=affine, stats='sum', nodata=-9999)
    gdf[field_name] = [stat['sum'] for stat in stats]
    #gdf.to_file(output_path)
    return(gdf)


def add_field_shapfile_more(gdf,tif_path,field_name):
    with rasterio.open(tif_path) as src:
        affine = src.transform
        array = src.read(1)  # 读取第一个波段的数据
    stats = zonal_stats(gdf.geometry, array, affine=affine, stats='sum', nodata=-9999)
    gdf[field_name] = [stat['sum'] for stat in stats]
    return(gdf)




#这里用了不同的函数叠加
for num in range(11):
    year = num+2010
    print(year)
    Crop = add_field_shapfile('NUS2010_NUTS2_01m_3035.shp',f'Crop_AEI_1km_grid/{year}/crop_AEI_{year}_layer_1.tif','Crop_AEI_NUTS2/Crop_1.shp','APPL_OFRU')
    Crop = add_field_shapfile_more(Crop,f'Crop_AEI_1km_grid/{year}/crop_AEI_{year}_layer_29.tif','CERE')
    Crop = add_field_shapfile_more(Crop,f'Crop_AEI_1km_grid/{year}/crop_AEI_{year}_layer_3.tif','CITR')
    Crop = add_field_shapfile_more(Crop,f'Crop_AEI_1km_grid/{year}/crop_AEI_{year}_layer_6.tif','GRAS')
    Crop = add_field_shapfile_more(Crop,f'Crop_AEI_1km_grid/{year}/crop_AEI_{year}_layer_7.tif','LMAIZ')
    Crop = add_field_shapfile_more(Crop,f'Crop_AEI_1km_grid/{year}/crop_AEI_{year}_layer_8.tif','LRAPE')
    Crop = add_field_shapfile_more(Crop,f'Crop_AEI_1km_grid/{year}/crop_AEI_{year}_layer_15.tif','OlIVGR')
    Crop = add_field_shapfile_more(Crop,f'Crop_AEI_1km_grid/{year}/crop_AEI_{year}_layer_30.tif','OTHER')
    Crop = add_field_shapfile_more(Crop,f'Crop_AEI_1km_grid/{year}/crop_AEI_{year}_layer_16.tif','PARI')
    Crop = add_field_shapfile_more(Crop,f'Crop_AEI_1km_grid/{year}/crop_AEI_{year}_layer_17.tif','POTA')
    Crop = add_field_shapfile_more(Crop,f'Crop_AEI_1km_grid/{year}/crop_AEI_{year}_layer_18.tif','PULS')
    Crop = add_field_shapfile_more(Crop,f'Crop_AEI_1km_grid/{year}/crop_AEI_{year}_layer_22.tif','SUGB')
    Crop = add_field_shapfile_more(Crop,f'Crop_AEI_1km_grid/{year}/crop_AEI_{year}_layer_23.tif','SUNF')
    Crop = add_field_shapfile_more(Crop,f'Crop_AEI_1km_grid/{year}/crop_AEI_{year}_layer_25.tif','TEXT')
    Crop = add_field_shapfile_more(Crop,f'Crop_AEI_1km_grid/{year}/crop_AEI_{year}_layer_27.tif','TOMA_OVEG')
    Crop = add_field_shapfile_more(Crop,f'Crop_AEI_1km_grid/{year}/crop_AEI_{year}_layer_28.tif','VINY')
    output_shapefile_path = f'Crop_AEI_NUTS2/Crop_AEI_NUTS2_{year}.shp'
    Crop.to_file(output_shapefile_path)








