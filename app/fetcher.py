import httpx
import logging

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

async def fetch_sector_news(sector: str) -> str:
    query = f"{sector} sector market news India"
    url = f"https://duckduckgo.com/html?q={query}"

    try:
        logger.info(f"Fetching news for sector: {sector}")
        async with httpx.AsyncClient(follow_redirects=True) as client:  # <--- important!
            response = await client.get(url, headers=HEADERS)

            if response.status_code != 200:
                logger.error(f"Failed to fetch data for {sector}. Status: {response.status_code}")
                raise Exception("Failed to fetch data from DuckDuckGo")

            return response.text[:3000]  # increased limit
    except Exception as e:
        logger.error(f"Error fetching news for {sector}: {str(e)}")
        raise