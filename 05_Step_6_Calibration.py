import pandas as pd
import os
import geopandas as gpd
import numpy as np
from osgeo import gdal, gdalconst

os.chdir(r"E:\01_Reseach_papers\FA_Pre_irrigation_grid_map\Depository") 

# 6.1 NUTS2 level, calculate crop-specific AAI calibration coefficients

for num in range(11):
    year = num + 2010
    print(year)
    AAI = pd.read_excel(f"Step_02/05_crop_AAI_NUTS2_{year}.xlsx")
    NUTS_ID = pd.read_excel("Step_06/NUTS_number_list_new.xlsx",sheet_name = "Sheet1")
    AAI_NUTS_ID = pd.merge(NUTS_ID, AAI, on='NUTS2', how='inner')
    AAI_NUTS_ID.insert(0, 'FID', AAI_NUTS_ID['NUTS2'])
    gdf = gpd.read_file(f'Step_05/Crop_AEI_NUTS2/Crop_AEI_NUTS2_{year}.shp')
    merged_gdf = gdf.merge(AAI_NUTS_ID, on='FID')
    merged_gdf['GRAS_Cali'] = 10000 * merged_gdf['Grass']/merged_gdf['GRAS']
    merged_gdf['CERE_Cali'] = 10000.0 * merged_gdf['Cereal_excl']/merged_gdf['CERE']
    merged_gdf['LMAIZ_Cali'] = 10000.0 * merged_gdf['Maize']/merged_gdf['LMAIZ']
    merged_gdf['PARI_Cali'] = 10000.0 * merged_gdf['Rice']/merged_gdf['PARI']
    merged_gdf['PULS_Cali'] = 10000.0 * merged_gdf['Pulses']/merged_gdf['PULS']
    merged_gdf['POTA_Cali'] = 10000.0 * merged_gdf['Potato']/merged_gdf['POTA']
    merged_gdf['SUGB_Cali'] = 10000.0 * merged_gdf['Sugarbeet']/merged_gdf['SUGB']
    merged_gdf['LRAPE_Cali'] = 10000.0 * merged_gdf['Turnip_rape']/merged_gdf['LRAPE']
    merged_gdf['SUNF_Cali'] = 10000.0 * merged_gdf['Sunflower']/merged_gdf['SUNF']
    merged_gdf['TEXT_Cali'] = 10000.0 * merged_gdf['Textile']/merged_gdf['TEXT']
    merged_gdf['TOMA_OVEG_Cali'] = 10000.0 * merged_gdf['Vege_melon_strawberry']/merged_gdf['TOMA_OVEG']
    merged_gdf['OTHER_Cali'] = 10000.0 * merged_gdf['Other_crop']/merged_gdf['OTHER']
    merged_gdf['APPL_OFRU_Cali'] = 10000.0 * merged_gdf['Fruit_berry']/merged_gdf['APPL_OFRU']
    merged_gdf['CITR_Cali'] = 10000.0 * merged_gdf['Citrus']/merged_gdf['CITR']
    merged_gdf['OLIVGR_Cali'] = 10000.0 * merged_gdf['Olive']/merged_gdf['OlIVGR']
    merged_gdf['VINY_Cali'] = 10000.0 * merged_gdf['Vineyard']/merged_gdf['VINY']
    selected_columns = ['FID','ID_x',
                        'GRAS_Cali', 'CERE_Cali', 'LMAIZ_Cali','PARI_Cali','PULS_Cali',
                        'POTA_Cali','SUGB_Cali','LRAPE_Cali','SUNF_Cali','TEXT_Cali',
                        'TOMA_OVEG_Cali','OTHER_Cali','APPL_OFRU_Cali','CITR_Cali',
                        'OLIVGR_Cali','VINY_Cali']
    selected_data = merged_gdf[selected_columns]
    selected_data = selected_data.rename(columns={'ID_x': 'ID'})
    selected_data.replace('inf', np.nan, inplace=True)#check Nan and inf data, replaced by 0
    selected_data.replace([np.inf, -np.inf], np.nan, inplace=True)
    selected_data.fillna(0, inplace=True)
    selected_data.to_excel(f'Step_06/Coefficients_NUTS2/Coefficients_{year}.xlsx', index=False)



