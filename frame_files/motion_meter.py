import asyncio
from frame_sdk import Frame
from frame_sdk.display import PaletteColors

async def main():
    async with Frame() as f:
        await f.display.show_text("Move to charge the meter!", align="middle_center")

        max_intensity = 0.0
        prev = await f.motion.get_direction()

        for i in range(30):
            await asyncio.sleep(0.1)
            direction = await f.motion.get_direction()
            delta = (direction - prev).amplitude()
            max_intensity = max(max_intensity, delta)
            bar_width = min(int(delta * 400), 400)

            await f.display.clear()
            await f.display.draw_rect(120, 180, bar_width, 40, PaletteColors.GREEN)
            await f.display.show()
            prev = direction

        await f.display.show_text("Done!", align="middle_center")
        await asyncio.sleep(2)

asyncio.run(main())
