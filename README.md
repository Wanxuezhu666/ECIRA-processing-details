# Crop-specific_Irrigated_Area_Map_EU
**Contact**: Wanxue Zhu (wanxue.zhu@agr.uni-goettingen.de) & Stefan Siebert  
_Department of Crop Sciences, University of Göttingen, Von-Siebold-Str. 8, 37075 Göttingen, Germany_    
**Updated**: 04 October 2024 

The **European Crop-specific IRrigated Area Dataset (ECIRA)** provides data on the actual irrigated area for specific crops across 28 European countries from 2010 to 2020, with a spatial resolution of 1 km and using the EPSG: 3035 projection. 

**16 crop types are included**: cereals (excluding maize and rice), maize, rice, pulses, potatoes, sugar beets, rapeseed and turnip rapeseed, sunflower, textile crops, open-field vegetables, melons, strawberries, grasslands, fruits and berries, citrus, olives, vineyards, and other crops.   

**28 European countries are included**: Austria, Belgium, Bulgaria, Cyprus, the Czech Republic, Germany, Denmark, Estonia, Greece, Spain, Finland, France, Croatia, Hungary, Ireland, Italy, Lithuania, Luxembourg, Latvia, Malta, Netherlands, Poland, Portugal, Romania, Sweden, Slovenia, Slovakia, and the United Kingdom.  

This document outlines the detailed methodology used to generate the ECIRA dataset, which is organized into distinct processing steps.

_Abbreviations:_
-	**AAI** (in hectares): Irrigated area, namely area actually received irrigation.
-	**AEI** (in hectares): Irrigable area, namely area equipped with irrigation infrastructure without considering the actual irrigation is applied or not.

## Step 01: Generating NUTS2-level annual total AAI for 2010-2020
**Method**: Manual (see the manuscript)

## Step 02: Generating NUTS2-level annual crop-specific AAI for 2010-2020
**Method**: Manual (see the manuscript)

## Step 03: Generating 1km gridded AEI in 2010
**Method**: QGIS + Python (Step_03_AEI_1km.py)  
-	3.1 Transfer GMIA 0.01 arc degree raster data (AEI 2005 at 0.01 arc degree) into points shapefile (Done in QGIS)
-	3.2 Transfer HID 5 arc min raster data (AEI 2010 at 5 arc min) into grid vector shapefile (Done in QGIS)  
- 3.3	Perform Zonal Statistical calculations to compute the mean of all points within the 5 arc minute grids generated in step 2, and create a new grid shapefile. (Done in QGIS)
- 3.4 Resample GMIA (AEI 2005) from 0.01 arc degree to 1 km grid (Done in Python: **xxx.py**).
- 3.5 Convert the shapefile generated in step 3.3 into a TIFF file. This will create the GMIA AEI 2005 5 arc min TIFF file (Done in Python:**xxx.py**)
- 3.6 At the 5-arc minute grid, calculate the correction coefficients between GMIA (AEI 2005) and HID (AEI 2010) to obtain the coefficients at 5 arc min, then resample it to 1km (Done in Python:**xxx.py**).
- 3.7 At 1km grid level, multiply the GMIA obtained in step 3.4 by the coefficients obtained in step 3.6.
- 3.8 Revised the maximum final AEI cannot be over 100 hectare.  

## Step 04: Generating annual 1km gridded crop-specific growing area for 2010–2020
4.1	Split the multi-layer raster data from PCTM into individual single-layer rasters. Layer 0 is UAA, layers 1–28 are expected crop growing share. (Done in Python: **xxx.py**).
4.2	Revise UAA maximum (provided by the ‘weight’ column in DGPCM dataset) as 100 hectares in each 1km pixel. (Done in Python)
4.3	Calculate UAA loss caused by revising the maximum UAA to 100 hectares (optional, Done in Python).
4.4	Aggregated the growing share of some crops as follows, 
| ID |     Eurostat 2010 category     | ECIRA | DGPCM|
| -- | ------------------------------ | ------|----- |
| 1  | Cereals excluding maize & rice |  CERE |      |
| 1.1| Soft wheat                     |       | SWHE |
| 1.2| Durum wheat                    |       | DWHE |
| 1.3| Barley                         |       | BARL |
| 1.4| Rye                            |       | RYEM |
| 1.5| Oats                           |       | OATS |
| 1.6| Other cereals                  |       | OCER |
| 2  | Maize (green and grain)        | LMAIZ | LMAIZ|
| 3  | Rice                           | PARI  | PARI |
| 4  | Pulses                         | PULS  | PULS |
| 5  | Potato                         | POTA  | POTA |
| 6  | Sugar beet                     | SUGB  | SUGB |







