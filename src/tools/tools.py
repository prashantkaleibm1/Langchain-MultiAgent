from langchain.tools import tool
from requests import request
from dotenv import load_dotenv
import os
from tavily import TavilyClient
from rich import print
from bs4 import BeautifulSoup
import trafilatura
import readability
from readability import Document

load_dotenv()
tavily=TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query:str) -> str: 
    """ search the web for the recent and reliable information on the topic"""
    results=tavily.search(query=query,max_results=5)
    
    out=[]
    
    for r in results['results']:
        out.append(
            f"Title : {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n"
        )
    
    print(results)
    return "\n-------\n".join(out)

##### Scrape content from URL###############

import requests


@tool
def scrape_url(url: str) -> str:
    """Scrape webpage text using multiple extraction strategies."""

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/130.0.0.0 Safari/537.36"
        ),
        "Accept": (
            "text/html,application/xhtml+xml,application/xml;"
            "q=0.9,image/avif,image/webp,*/*;q=0.8"
        ),
        "Accept-Language": "en-US,en;q=0.9,de;q=0.8",
        "Referer": "https://www.google.com/",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    try:
        with requests.Session() as session:
            session.headers.update(headers)

            response = session.get(
                url,
                timeout=20,
                allow_redirects=True
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # Strategy 1: Extract article/main content
            for selector in [
                "article",
                "main",
                '[role="main"]',
                ".article-content",
                ".post-content",
                "#content",
            ]:
                element = soup.select_one(selector)
                if element:
                    text = element.get_text(" ", strip=True)
                    if len(text) > 100:
                        return text

            # Strategy 2: Remove non-content elements
            for element in soup.select(
                "script, style, noscript, svg, nav, footer, "
                "header, aside, form"
            ):
                element.decompose()

            # Strategy 3: Extract paragraphs and headings
            blocks = soup.select("h1, h2, h3, p, li, blockquote")
            text = "\n".join(
                block.get_text(" ", strip=True)
                for block in blocks
                if block.get_text(strip=True)
            )

            if len(text.strip()) > 100:
                return text

            # Strategy 4: Fall back to all remaining page text
            text = soup.get_text(separator=" ", strip=True)

            if text:
                return text

            return "No readable text found on the webpage."

    except requests.exceptions.Timeout:
        return f"Timeout error while accessing: {url}"

    except requests.exceptions.HTTPError as e:
        return f"HTTP error: {e}"

    except requests.exceptions.ConnectionError as e:
        return f"Connection error: {e}"

    except requests.exceptions.RequestException as e:
        return f"Request error: {e}"

    except Exception as e:
        return f"Unexpected error: {e}"


# Example usage
if __name__ == "__main__":
    url = "https://example.com"
    content = scrape_url(url)
    print(content)
