from sklearn.neighbors import NearestNeighbors
import numpy as np

def find_nearest_dong(lat, lon, dong_info):
    # dong_info: [{district, dong, latitude, longitude, population}, ...]
    coords = np.array([[d["latitude"], d["longitude"]] for d in dong_info])
    query = np.array([[lat, lon]])

    nbrs = NearestNeighbors(n_neighbors=1).fit(coords)
    _, indices = nbrs.kneighbors(query)
    nearest = dong_info[indices[0][0]]
    return nearest
