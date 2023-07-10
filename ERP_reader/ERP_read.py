import numpy as np
import cv2
import os

cwd = os.getcwd()

light_maps_folder = cwd + '/light_maps/'
bluelightmap = light_maps_folder + 'bluelightmap2.tif'

# Read the light map
light_map = cv2.imread('bluelightmap2.tif', cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
print(light_map)

#print the first 5 pixels that are non-zero
print("nonzero terms:", light_map[np.nonzero(light_map)][0:5])        

#actual sphere radius 
radius = 1

# calculate the average light strength and pixel area
avg_light_strength = np.mean(light_map)
print("avglight strenght",avg_light_strength)
pixel_area = 4 * np.pi * (radius **2) / (light_map.shape[0] * light_map.shape[1])
print("pixel area",pixel_area)
#incident power for each pixel and sum for total incident power
total_incident_power = np.sum(light_map) * pixel_area
print("total incident power",total_incident_power)
# radiation pressure
c = 3 * 10 ** 8
radiation_pressure = total_incident_power / (c * 4* np.pi * (radius ** 2))
print("radiation pressure",radiation_pressure)
