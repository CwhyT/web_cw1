import httpx

OPEN_LIBRARY_BASE_URL = "https://openlibrary.org"


async def fetch_search_results(query: str, limit: int = 10) -> dict:
    async with httpx.AsyncClient(base_url=OPEN_LIBRARY_BASE_URL, timeout=10.0) as client:
        response = await client.get("/search.json", params={"q": query, "limit": limit})
        response.raise_for_status()
        return response.json()


async def fetch_work_details(openlibrary_key: str) -> dict:
    path = openlibrary_key if openlibrary_key.startswith("/") else f"/works/{openlibrary_key}"
    async with httpx.AsyncClient(base_url=OPEN_LIBRARY_BASE_URL, timeout=10.0) as client:
        response = await client.get(f"{path}.json")
        response.raise_for_status()
        return response.json()

