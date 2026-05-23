from langchain.tools import tool
import requests 
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
load_dotenv()

# create first agent - Tavily web search agent
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# tool
@tool
def web_search(query : str) -> str:
    """Search the web for recent and reliable information on a topic. Returns Titles , URLs and snippets."""
    results = tavily.search(query=query,max_results=5)
    
    out = []

    for r in results['results']:
        out.append(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n"
        )
    
    return "\n----\n".join(out)

# print(web_search.invoke("what are latest news on foriegn deals of india?"))


 
