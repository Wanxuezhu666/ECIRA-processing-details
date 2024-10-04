# Crop-specific_Irrigated_Area_Map_EU
**Contact**: Wanxue Zhu (wanxue.zhu@agr.uni-goettingen.de) & Stefan Siebert  
Department of Crop Sciences, University of Göttingen, Von-Siebold-Str. 8, 37075 Göttingen, Germany    
**Updated**: 04 October 2024 

The **European Crop-specific IRrigated Area Dataset (ECIRA)** provides data on the actual irrigated area for specific crops across 28 European countries from 2010 to 2020, with a spatial resolution of 1 km and using the EPSG: 3035 projection. 

**16 crop types are included**: cereals (excluding maize and rice), maize, rice, pulses, potatoes, sugar beets, rapeseed and turnip rapeseed, sunflower, textile crops, open-field vegetables, melons, strawberries, grasslands, fruits and berries, citrus, olives, vineyards, and other crops.   

**28 European countries are included**: Austria, Belgium, Bulgaria, Cyprus, the Czech Republic, Germany, Denmark, Estonia, Greece, Spain, Finland, France, Croatia, Hungary, Ireland, Italy, Lithuania, Luxembourg, Latvia, Malta, Netherlands, Poland, Portugal, Romania, Sweden, Slovenia, Slovakia, and the United Kingdom.  

This document outlines the detailed methodology used to generate the ECIRA dataset, which is organized into distinct processing steps.

**Key input datasets for generating ECIRA** 
-	Annual crop-specific growing shares and total utilized agricultural areas at a 1-km scale for 2010–2020. https://doi.org/10.1016/10.1016/j.ecoinf.2024.102836
-	Annual subnational total irrigated area data from the European Long-term Irrigation Area Dataset (ELIAD Dataset 6 – the best guess of total AAI, primarily at the NUTS2 level) for 2010–2020. https://doi.org/10.1038/s43247-024-01721-z
-	The 0.01 arc degree gridded total irrigable area for 2005 from the Global Map of Irrigation Area version 5.0 (GMIA v5.0), and the 5-arc minute gridded total irrigable area for 2010 from the Historical Irrigation Dataset (HID). https://doi.org/10.13140/2.1.2660.6728  https://doi.org/10.1038/s44221-024-00206-9
-	Eurostat-reported crop-specific irrigated area data from 2010 at the NUTS2 level. https://doi.org/10.2908/EF_MP_IRRI


## Step 01: 
