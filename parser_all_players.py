import aiohttp
import asyncio
import pandas as pd
from tqdm import tqdm

async def fetch_page(session, page):
    url = f"https://hearthstone.blizzard.com/api/community/leaderboardsData?region=EU&leaderboardId=battlegrounds&page={page}"
    try:
        async with session.get(url) as response:
            return await response.json()
    except Exception as e:
        print(f"Ошибка на странице {page}: {str(e)}")
        return None


async def main():
    all_data = []
    connector = aiohttp.TCPConnector(limit_per_host=10)

    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [fetch_page(session, page) for page in range(1, 730)]

        for future in tqdm(asyncio.as_completed(tasks), total=len(tasks)):
            data = await future
            if data and "leaderboard" in data:
                for player in data['leaderboard']['rows']:
                    all_data.append({
                        "Rank": player["rank"],
                        "Player": player["accountid"],
                        "Rating": player["rating"]
                    })

    df = pd.DataFrame(all_data)
    df.to_excel("hs_bg_api_leaderboard_async.xlsx", index=False)


if __name__ == "__main__":
    asyncio.run(main())