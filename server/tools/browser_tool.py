import asyncio
from playwright.async_api import async_playwright

async def scrape_web_page(url):
    try:
        async with async_playwright() as p:
            # Launch in headless mode
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, wait_until="networkidle", timeout=10000)
            title = await page.title()
            text = await page.evaluate("() => document.body.innerText")
            await browser.close()
            # Return cropped output to save context window tokens
            return {
                "title": title,
                "content": text[:1200]
            }
    except Exception as e:
        return {"error": f"Playwright browser scrape failed: {e}"}

def search_duckduckgo(query):
    # Synchronous helper to fetch DDG results without complexity
    try:
        import requests
        url = f"https://html.duckduckgo.com/html/?q={query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=5)
        if resp.status_code == 200:
            return resp.text[:2000] # return raw html excerpt
    except Exception as e:
         pass
    return f"No direct internet results found for: {query}"
