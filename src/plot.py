import logging
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d # do not delete this line, even if IDE mistakes it as unused

COLORS = ['#5DEACE', 'purple',  'gold', 'navy', 'pink', 'c', '#CA7272', 'b', '#AE9DC2', 'grey']

def _add_points_to_plot(centroids, scatter_plot):
    color_list_idx = 0
    for cen in centroids.keys():
        scatter_plot.scatter(*zip(*centroids[cen]), color=COLORS[color_list_idx])
        scatter_plot.scatter(*cen, color=COLORS[color_list_idx], marker="*")
        color_list_idx += 1


def _plot_cluster_3d(centroids):
    logging.debug('Started plot_clust_3d')
    ax = plt.axes(projection='3d') # 'ax' name by convention
    _add_points_to_plot(centroids, ax)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')


def show_scatter_plot(dim, centroids):
    logging.debug('Started show_scatter_plot')
    if dim == 2:
        _add_points_to_plot(centroids, plt)
    else:
        _plot_cluster_3d(centroids)
    plt.show()
