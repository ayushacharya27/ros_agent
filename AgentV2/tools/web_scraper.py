from firecrawl import FirecrawlApp
from langchain_core.tools import tool
from dotenv import load_dotenv
import os

load_dotenv()

app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

# This all is Done From the Documnetation no Changes

@tool
def search_ros2_docs(query: str) -> str:
    """
    Search the web for ROS2-related documentation, tutorials, or answers.
    Use this when you need to find how to do something in ROS2.
    
    Args:
        query: What you want to know about ROS2
    """
    try:
        results = app.search(
            query=f"ROS2 {query}",
            limit=3,
            scrape_options={"formats": ["markdown"]}
        )
        
        output = []
        for r in results.data:
            title    = getattr(r, "title", "No Title")
            url      = getattr(r, "url", "")
            markdown = getattr(r, "markdown", "") or getattr(r, "description", "")
            
            output.append(f"### {title}\nURL: {url}\n\n{markdown}")
        
        return "\n\n---\n\n".join(output) if output else "No results found."
    
    except Exception as e:
        return f"Search failed: {str(e)}"


@tool
def scrape_ros2_page(url: str) -> str:
    """
    Scrape a specific ROS2 documentation or tutorial page for detailed content.
    Use this when you already have a URL and need the full content.
    
    Args:
        url: The URL of the ROS2 docs page to scrape
    """
    try:
        result = app.scrape_url(
            url,
            formats=["markdown"],
            only_main_content=True
        )
        
        return result.markdown or "No content found."
    
    except Exception as e:
        return f"Scrape failed: {str(e)}"