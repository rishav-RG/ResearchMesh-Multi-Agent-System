from langchain.tools import tool
import requests 
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY")) # Initialize Tavily client with API key

# tool for web search 
@tool
def web_search(query : str) -> str:
    """Search the web for recent and reliable information on a topic. Returns Titles , URLs and snippets."""
    # Use the Tavily client to search the web with the given query.
    results = tavily.search(query=query,max_results=5)
    
    out = []

    # Iterate through the search results to format the output.
    for r in results['results']:
        out.append(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n"
        )
    
    # join formatted results into a single string.
    return "\n----\n".join(out)

# print(web_search.invoke("what are latest news on foriegn deals of india?"))


# tool for scraping

@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    try:
        # send GET request to the URL with a timeout and user-agent header.
        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"}) 
        # Parse the HTML content of the page.
        soup = BeautifulSoup(resp.text, "html.parser")
        # Remove script, style, nav, and footer tags to clean content.
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        # get clean text from parsed HTML, limited to 3000 characters.
        return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"  # return error if scraping fails.
     
# print(scrape_url.invoke("https://www.bbc.com/news/articles/crrnee01r9jo"))
