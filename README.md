# Mind Map Generator

This incomplete project is a Mind Map Generator that uses Wikipedia data to create and visualize mind maps. I hope there is some wisdom I will find in here later to justify the time it took to get this repo to function correctly.

## Files Overview

### `mind_map_creator.py`

- **Purpose**: This module is responsible for creating a mind map graph based on a starting topic and a specified depth.
- **Key Components**:
  - `MindMapCreator` class: Initializes with a data manager and logger, and uses NetworkX to create a graph.
  - `create_mind_map` method: Generates a mind map by adding nodes and edges based on linked topics retrieved from the data manager.

### `mind_map_visualizer.py`

- **Purpose**: This module handles the visualization of the mind map using Matplotlib.
- **Key Components**:
  - `MindMapVisualizer` class: Initializes with a logger.
  - `visualize_mind_map` method: Draws the mind map graph with labels and custom styling, and embeds it in a Matplotlib figure.

### `gui.py`

- **Purpose**: This module provides a graphical user interface (GUI) for the mind map generator using Tkinter.
- **Key Components**:
  - `MindMapGUI` class: Sets up the main window, initializes components, and handles user interactions.
  - `create_widgets` method: Creates and arranges the GUI widgets.
  - `generate_mind_map` method: Handles the generation and visualization of the mind map based on user input.

### `util.py`

- **Purpose**: Contains utility functions and classes used across the project.
- **Key Components**:
  - Various utility functions for string manipulation and caching.
  - Classes for managing configuration flags and memoization.

### `data_manager.py`

- **Purpose**: This module interacts with the Wikipedia API to fetch linked topics for a given topic.
- **Key Components**:
  - `WikipediaDataManager` class: Manages API requests to Wikipedia.
  - `get_linked_topics` method: Retrieves a list of linked topics from Wikipedia for a given topic.

## Dependencies

- `networkx`: For creating and managing the mind map graph.
- `matplotlib`: For visualizing the mind map.
- `tkinter`: For the graphical user interface.
- `requests`: For making HTTP requests to the Wikipedia API.

## Getting Started

To run the application, ensure you have the necessary Python packages installed. You can install them using:

```bash
pip install -r requirements.txt
```

Then, execute the GUI application:

```bash
python main.py
```

This will start the GUI application, allowing you to input a starting topic and depth, and visualize the resulting mind map.    
