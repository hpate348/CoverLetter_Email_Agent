# tools/search.py
import os
from dotenv import load_dotenv
load_dotenv()
from tavily import TavilyClient

client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"]) #tavily object to search

def search_company(company_name: str) -> str:
    results = client.search(
        query=f"{company_name} company culture mission recent news hiring",
        max_results=5
    )
    # Return a clean summary string Claude can reason over
    snippets = [r["content"] for r in results["results"]]
    return "\n\n".join(snippets)