# 6.2 Generate 1 km crop-specific AAI calibration coefficients TIF

from osgeo import gdal, gdalconst

def create_new_geotiff(input_path, output_path, pixel_values_dict):
    input_dataset = gdal.Open(input_path, gdalconst.GA_ReadOnly)
    geotransform = input_dataset.GetGeoTransform()
    projection = input_dataset.GetProjection()
    num_cols = input_dataset.RasterXSize
    num_rows = input_dataset.RasterYSize
    input_data = input_dataset.ReadAsArray()
    new_data = np.zeros((num_rows, num_cols), dtype=np.float32)
  # Assign values to the new pixel data array based on the pixel value dictionary
    for row in range(num_rows):
        for col in range(num_cols):
            pixel_value = input_data[row][col]
            if not np.isnan(pixel_value):  # Check whether it is NaN
                if pixel_value in pixel_values_dict:
                    new_data[row][col] = pixel_values_dict[pixel_value]
            else:
                new_data[row][col] = nan_value_replacement
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    driver = gdal.GetDriverByName("GTiff")
    output_dataset = driver.Create(output_path,
                                    num_cols,
                                    num_rows,
                                    1,  
                                    gdal.GDT_Float32)
    output_dataset.SetGeoTransform(geotransform)
    output_dataset.SetProjection(projection)
    output_band = output_dataset.GetRasterBand(1)
    output_band.WriteArray(new_data)
    input_dataset = None
    output_dataset = None


for num in range(11):
    year = num + 2010
    df = pd.read_excel(f'Step_06/Coefficients_NUTS2/Coefficients_{year}.xlsx')
    print(year)
    pixel_values_dict = dict(zip(df['ID'], df['GRAS_Cali']))
    input_tif_path = "Step_06/Grid_number_ID.tif"
    output_tif_path = f"Step_06/Coefficients_1km/{year}/GRAS_efficients_{year}.tif"
    create_new_geotiff(input_tif_path, output_tif_path, pixel_values_dict)
    pixel_values_dict = dict(zip(df['ID'], df['CERE_Cali']))
    output_tif_path = f"Step_06/Coefficients_1km/{year}/CERE_efficients_{year}.tif"
    create_new_geotiff(input_tif_path, output_tif_path, pixel_values_dict)
    pixel_values_dict = dict(zip(df['ID'], df['LMAIZ_Cali']))
    output_tif_path = f"Step_06/Coefficients_1km/{year}/LMAIZ_efficients_{year}.tif"
    create_new_geotiff(input_tif_path, output_tif_path, pixel_values_dict)
    pixel_values_dict = dict(zip(df['ID'], df['PARI_Cali']))
    output_tif_path = f"Step_06/Coefficients_1km/{year}/PARI_efficients_{year}.tif"
    create_new_geotiff(input_tif_path, output_tif_path, pixel_values_dict)
    pixel_values_dict = dict(zip(df['ID'], df['PULS_Cali']))
    output_tif_path = f"Step_06/Coefficients_1km/{year}/PULS_efficients_{year}.tif"
    create_new_geotiff(input_tif_path, output_tif_path, pixel_values_dict)
    pixel_values_dict = dict(zip(df['ID'], df['POTA_Cali']))
    output_tif_path = f"Step_06/Coefficients_1km/{year}/POTA_efficients_{year}.tif"
    create_new_geotiff(input_tif_path, output_tif_path, pixel_values_dict)
    #----------------
    pixel_values_dict = dict(zip(df['ID'], df['SUGB_Cali']))
    output_tif_path = f"Step_06/Coefficients_1km/{year}/SUGB_efficients_{year}.tif"
    create_new_geotiff(input_tif_path, output_tif_path, pixel_values_dict)
    pixel_values_dict = dict(zip(df['ID'], df['LRAPE_Cali']))
    output_tif_path = f"Step_06/Coefficients_1km/{year}/LRAPE_efficients_{year}.tif"
    create_new_geotiff(input_tif_path, output_tif_path, pixel_values_dict)
    pixel_values_dict = dict(zip(df['ID'], df['SUNF_Cali']))
    output_tif_path = f"Step_06/Coefficients_1km/{year}/SUNF_efficients_{year}.tif"
    create_new_geotiff(input_tif_path, output_tif_path, pixel_values_dict)
    pixel_values_dict = dict(zip(df['ID'], df['TEXT_Cali']))
    output_tif_path = f"Step_06/Coefficients_1km/{year}/TEXT_efficients_{year}.tif"
    create_new_geotiff(input_tif_path, output_tif_path, pixel_values_dict)
    pixel_values_dict = dict(zip(df['ID'], df['TOMA_OVEG_Cali']))
    output_tif_path = f"Step_06/Coefficients_1km/{year}/TOMA_OVEG_efficients_{year}.tif"
    create_new_geotiff(input_tif_path, output_tif_path, pixel_values_dict)
    #-------------
    pixel_values_dict = dict(zip(df['ID'], df['OTHER_Cali']))
    output_tif_path = f"Step_06/Coefficients_1km/{year}/OTHER_efficients_{year}.tif"
    create_new_geotiff(input_tif_path, output_tif_path, pixel_values_dict)
    pixel_values_dict = dict(zip(df['ID'], df['APPL_OFRU_Cali']))
    output_tif_path = f"Step_06/Coefficients_1km/{year}/APPL_OFRU_efficients_{year}.tif"
    create_new_geotiff(input_tif_path, output_tif_path, pixel_values_dict)
    pixel_values_dict = dict(zip(df['ID'], df['CITR_Cali']))
    output_tif_path = f"Step_06/Coefficients_1km/{year}/CITR_efficients_{year}.tif"
    create_new_geotiff(input_tif_path, output_tif_path, pixel_values_dict)
    pixel_values_dict = dict(zip(df['ID'], df['OLIVGR_Cali']))
    output_tif_path = f"Step_06/Coefficients_1km/{year}/OLIVGR_efficients_{year}.tif"
    create_new_geotiff(input_tif_path, output_tif_path, pixel_values_dict)
    pixel_values_dict = dict(zip(df['ID'], df['VINY_Cali']))
    output_tif_path = f"Step_06/Coefficients_1km/{year}/VINY_efficients_{year}.tif"
    create_new_geotiff(input_tif_path, output_tif_path, pixel_values_dict)



