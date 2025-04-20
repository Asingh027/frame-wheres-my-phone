import asyncio
from frame_sdk import Frame
from frame_sdk.display import Alignment, PaletteColors
from frame_sdk.camera import Quality

async def main():
    async with Frame() as f:
        await f.display.show_text("Tap to take a photo", align=Alignment.MIDDLE_CENTER)
        await f.motion.wait_for_tap()

        await f.display.show_text("Capturing...", align=Alignment.MIDDLE_CENTER)
        photo_bytes = await f.camera.take_photo(autofocus_seconds=1, quality=Quality.MEDIUM)
        await f.display.show_text("Previewing...", align=Alignment.MIDDLE_CENTER)

        # Give user 5 seconds to confirm saving
        await f.display.write_text("Tap to save", 10, 350, color=PaletteColors.GREEN)
        await f.display.show()

        try:
            await asyncio.wait_for(f.motion.wait_for_tap(), timeout=5.0)
            await f.files.write_file("preview-photo.jpg", photo_bytes)
            await f.display.show_text("Saved as preview-photo.jpg", align=Alignment.MIDDLE_CENTER, color=PaletteColors.GREEN)
        except asyncio.TimeoutError:
            await f.display.show_text("Cancelled", align=Alignment.MIDDLE_CENTER, color=PaletteColors.YELLOW)

        await asyncio.sleep(3)
        await f.display.clear()
        await f.display.show()

asyncio.run(main())
