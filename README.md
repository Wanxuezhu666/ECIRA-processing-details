# Crop-specific_Irrigated_Area_Map_EU
**Contact**: Wanxue Zhu (wanxue.zhu@agr.uni-goettingen.de) & Stefan Siebert  
Department of Crop Sciences, University of Göttingen, Von-Siebold-Str. 8, 37075 Göttingen, Germany    
**Updated**: 04 October 2024 

The **European Crop-specific IRrigated Area Dataset (ECIRA)** provides data on the actual irrigated area for specific crops across 28 European countries from 2010 to 2020, with a spatial resolution of 1 km and using the EPSG: 3035 projection. 

**16 crop types are included**: cereals (excluding maize and rice), maize, rice, pulses, potatoes, sugar beets, rapeseed and turnip rapeseed, sunflower, textile crops, open-field vegetables, melons, strawberries, grasslands, fruits and berries, citrus, olives, vineyards, and other crops.   

**28 European countries are included**: Austria, Belgium, Bulgaria, Cyprus, the Czech Republic, Germany, Denmark, Estonia, Greece, Spain, Finland, France, Croatia, Hungary, Ireland, Italy, Lithuania, Luxembourg, Latvia, Malta, Netherlands, Poland, Portugal, Romania, Sweden, Slovenia, Slovakia, and the United Kingdom.  

This document outlines the detailed methodology used to generate the ECIRA dataset, which is organized into distinct processing steps.

_Abbreviations:_
-	**AAI** (in hectares): Irrigated area, namely area actually received irrigation.
-	**AEI** (in hectares): Irrigable area, namely area equipped with irrigation infrastructure without considering the actual irrigation is applied or not.

## Step 01: Generating NUTS2-level annual total AAI for 2010-2020
**Method**: Manual

## Step 02: Generating NUTS2-level annual crop-specific AAI for 2010-2020
**Method**: Manual

## Step 03: Generating 1km gridded AEI in 2010

**Method**: QGIS + Python (Step_03_AEI_1km.py)  
**Input**: 
- Step_03/Input_01_AEI_share_2005_001_arc_degree.tif (AEI in year 2005 at 0.01 arc degree resolution)      
- Step_03/Input_02_AEI_share_2010_5_arc_min.tif (AEI in year 2010 at 5 arc min resolution)  
- Step_03/Input_03_Reference_1km.tif (1 km grid as reference)           
**Output**:
- Step_03/ AEI_share_2010_1km_revised_100.tif  

3.1	Transfer GMIA 0.01 arc degree raster data (AEI 2005 at 0.01 arc degree) into points shapefile (Done in QGIS. Results: AEI_share_2005_001_arc_degree_point.shp)  
3.2	Transfer HID 5 arc min raster data (AEI 2010 at 5 arc min) into grid vector shapefile (Done in QGIS. Results: Grid_5_arc_min.shp)  
3.3	Perform Zonal Statistical calculations to compute the mean of all points within the 5 arc minute grids generated in step 2, and create a new grid shapefile. 
(Done in QGIS. Results: Grid_5_arc_min_AEI2005_mean.shp)  
3.4	Resample GMIA (AEI 2005) from 0.01 arc degree to 1 km grid (Done in Python).  
3.5	Convert the shapefile generated in step 3.3 into a TIFF file. This will create the GMIA AEI 2005 5 arc min TIFF file (Done in Python)  
3.6	At the 5-arc minute grid, calculate the correction coefficients between GMIA (AEI 2005) and HID (AEI 2010) to obtain the coefficients at 5 arc min, then resample it to 1km (Done in Python).  
3.7	At 1km grid level, multiply the GMIA obtained in step 3.4 by the coefficients obtained in step 3.6.  
3.8	Revised the maximum final AEI cannot be over 100 hectare.  















