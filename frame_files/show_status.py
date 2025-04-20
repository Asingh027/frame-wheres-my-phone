import asyncio
import datetime
from frame_sdk import Frame
from frame_sdk.display import Alignment, PaletteColors

async def show_battery_time(f: Frame):
    batteryPercent = await f.get_battery_level()
    color = (
        PaletteColors.RED if batteryPercent < 20
        else PaletteColors.YELLOW if batteryPercent < 50
        else PaletteColors.GREEN
    )

    batteryWidth = 150
    batteryHeight = 75

    # Battery icon
    await f.display.draw_rect(640 - 32, 40 + batteryHeight // 2 - 8, 32, 16, PaletteColors.WHITE)
    await f.display.draw_rect_filled(
        640 - 16 - batteryWidth, 40 - 8, batteryWidth + 16, batteryHeight + 16,
        1, PaletteColors.WHITE, PaletteColors.YELLOW
    )
    await f.display.draw_rect(
        640 - 8 - batteryWidth, 40,
        int(batteryWidth * 0.01 * batteryPercent),
        batteryHeight, color
    )
    await f.display.write_text(
        f"{batteryPercent}%", 640 - 8 - batteryWidth, 40,
        batteryWidth, batteryHeight, Alignment.MIDDLE_CENTER
    )

    # Date/time
    now = datetime.datetime.now()
    await f.display.write_text(
        now.strftime("%#I:%M %p\n%a, %B %d, %Y").lstrip("0"),
        align=Alignment.MIDDLE_CENTER
    )

    await f.display.show()


async def main():
    async with Frame() as f:
        showing = False
        #await f.display.show_text("Tap to toggle time & battery", align=Alignment.MIDDLE_CENTER)

        while True:
            await f.motion.wait_for_tap()

            if showing:
                await f.display.clear()
                await f.display.show()
                showing = False
            else:
                await f.display.clear()
                await show_battery_time(f)
                showing = True

asyncio.run(main())
