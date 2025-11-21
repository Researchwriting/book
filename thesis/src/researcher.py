import requests
import time
from .config import Config
from .rate_limiter import GlobalRateLimiter
from .paper_cache import PaperCache

class Researcher:
    def __init__(self, reference_manager=None):
        self.api_key = Config.SEMANTIC_SCHOLAR_API_KEY
        self.base_url = "https://api.semanticscholar.org/graph/v1/paper/search"
        self.reference_manager = reference_manager
        self.rate_limiter = GlobalRateLimiter()  # Global rate limiter
        self.cache = PaperCache()  # Paper cache


    def search_papers(self, query, limit=5, chapter=""):
        """
        Search for academic papers using Semantic Scholar.
        Uses global rate limiting and caching for efficiency.
        STRICT MODE: Returns empty list if API fails. NO MOCK DATA.
        """
        if not self.api_key:
            print("Warning: No Semantic Scholar API key found. Returning empty list (Strict Mode).")
            return []

        # Check cache first
        cached_results = self.cache.get(query, limit)
        if cached_results is not None:
            # Save cached results to reference manager
            if self.reference_manager and chapter:
                for paper in cached_results:
                    self.reference_manager.add_reference(paper, chapter, ref_type="academic")
            return cached_results

        # Apply global rate limiting (coordinates across all processes)
        self.rate_limiter.wait_for_slot()

        headers = {"x-api-key": self.api_key}
        params = {
            "query": query,
            "limit": limit,
            "fields": "title,authors,year,abstract,venue,doi"
        }

        try:
            response = requests.get(self.base_url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                papers = data.get('data', [])
                
                # Cache the results
                self.cache.set(query, limit, papers)
                
                # Save to reference manager
                if self.reference_manager and chapter:
                    for paper in papers:
                        self.reference_manager.add_reference(paper, chapter, ref_type="academic")
                
                return papers
            else:
                print(f"Error searching papers: {response.status_code} - {response.text}")
                return []
        except Exception as e:
            print(f"Exception during research: {e}")
            return []

    def search_web(self, query, limit=5, chapter=""):
        """
        Search the web using Tavily API.
        """
        api_key = Config.TAVILY_API_KEY
        if not api_key:
            print("Warning: No Tavily API key found. Skipping web search.")
            return []

        url = "https://api.tavily.com/search"
        payload = {
            "api_key": api_key,
            "query": query,
            "search_depth": "advanced",
            "include_answer": False,
            "max_results": limit
        }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                
                # Save to reference manager
                if self.reference_manager and chapter:
                    for result in results:
                        self.reference_manager.add_reference(result, chapter, ref_type="web")
                
                return results
            else:
                print(f"Error searching web: {response.status_code} - {response.text}")
                return []
        except Exception as e:
            print(f"Exception during web search: {e}")
            return []

    def format_references(self, papers, web_results=None):
        """
        Format papers and web results into Harvard style references.
        """
        references = []
        
        # Format Academic Papers
        for paper in papers:
            authors = paper.get('authors', [])
            if authors:
                author_text = ", ".join([a['name'] for a in authors])
            else:
                author_text = "Unknown"
            
            year = paper.get('year', 'n.d.')
            title = paper.get('title', 'Untitled')
            venue = paper.get('venue', '')
            
            ref = f"{author_text} ({year}) '{title}', {venue}."
            references.append(ref)
            
        # Format Web Results
        if web_results:
            for result in web_results:
                title = result.get('title', 'Untitled')
                url = result.get('url', '')
                # Simple Harvard for websites: Title (Year) [Online]. Available at: URL.
                ref = f"'{title}' (n.d.) [Online]. Available at: {url}."
                references.append(ref)
                
        return references
