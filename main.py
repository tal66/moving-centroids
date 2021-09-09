import argparse
import logging
import plot, file_parser, moving_centroids  # project files
import os

DEFAULT_FILE = os.path.abspath('data_points.txt')
DEFAULT_K = 3
DEFAULT_PLOT_DIM = 2
DEFAULT_NUM_ITERATIONS = 20

logger = logging.getLogger()
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s %(levelname)s %(name)s %(funcName)s()]: %(message)s'
)

parser = argparse.ArgumentParser()
parser.add_argument('-f','--file', default=DEFAULT_FILE)
parser.add_argument('-d', '--dim', type=int, default=DEFAULT_PLOT_DIM, help='dimension for plot. 2 or 3')
parser.add_argument('-i', '--iter', type=int, default=DEFAULT_NUM_ITERATIONS, help='number of iterations')
parser.add_argument('-k', type=int, default=DEFAULT_K, help="number of clusters")  # 'k' is used by convention
args = parser.parse_args()

logging.info(f'args:file = {args.file}')
logging.info(f'args:dim = {args.dim}')
logging.info(f'args:num iterations = {args.iter}')
logging.info(f'args:k = {args.k}')


if __name__ == "__main__":
    data_points = file_parser.parse_file(args.file)
    clusters = moving_centroids.MovingCentroids(points=data_points, k=args.k)
    clusters.iterate_and_update_centroids(args.iter)
    plot.show_scatter_plot(args.dim, clusters.clusters_by_centroid)