# 6.3 Multiplying AAI calibration coefficients (generated in step 6.2) with crop-AEI (generated in step 5.2).

def multiply_two_images(input_path1, input_path2, output_path):
    input_dataset1 = gdal.Open(input_path1, gdalconst.GA_ReadOnly)
    input_dataset2 = gdal.Open(input_path2, gdalconst.GA_ReadOnly)
    num_cols = input_dataset1.RasterXSize
    num_rows = input_dataset1.RasterYSize
    data_type = gdal.GDT_Float32
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    driver = gdal.GetDriverByName("GTiff")
    output_dataset = driver.Create(output_path, num_cols, num_rows, 1, data_type)
    output_dataset.SetGeoTransform(input_dataset1.GetGeoTransform())
    output_dataset.SetProjection(input_dataset1.GetProjection())
    data1 = input_dataset1.GetRasterBand(1).ReadAsArray().astype(np.float32)
    data2 = input_dataset2.ReadAsArray().astype(np.float32)
    result_data = data1 * data2 / 10000.0
    result_data[result_data > 100] = 100
    output_band = output_dataset.GetRasterBand(1)
    output_band.WriteArray(result_data)
    input_dataset1 = None
    input_dataset2 = None
    output_dataset = None

for num in range(11):
    year = num + 2010
    print(year)
    multiply_two_images(f"Step_05/Crop_AEI_1km_grid/{year}/crop_AEI_{year}_layer_29.tif", f"Step_06/Coefficients_1km/{year}/CERE_efficients_{year}.tif", f"ECIRA/{year}/CERE_AAI_{year}.tif")
    multiply_two_images(f"Step_05/Crop_AEI_1km_grid/{year}/crop_AEI_{year}_layer_7.tif", f"Step_06/Coefficients_1km/{year}/LMAIZ_efficients_{year}.tif", f"ECIRA/{year}/LMAIZ_AAI_{year}.tif")
    multiply_two_images(f"Step_05/Crop_AEI_1km_grid/{year}/crop_AEI_{year}_layer_16.tif", f"Step_06/Coefficients_1km/{year}/PARI_efficients_{year}.tif", f"ECIRA/{year}/PARI_AAI_{year}.tif")
    multiply_two_images(f"Step_05/Crop_AEI_1km_grid/{year}/crop_AEI_{year}_layer_18.tif", f"Step_06/Coefficients_1km/{year}/PULS_efficients_{year}.tif", f"ECIRA/{year}/PULS_AAI_{year}.tif")
    multiply_two_images(f"Step_05/Crop_AEI_1km_grid/{year}/crop_AEI_{year}_layer_17.tif", f"Step_06/Coefficients_1km/{year}/POTA_efficients_{year}.tif", f"ECIRA/{year}/POTA_AAI_{year}.tif")
    multiply_two_images(f"Step_05/Crop_AEI_1km_grid/{year}/crop_AEI_{year}_layer_22.tif", f"Step_06/Coefficients_1km/{year}/SUGB_efficients_{year}.tif", f"ECIRA/{year}/SUGB_AAI_{year}.tif")
    multiply_two_images(f"Step_05/Crop_AEI_1km_grid/{year}/crop_AEI_{year}_layer_8.tif", f"Step_06/Coefficients_1km/{year}/LRAPE_efficients_{year}.tif", f"ECIRA/{year}/LRAPE_AAI_{year}.tif")
    multiply_two_images(f"Step_05/Crop_AEI_1km_grid/{year}/crop_AEI_{year}_layer_23.tif", f"Step_06/Coefficients_1km/{year}/SUNF_efficients_{year}.tif", f"ECIRA/{year}/SUNF_AAI_{year}.tif")
    multiply_two_images(f"Step_05/Crop_AEI_1km_grid/{year}/crop_AEI_{year}_layer_25.tif", f"Step_06/Coefficients_1km/{year}/TEXT_efficients_{year}.tif", f"ECIRA/{year}/TEXT_AAI_{year}.tif")
    multiply_two_images(f"Step_05/Crop_AEI_1km_grid/{year}/crop_AEI_{year}_layer_27.tif", f"Step_06/Coefficients_1km/{year}/TOMA_OVEG_efficients_{year}.tif", f"ECIRA/{year}/TOMA_OVEG_AAI_{year}.tif")
    multiply_two_images(f"Step_05/Crop_AEI_1km_grid/{year}/crop_AEI_{year}_layer_6.tif", f"Step_06/Coefficients_1km/{year}/GRAS_efficients_{year}.tif", f"ECIRA/{year}/GRAS_AAI_{year}.tif")
    multiply_two_images(f"Step_05/Crop_AEI_1km_grid/{year}/crop_AEI_{year}_layer_30.tif", f"Step_06/Coefficients_1km/{year}/OTHER_efficients_{year}.tif", f"ECIRA/{year}/OTHER_AAI_{year}.tif")
    multiply_two_images(f"Step_05/Crop_AEI_1km_grid/{year}/crop_AEI_{year}_layer_1.tif", f"Step_06/Coefficients_1km/{year}/APPL_OFRU_efficients_{year}.tif", f"ECIRA/{year}/APPL_OFRU_AAI_{year}.tif")
    multiply_two_images(f"Step_05/Crop_AEI_1km_grid/{year}/crop_AEI_{year}_layer_3.tif", f"Step_06/Coefficients_1km/{year}/CITR_efficients_{year}.tif", f"ECIRA/{year}/CITR_AAI_{year}.tif")
    multiply_two_images(f"Step_05/Crop_AEI_1km_grid/{year}/crop_AEI_{year}_layer_15.tif", f"Step_06/Coefficients_1km/{year}/OLIVGR_efficients_{year}.tif", f"ECIRA/{year}/OLIVGR_AAI_{year}.tif")
    multiply_two_images(f"Step_05/Crop_AEI_1km_grid/{year}/crop_AEI_{year}_layer_28.tif", f"Step_06/Coefficients_1km/{year}/VINY_efficients_{year}.tif", f"ECIRA/{year}/VINY_AAI_{year}.tif")





