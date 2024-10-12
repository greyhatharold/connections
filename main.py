from mind_map_creator import MindMapCreator
from mind_map_visualizer import MindMapVisualizer
from data_manager import WikipediaDataManager
from logger import Logger, log_function_call, get_logger

logger = get_logger("mind_map")

@log_function_call(logger)
def main():
    data_manager = WikipediaDataManager()
    
    start_topic = "Artificial Intelligence"
    
    creator = MindMapCreator(data_manager, logger)
    
    try:
        graph = creator.create_mind_map(start_topic)
    except Exception as e:
        logger.error(f"Error creating mind map: {str(e)}")
        return
    
    visualizer = MindMapVisualizer(logger)
    
    try:
        visualizer.visualize_mind_map(graph, start_topic)
    except Exception as e:
        logger.error(f"Error visualizing mind map: {str(e)}")

if __name__ == "__main__":
    main()
