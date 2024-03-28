import osmnx as ox
import random
from shapely.geometry import Point
import geopandas as gpd
import pandas as pd
import folium
import gpxpy
import gpxpy.gpx
from folium import plugins

def generate_random_points(centroid, distance, num_points):
    street_graph = ox.graph_from_point(centroid, dist=distance, network_type='all')
    nodes, _ = ox.graph_to_gdfs(street_graph)
    centroid_point = Point(centroid)
    nodes = nodes[nodes.distance(centroid_point).abs() <= distance]
    points = []
    while len(points) < num_points and not nodes.empty:
        index = random.choice(nodes.index)
        point = nodes.loc[index, 'geometry']
        points.append(point)
        nodes = nodes.drop(index)
    return points

centroid = (69.6587586, 18.9397725)
distance = 1000
num_points = 5
random_points = generate_random_points(centroid, distance, num_points)

map_center = list(reversed(centroid))
mymap = folium.Map(location=map_center, zoom_start=15)

for point in random_points:
    folium.Marker(location=[point.y, point.x]).add_to(mymap)

plugins.LocateControl().add_to(mymap)

html_file_path = "index.html"
mymap.save(html_file_path)
print("HTML map with random points saved successfully!")
