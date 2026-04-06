---
name: web-scraper
description: >
  Build web scrapers for data collection and research. Invoke for: "scrape this website",
  "web scraping", "extract data from", "crawl", "collect data from web",
  "automate data collection", "fetch and parse HTML".
argument-hint: URL or site to scrape and data to extract
allowed-tools: Read, Write, WebFetch, WebSearch
---

# Skill: Web Scraper — Automated Data Collection
**Category:** Optimization/Research

## Role
Build ethical, respectful web scrapers for research data collection.

## When to invoke
- "collect data from X website"
- Research data gathering
- Monitoring web content for changes
- Bulk content extraction

## Instructions
1. Check robots.txt before scraping
2. Rate limit: never more than 1 request/second without permission
3. Use WebFetch for individual pages, design crawler for multiple
4. Parse: BeautifulSoup for HTML, cssselect for specific elements
5. Store: save to data/outputs/ with source URL and timestamp
6. Ethics: don't scrape private/sensitive data, respect ToS

## Output format
```python
# Scraper pattern
def scrape_page(url: str) -> dict:
    html = fetch(url)
    soup = BeautifulSoup(html, 'html.parser')
    return {
        "url": url,
        "title": soup.find("h1").text,
        "content": ...,
        "scraped_at": datetime.now().isoformat()
    }
```

## Example
/web-scraper collect AI research blog posts from arxiv.org for the research pipeline
