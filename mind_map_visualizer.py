import matplotlib.pyplot as plt
import networkx as nx
from logger import log_function_call
from pip._vendor.rich.logging import RichHandler

class MindMapVisualizer:
    def __init__(self, logger):
        self.logger = logger

    @log_function_call(RichHandler())
    def visualize_mind_map(self, graph, start_topic, fig=None):
        self.logger.info("Visualizing mind map")
        if fig is None:
            fig, ax = plt.subplots(figsize=(12, 8))
        else:
            fig.clear()
            ax = fig.add_subplot(111)
        
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, ax=ax, with_labels=True, node_color='lightblue', 
                node_size=3000, font_size=8, font_weight='bold')
        ax.set_title(f"Mind Map for '{start_topic}'")
        ax.axis('off')
        
        # Instead of tight_layout, adjust the figure size if needed
        fig.set_size_inches(12, 8)
        fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
        
        return fig