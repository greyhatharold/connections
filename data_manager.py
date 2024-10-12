import requests

class WikipediaDataManager:
    def __init__(self):
        self.api_url = "https://en.wikipedia.org/w/api.php"

    def get_linked_topics(self, topic, limit=5):
        params = {
            "action": "query",
            "format": "json",
            "titles": topic,
            "prop": "links",
            "pllimit": limit
        }
        response = requests.get(self.api_url, params=params)
        data = response.json()
        
        linked_topics = []
        pages = data["query"]["pages"]
        for page_id in pages:
            page = pages[page_id]
            if "links" in page:
                linked_topics.extend([link["title"] for link in page["links"]])
        
        return linked_topics[:limit]
