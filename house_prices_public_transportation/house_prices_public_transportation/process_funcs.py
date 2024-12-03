from sklearn.neighbors import KDTree, BallTree
import geopy.distance
import googlemaps
import json 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

class googleMaps():
    def __init__(self,api_key, create_gmaps=True):
        if not create_gmaps:
            self.gmaps = googlemaps.Client(key=api_key)

    def get_geocode(self,list_of_locations:list):
        if list_of_locations is []:
            return "No locations provided"
        
        test_dict = {}
        for i, loc in enumerate(list_of_locations):
            test_dict[loc] = self.gmaps.geocode(loc)
        
        return test_dict


def load_json_file(name):
    """reads the json file and returns the dictionary"""
    with open(name, 'r',) as f:
        busstopCordinates = json.load(f)
    return busstopCordinates


class stikprove(): 
    def __init__(self, list_of_house_coodinates, list_of_busstop_coodinates):
        self.dict = self.calc_stikprove(list_of_house_coodinates, list_of_busstop_coodinates)
        self.df = pd.DataFrame()

    def calc_stikprove(self, list_of_house_coodinates, list_of_busstop_coodinates):
        self_nearest_dict = {}

        for i, house_coodinate in enumerate(list_of_house_coodinates):
            shortest_distance = np.inf
            shortest_distance_coodinate = None
            
            # Loop through all busstops
            for busstop in list_of_busstop_coodinates:
            
                # Calculate the distance between the house and the busstop
                dist = geopy.distance.distance(house_coodinate, tuple(busstop)).km
            
                # Check if the distance is shorter than the shortest distance
                if dist<shortest_distance:
                    shortest_distance = dist
                    shortest_distance_coodinate = busstop

            # Store the nearest busstop to the house
            self_nearest_dict[house_coodinate] = {'coordinate': tuple(shortest_distance_coodinate),
                                                    'Geopy distance': shortest_distance}

        return self_nearest_dict

    def store_in_df(self, nearest_dict):
        df_dist_diff = self.df
        
        # tree column 
        keys = list(nearest_dict[list(nearest_dict.keys())[0]].keys())
        key = [key for key in keys if 'tree distance' in key][0]
        # remove warning 
        import warnings
        warnings.filterwarnings('ignore')
        for coodinate in list(self.dict.keys()):
            
            df_dist_diff = df_dist_diff.append({'coordinate': coodinate,
                                                'Geopy distance': self.dict[coodinate]['Geopy distance'],
                                                key: nearest_dict[coodinate][key],
                                                'Geopy-Geopy': nearest_dict[coodinate]['Geopy distance'] - self.dict[coodinate]['Geopy distance'],
                                                'Tree-Geopy': nearest_dict[coodinate][key] - self.dict[coodinate]['Geopy distance']
                                                }, ignore_index=True)
        # enable warning
        warnings.filterwarnings('default')
        self.df = df_dist_diff


class ball_tree:
    def __init__(self, coordinates) -> None:
        # 
        self.earth_radius = 6371 # in km

        # handle the different types of coordinates
        coordinates = self._handle_coordinates_types(coordinates)
        
        # turn each element into a list of the coordinates
        X = [self._convert_to_radians(list(stop)) for stop in coordinates]
        self.X = X

        # build the tree
        self.tree = BallTree(X, metric='haversine')

    def _handle_coordinate_types(self, coordinate):
        # convert the coordinates to radians
        if isinstance(coordinate,tuple):
            coordinate = np.array(coordinate)
        elif isinstance(coordinate, list):
            coordinate = np.array(coordinate)
        elif isinstance(coordinate, np.array):
            pass
        else: 
            raise ValueError("Coordinates must be a tuple, list or numpy array")
        return coordinate
    def _handle_coordinates_types(self, coordinates):

        if isinstance(coordinates, pd.Series):
            coordinates = coordinates.values
        
        elif isinstance(coordinates, np.array):
            coordinates = coordinates
        
        elif isinstance(coordinates, list):
            coordinates = np.array(coordinates)
        
        else: 
            raise ValueError("Coordinates must be a pandas series, numpy array or list")
        return coordinates
    
    def _convert_to_radians(self, coordinates):
        return np.radians(coordinates)
    
    def _convert_to_km(self, distance):
        return distance * self.earth_radius
    
    def tree_query(self,coordinate, k:int=1):
        """
        Query the tree for the nearest neighbor
            Args: 
                coordinate: tuple, list or numpy array
            Returns:
                index: int
                distance: float
        """
        # handle the different types of coordinates
        coordinate = self._handle_coordinate_types(coordinate)

        # convert the coordinates to radians
        coordinate = self._convert_to_radians(coordinate)

        # query the tree for the nearest neighbor
        nearest_dist, nearest_ind = self.tree.query(
            coordinate.reshape(1,-1), # coordinates for the specific location
            k=k # number of nearest neighbors
            )
        
        # convert the distance to km and return the index and distance
        nearest_dist = self._convert_to_km(nearest_dist[0])
        nearest_ind = nearest_ind[0]

        return nearest_ind[0], nearest_dist[0]
        
    def tree_query_radius(self, coordinate, radius:float):
        """
        Query the tree for all neighbors within a radius
        Args: 
            coordinate: tuple, list or numpy array
            radius: float (in km)
        Returns:
            indexes: list
            distances: list
        """
        # convert the radius to radians
        radian_radius = radius/self.earth_radius

        # handle the different types of coordinates and convert to radians
        coordinate = self._handle_coordinate_types(coordinate) 
        coordinate_radian = self._convert_to_radians(coordinate)
        
        # query the tree for the nearest neighbor within a radius
        indexes, distances = self.tree.query_radius(coordinate_radian.reshape(1,-1), r=radian_radius, return_distance=True)
        self.dist = distances
        # convert the distances to km and return the indexes and distances        
        distances = list(self._convert_to_km(distances[0]))
        indexes = list(indexes[0])

        return indexes, distances

def calc_distance(coordinate1, coordinate2):
    return geopy.distance.distance(coordinate1, coordinate2).km