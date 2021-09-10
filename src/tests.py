import unittest
from moving_centroids import *

logging.disable(logging.CRITICAL)


class TestMovingCentroidsCreation(unittest.TestCase):
    points = [(1, 2), (100, 890), (-156, 7000)]

    def test_init_without_attribute_k_throws_TypeError(self):
        self.assertRaises(TypeError, MovingCentroids, points=self.points)

    def test_init_without_attribute_points_throws_TypeError(self):
        self.assertRaises(TypeError, MovingCentroids, k=1)

    def test_init_k_lower_than_len_points_throws_Exception(self):
        self.assertRaises(Exception, MovingCentroids, points=self.points, k=len(self.points)+1)

    def test_init_k_lower_than_zero_throws_Exception(self):
        self.assertRaises(Exception, MovingCentroids, points=self.points, k=-1)

    def test_init_number_of_initial_centroids_equal_to_k(self):
        k = max(len(self.points), 3)
        moving_cen = MovingCentroids(points=self.points, k=k)
        self.assertEqual(len(moving_cen.clusters_by_centroid), k)

        moving_cen = MovingCentroids(points=self.points, k=1)
        self.assertEqual(len(moving_cen.clusters_by_centroid), 1)


class TestMovingCentroidsFunctionsCalculation(unittest.TestCase):

    def test__closest_centroid(self):
        point = (1,2)
        centroids = {(1500, 2000): [], (-19, 15): [], (100,148): []}
        expected = (-19, 15)

        result = MovingCentroids._get_closest_centroid(point, centroids)
        self.assertEqual(result, expected)

    def test__cluster_average__case1(self):
        centroids = {(1, 5): [(1, 5), (-3, 10), (11, 12)]}
        cen = (1, 5)
        expected = (3, 9)

        result = MovingCentroids._get_cluster_average(cen, centroids[cen])
        self.assertEqual(result, expected)

    def test___cluster_average__case2(self):
        centroids = {(4, 15, 10): [(4, 15, 10), (100, 30, 80), (70, 80, 140), (20, 60, 100)]}
        cen = (4, 15, 10)
        expected = (194 / 4, 185 / 4, 330 / 4)

        result = MovingCentroids._get_cluster_average(cen, centroids[cen])
        self.assertEqual(result, expected)

    def test__clusters_equal(self):
        cases = [  # [cluster1, cluster2, expected], [...
            [[{(1, 2): [(1, 1)], (0, 15): [(100, 8), (20, 50)]},
             {(1, 2): [(1, 1)], (0, 15): [(20, 50), (100, 8)]}], True],

            [[{(1, 2): [(1, 1)], (0, 10): [(100, 80), (20, 50)]},
            {(0, 10): [(20, 50), (100, 80)], (1, 2): [(1, 1)]}], True],

            [[{}, {}], True],

            [[{(1, 1): []}, {(1, 2): []}], False],

            [[{(1, 2): [(1, 1)], (0, 15): [(100, 8), (20, 50)]},
            {(1, 2): [(1, 1)], (0, 15): [(8, 100), (20, 50)]}], False],

            [[{(1, 2): [(10, 20)], (3, 4): [(30, 40)]},
              {(1, 2): [(30, 40)], (3, 4): [(10, 20)]}], False]
        ]

        for item in cases:
            clusters, expected = item
            result = MovingCentroids._clusters_equal(*clusters)
            self.assertEqual(result, expected,
                             '{}, expected={}'.format(clusters, expected))


class TestMovingCentroidsFunctionsClusterAssignment(unittest.TestCase):
    points1 = [(1, 5), (-3, 10), (11, 12), (1, 2), (100, 65), (-10, 20)]
    points2 = [(4, 15, 10), (100, 30, 80), (70, 80, 140), (20, 60, 100), (-1, 2, 20), (-10, 800, 10)]

    def test__all_points_are_assigned_to_clusters_after_assignment__case2(self):
        moving_cen2 = MovingCentroids(self.points2, 3)
        updated_centroids = MovingCentroids._assign_points_to_clusters(
            moving_cen2.points, {(70, 80, 140): [], (40, 18, 10): []})
        values = [item for sublist in updated_centroids.values() for item in sublist]  # flatten

        for p in moving_cen2.points:
            self.assertIn(p, values)

    def test__clusters_type_does_not_change_when_updating_centroids(self):
        moving_cen2 = MovingCentroids(self.points2, 3)
        expected = type(moving_cen2.clusters_by_centroid)
        updated_centroids = moving_cen2._get_updated_centroids(moving_cen2.clusters_by_centroid)
        self.assertIsInstance(updated_centroids, expected)

    def test__number_of_clusters_does_not_change_when_updating_centroids_case1(self):
        moving_cen1 = MovingCentroids(self.points1, 3)
        expected = len(moving_cen1.clusters_by_centroid)

        updated_centroids = moving_cen1._get_updated_centroids(moving_cen1.clusters_by_centroid)
        self.assertEqual(len(updated_centroids), expected)

    def test__number_of_clusters_does_not_change_when_updating_centroids_case2(self):
        moving_cen2 = MovingCentroids(self.points2, 2)
        expected = len(moving_cen2.clusters_by_centroid)

        updated_centroids = moving_cen2._get_updated_centroids(moving_cen2.clusters_by_centroid)
        self.assertEqual(len(updated_centroids), expected)


class TestMovingCentroidsMainLogic(unittest.TestCase):
    points1 = [(4, 15, 10), (100, 30, 80), (70, 80, 140), (20, 60, 100), (-1, 2, 20), (-10, 800, 10)]
    moving_cen1 = MovingCentroids(points1, 3)

    def test__centroids_attribute_is_updated_after_first_iteration(self):
        prev_centroids = self.moving_cen1.clusters_by_centroid
        self.moving_cen1.iterate_and_update_centroids(1)

        self.assertEqual(MovingCentroids._clusters_equal(self.moving_cen1.clusters_by_centroid, prev_centroids), False,
                         '{} same as \n {}'.format(self.moving_cen1.clusters_by_centroid, prev_centroids))

    def test__iteration_assigns_all_points_to_clusters(self):
        self.moving_cen1.set_random_centroids(3)
        self.moving_cen1.iterate_and_update_centroids(1)
        num_of_points_in_clusters = sum([len(cluster) for cluster in self.moving_cen1.clusters_by_centroid.values()])
        expected = len(self.points1)
        self.assertEqual(num_of_points_in_clusters, expected)


if __name__ == '__main__':
    unittest.main()
