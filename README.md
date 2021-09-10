# moving-centroids
Clustering 

## Installation
install requirements in your virtual env 
`py -m pip install -r ../requirements.txt`

## Quick Start:
0. activate venv
1. `cd src`
2. examples: 
    - `main.py` - runs with default args (expecting the sample file `data_points.txt` to be in the directory), outputs 2d plot
    - `main.py -f data_points_3d.txt --dim=3` - runs with sample file `data_points_3d.txt`, outputs 3d plot
    - `main.py -k=5` - outputs 2d plot with 5 clusters
    - `main.py -f my_file.txt -k=4` - outputs 2d plot with 4 clusters, using your file as input. see sample files for necessary format

### limitations:
- max `k` = 10, inclusive (number of clusters)
- plot can only be 2d or 3d
- since initial centroids are chosen at random, result may be different in different runs


