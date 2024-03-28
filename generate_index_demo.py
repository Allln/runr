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
    edges = ox.graph_to_gdfs(street_graph, nodes=False)
    
    # Filter edges within the given distance from the centroid
    centroid_point = Point(centroid)
    edges = edges[edges.apply(lambda row: centroid_point.distance(row.geometry) <= distance, axis=1)]
    
    # Generate random points along the edges
    points = []
    while len(points) < num_points and not edges.empty:
        index = random.choice(edges.index)
        edge = edges.loc[index, 'geometry']
        # Generate a random distance along the edge
        min_dist = 0.01  # Minimum distance to avoid selecting the start/end points
        max_dist = edge.length - 0.01  # Maximum distance along the edge
        random_dist = random.uniform(min_dist, max_dist)
        point = edge.interpolate(random_dist)
        points.append(point)
        edges = edges.drop(index)
    return points

#nw pg
centroid = (69.6587586, 18.9397725)
#cz pot
#centroid = (50.0121583, 13.3792261)

distance = 1500
num_points = 100
random_points = generate_random_points(centroid, distance, num_points)

map_center = list(reversed(centroid))
mymap = folium.Map(location=map_center, zoom_start=15)

for point in random_points:
    folium.Marker(location=[point.y, point.x]).add_to(mymap)

plugins.LocateControl().add_to(mymap)

html_file_path = "nw.html"
mymap.save(html_file_path)
print("HTML map with random points saved successfully!")
