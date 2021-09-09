import numpy as np
import random
import logging


class MovingCentroids:
    MAX_DISTANCE_BET_POINTS = 2_000_000_000

    def __init__(self, points, k):  # 'k' = convention for number of clusters
        self.points = points
        self.clusters_by_centroid = dict()

        self.set_random_centroids(k)
        logging.debug(f'initial {k} centroids: {self.clusters_by_centroid}')

    def _validate_args(self, k):
        if len(self.points) < k:
            message = f'{self.__class__.__name__} input was only {len(self.points)} points < k={k}; ' \
                           f'Add more points, or use lower k'
            logging.exception(message)
            raise ValueError(message)
        if k < 1:
            raise ValueError(f'k < 1 (input was k={k})')

    def set_random_centroids(self, k):
        """sets k random centroids, chosen from self.points"""
        self._validate_args(k)
        self.clusters_by_centroid = dict()
        while len(self.clusters_by_centroid) < k:
            idx = random.randint(0, len(self.points) - 1)
            point = self.points[idx]
            self.clusters_by_centroid[point] = []

    def iterate_and_update_centroids(self, num_iterations):
        logging.debug(f'starting {num_iterations} iterations')
        for i in range(0, num_iterations):
            updated_centroids = self._get_updated_centroids(self.clusters_by_centroid)
            assigned_centroids = self._assign_points_to_clusters(self.points, updated_centroids)
            if self._clusters_equal(self.clusters_by_centroid, assigned_centroids):
                logging.info(f'discontinued after {i} iterations (new clusters were the same)')
                logging.debug( f'clusters: {self.clusters_by_centroid}')
                break
            self.clusters_by_centroid = assigned_centroids

    @classmethod
    def _get_updated_centroids(cls, clusters_by_centroid):
        updated_centroids = dict()
        for cen in clusters_by_centroid:
            new_cen = cls._get_cluster_average(cen, clusters_by_centroid[cen])
            updated_centroids[new_cen] = []
        logging.debug(f'updated centroids: {updated_centroids}')
        return updated_centroids

    @staticmethod
    def _get_cluster_average(cen, points):
        if len(points) == 0:
            new_cen = cen
        else:
            cluster_average = np.mean(points, axis=0)
            new_cen = tuple(np.round(cluster_average, 2))
        return new_cen

    @classmethod
    def _assign_points_to_clusters(cls, points, centroids):
        for point in points:
            closest_centroid = cls._get_closest_centroid(point, centroids)
            centroids[closest_centroid].append(point)
        return centroids

    @classmethod
    def _get_closest_centroid(cls, point, centroids):
        min_dis = cls.MAX_DISTANCE_BET_POINTS
        centroids_list = list(centroids.keys())
        closest_cen = centroids_list[0]
        for cen in centroids_list:
            distance = cls._get_distance(point, cen)
            if distance < min_dis:
                min_dis = distance
                closest_cen = cen
        return closest_cen

    @staticmethod
    def _get_distance(p1, p2):
        distance = np.linalg.norm(np.array(p1) - np.array(p2))
        if distance > MovingCentroids.MAX_DISTANCE_BET_POINTS:
            raise ValueError(
                f'MAX_DISTANCE_BET_POINTS is {MovingCentroids.MAX_DISTANCE_BET_POINTS}. points are: {p1} and {p2}')
        return distance

    @classmethod
    def _clusters_equal(cls, centroids, updated_centroids):
        if len(centroids) != len(updated_centroids):
            return False
        for key in centroids:
            if key not in updated_centroids:
                return False
            same_list = cls._lists_of_points_equal(centroids[key], updated_centroids[key])
            if not same_list:
                return False
        return True

    @staticmethod
    def _lists_of_points_equal(list1, list2):
        if len(list1) != len(list2):
            return False
        if set(list1) != set(list2):
            return False
        return True


