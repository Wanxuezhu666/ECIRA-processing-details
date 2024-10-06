
#import os
#os.chdir(r"E:\01_Reseach_papers\FA_Pre_irrigation_grid_map\Depository\01_Processing_detail\step_01") 
"""
这个代码用于生成每个grid的NUTS编号
NUTS编号用数字代替，具体每个数字代表的是什么NUTS2 unit在xlsx文件中可以找到一一对应的关系

"""


import geopandas as gpd
import rasterio
from shapely.geometry import Point
import numpy as np
from tqdm import tqdm



def assign_nuts_to_raster(boundary_shapefile, raster_file, output_raster):
    boundary = gpd.read_file(boundary_shapefile)
    with rasterio.open(raster_file) as src:
        transform = src.transform
        crs = src.crs
        data = src.read(1)
        nodata_value = src.nodata if src.nodata is not None else 0  # 如果 nodata 为 None，使用默认值 0
        nuts_codes = np.full(data.shape, nodata_value, dtype=np.uint16)
        rows, cols = data.shape
        for row in tqdm(range(rows), desc="Processing rows", unit="row"):
            for col in range(cols):
                x, y = transform * (col + 0.5, row + 0.5)  # 计算像素中心的地理坐标
                point = Point(x, y)
                # 检查该点在哪个多边形内
                for _, poly in boundary.iterrows():
                    if poly.geometry.contains(point):
                        nuts_codes[row, col] = poly['ID']
                        break
        # 3. 保存结果为一个新的栅格文件
        out_meta = src.meta.copy()
        out_meta.update({"dtype": "uint16"})
        with rasterio.open(output_raster, 'w', **out_meta) as dst:
            dst.write(nuts_codes, 1)
    print(f"处理完成，结果保存为 '{output_raster}'")

# 示例用法
assign_nuts_to_raster(
    'D:/02_CRC_project/13_Grid_crop_specific_AAI/11_Zonal_calibration/NUS2010_NUTS2_01m_3035.shp',
    'E:/01_Reseach_papers/FA_Pre_irrigation_grid_map/Depository/Input_01_PCTM/UAA_2010_2020/UAA_2010.tif',
    'D:/02_CRC_project/13_Grid_crop_specific_AAI/11_Zonal_calibration/Grid_ID.tif'
)





def assign_nuts_to_raster(boundary_shapefile, raster_file, output_raster):
    boundary = gpd.read_file(boundary_shapefile)  
    with rasterio.open(raster_file) as src:
        transform = src.transform
        crs = src.crs
        data = src.read(1)
        nodata_value = src.nodata if src.nodata is not None else -1  # 如果 nodata 为 None，使用默认值 -1
        nuts_codes = np.full(data.shape, 0, dtype=np.uint16)  # 初始化为0
        rows, cols = data.shape      
        for row in tqdm(range(rows), desc="Processing rows", unit="row"):
            for col in range(cols):
                x, y = transform * (col + 0.5, row + 0.5)  # 计算像素中心的地理坐标
                point = Point(x, y)        
                found_polygon = False 
                # 检查该点在哪个多边形内
                for _, poly in boundary.iterrows():
                    if poly.geometry.contains(point):
                        nuts_codes[row, col] = poly['ID']
                        found_polygon = True
                        break
                if not found_polygon:
                    nuts_codes[row, col] = 0  # 不在任何多边形内的像素设为0
        # 保存结果为一个新的栅格文件
        out_meta = src.meta.copy()
        out_meta.update({"dtype": "uint16", "nodata": 0})
        with rasterio.open(output_raster, 'w', **out_meta) as dst:
            dst.write(nuts_codes, 1)
    

# 示例用法
assign_nuts_to_raster(
    'D:/02_CRC_project/13_Grid_crop_specific_AAI/11_Zonal_calibration/NUS2010_NUTS2_01m_3035.shp',
    'E:/01_Reseach_papers/FA_Pre_irrigation_grid_map/Depository/Input_01_PCTM/UAA_2010_2020/UAA_2010.tif',
    'E:/01_Reseach_papers/FA_Pre_irrigation_grid_map/Depository/Input_01_PCTMGrid_ID.tif'
)


#优化版本-非常快！！！！！！！！！！！！
import numpy as np
import geopandas as gpd
import rasterio
from shapely.geometry import Point
from tqdm import tqdm

def assign_nuts_to_raster(boundary_shapefile, raster_file, output_raster):
    # 读取边界矢量文件
    boundary = gpd.read_file(boundary_shapefile)  
    with rasterio.open(raster_file) as src:
        transform = src.transform
        crs = src.crs
        data = src.read(1)
        nodata_value = src.nodata if src.nodata is not None else -1
        nuts_codes = np.full(data.shape, 0, dtype=np.uint16)  # 初始化为0
        # 创建点网格
        rows, cols = data.shape
        x_coords, y_coords = np.meshgrid(np.arange(cols) + 0.5, np.arange(rows) + 0.5)
        x_coords, y_coords = rasterio.transform.xy(transform, y_coords, x_coords)
        # 转换为 numpy 数组
        x_coords = np.array(x_coords)
        y_coords = np.array(y_coords)
        # 将点列表转换为 GeoDataFrame
        points = gpd.GeoDataFrame(geometry=gpd.points_from_xy(x_coords.flatten(), y_coords.flatten()), crs=crs)
        # 将每个点与多边形进行空间连接，返回点属于的多边形ID
        joined = gpd.sjoin(points, boundary, how='left', op='within')
        # 填充 nuts_codes 数组
        nuts_codes = joined['ID'].fillna(0).values.reshape(data.shape).astype(np.uint16)
        # 保存结果为一个新的栅格文件
        out_meta = src.meta.copy()
        out_meta.update({"dtype": "uint16", "nodata": 0})
        with rasterio.open(output_raster, 'w', **out_meta) as dst:
            dst.write(nuts_codes, 1)

# 示例用法
assign_nuts_to_raster(
    'D:/02_CRC_project/13_Grid_crop_specific_AAI/11_Zonal_calibration/NUS2010_NUTS2_01m_3035.shp',
    'E:/01_Reseach_papers/FA_Pre_irrigation_grid_map/Depository/Input_01_PCTM/UAA_2010_2020/UAA_2010.tif',
    'E:/01_Reseach_papers/FA_Pre_irrigation_grid_map/Depository/Input_01_PCTMGrid_ID.tif'
)









