import asyncio
import datetime
import httpx
import os
from dotenv import load_dotenv
from frame_sdk import Frame
from frame_sdk.display import Alignment, PaletteColors

# Load from .env
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
LOCATION = os.getenv("LOCATION", "New York,US")

async def fetch_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={LOCATION}&appid={API_KEY}&units=imperial"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        data = resp.json()
        desc = data["weather"][0]["description"].title()
        temp = data["main"]["temp"]
        city = data["name"]
        return f"{city}\n{desc}\n{temp:.1f}°F"

async def main():
    async with Frame() as f:
        await f.display.show_text("Tap to get weather", align=Alignment.MIDDLE_CENTER)
        await f.motion.wait_for_tap()

        try:
            weather = await fetch_weather()
            await f.display.clear()
            await f.display.write_text(weather, align=Alignment.MIDDLE_CENTER)
            await f.display.show()
            await asyncio.sleep(6)
        except Exception as e:
            await f.display.show_text("Weather error", align=Alignment.MIDDLE_CENTER, color=PaletteColors.RED)
            await asyncio.sleep(3)

asyncio.run(main())
