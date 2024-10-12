import sys
import os
from logger import Logger, log_function_call, get_logger

logger = get_logger("mind_map_gui")

@log_function_call(logger)
def print_system_info():
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Python executable: {sys.executable}")
    logger.info(f"PYTHONPATH: {os.environ.get('PYTHONPATH', 'Not set')}")

print_system_info()

try:
    import tkinter as tk
    logger.info(f"Tkinter version: {tk.TkVersion}")
except ImportError as e:
    logger.error(f"Error importing tkinter: {e}")
    logger.debug(f"sys.path: {sys.path}")
    sys.exit(1)

from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mind_map_creator import MindMapCreator
from mind_map_visualizer import MindMapVisualizer
from data_manager import WikipediaDataManager

class MindMapGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Wikipedia Mind Map Generator")
        self.master.geometry("800x600")

        self.data_manager = WikipediaDataManager()
        self.creator = MindMapCreator(self.data_manager, logger)
        self.visualizer = MindMapVisualizer(logger)

        self.create_widgets()

    @log_function_call(logger)
    def create_widgets(self):
        self.frame = ttk.Frame(self.master, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.topic_label = ttk.Label(self.frame, text="Enter a topic:")
        self.topic_label.grid(row=0, column=0, sticky=tk.W, pady=5)

        self.topic_entry = ttk.Entry(self.frame, width=40)
        self.topic_entry.grid(row=0, column=1, sticky=tk.W, pady=5)

        self.generate_button = ttk.Button(self.frame, text="Generate Mind Map", command=self.generate_mind_map)
        self.generate_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.canvas_frame = ttk.Frame(self.master)
        self.canvas_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

    @log_function_call(logger)
    def generate_mind_map(self):
        topic = self.topic_entry.get()
        if not topic:
            logger.warning("No topic entered")
            return

        logger.info(f"Generating mind map for topic: {topic}")
        graph = self.creator.create_mind_map(topic)

        # Clear previous plot
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        # Create a new figure and plot the mind map
        fig = plt.figure(figsize=(10, 6))
        self.visualizer.visualize_mind_map(graph, topic, fig)

        # Embed the plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        canvas.draw()