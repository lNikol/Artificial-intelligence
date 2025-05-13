import numpy as np

def initialize_centroids_forgy(data, k):    
    indices = np.random.choice(data.shape[0], size=k, replace=False)
    return data[indices]

def initialize_centroids_kmeans_pp(data, k):
    centroids = np.zeros((k, data.shape[1]))
    # wybieram losowo punkt poczatkowy
    centroids[0] = data[np.random.choice(data.shape[0], 1, replace=False)]

    # Liczenie odleglosci do najblizszego centroidu
    for i in range(1, k):
        distances = np.zeros(data.shape[0])
        for j in range(data.shape[0]):
            distances[j] = np.min(np.sqrt(np.sum((data[j] - centroids[:i]) ** 2)))
        # wybor najdalszego punktu
        centroids[i] = data[distances.argmax()]
    return centroids

def assign_to_cluster(data, centroids):
    # liczenie odleglosci od kazdego punktu do kazdego centroidu
    # np.newaxix - dodaje nowy wymiar, tablica 1D staje sie tablica 2D
    distances = np.sqrt(((data[:, np.newaxis] - centroids)**2).sum(axis=2))
    # zwracanie najbliższego centroidu
    return np.argmin(distances, axis=1)

def update_centroids(data, assignments):
    centroids = []
    for cluster in np.unique(assignments):
        centroids.append(data[assignments == cluster].mean(axis=0))
    return np.array(centroids)

def mean_intra_distance(data, assignments, centroids):
    return np.sqrt(np.sum((data - centroids[assignments, :])**2))

def k_means(data, num_centroids, kmeansplusplus= False):
    # centroids initizalization
    if kmeansplusplus:
        centroids = initialize_centroids_kmeans_pp(data, num_centroids)
    else: 
        centroids = initialize_centroids_forgy(data, num_centroids)

    
    assignments = assign_to_cluster(data, centroids)
    for i in range(100): # max number of iteration = 100
        # print(f"Intra distance after {i} iterations: {mean_intra_distance(data, assignments, centroids)}")
        centroids = update_centroids(data, assignments)
        new_assignments = assign_to_cluster(data, centroids)
        if np.all(new_assignments == assignments): # stop if nothing changed
            break
        else:
            assignments = new_assignments

    return new_assignments, centroids, mean_intra_distance(data, new_assignments, centroids)         

