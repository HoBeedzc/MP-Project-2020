from .NetworkBuilder import *
from .Visualization import *
import sys

print('''GraphStat 1.0.0
Author:HoBee
Find me at: https://github.com/HoBeedzc''')

if sys.version_info[0] < 3:
    print(
        "Sorry, GraphStat does not support Python2, please update your Python to 3.0 version.",
        file=sys.stderr)
    sys.exit(1)

__all__ = [
    'init_edge', 'init_graph', 'save_graph', 'load_graph', 'init_node',
    'get_id', 'get_name', 'get_power', 'get_type', 'get_other_info',
    'print_node', 'cal_average_dgree', 'get_attr_distribution',
    'cal_degree_distribution', 'plot_dgree_distribution', 'plot_nodes_attr'
]
__version__ = '1.0.0'
__license__ = 'MIT'
