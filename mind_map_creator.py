import networkx as nx

class MindMapCreator:
    def __init__(self, data_manager, logger):
        self.data_manager = data_manager
        self.logger = logger
        self.graph = nx.Graph()

    def create_mind_map(self, start_topic, depth=2):
        self.logger.info(f"Creating mind map for topic: {start_topic}")
        self.graph.add_node(start_topic)
        topics_to_process = [start_topic]
        
        for current_depth in range(depth):
            self.logger.info(f"Processing depth {current_depth + 1}")
            new_topics = []
            for topic in topics_to_process:
                linked_topics = self.data_manager.get_linked_topics(topic)
                for linked_topic in linked_topics:
                    self.graph.add_edge(topic, linked_topic)
                new_topics.extend(linked_topics)
            topics_to_process = list(set(new_topics))
        
        return self.graph
