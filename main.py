import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile
from aiogram.filters import CommandStart

# Tokeningizni shu yerga yozing
TOKEN = "7698712512:AAG85KmhKwttFUkwPXD1lKRHLxjgbfU_WLA"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def send_images(message: types.Message):
    images = ["images/photo_2025-04-21_22-46-26.jpg", "images/photo_2025-04-21_22-46-26 (2).jpg"]  # faqat 2 ta rasm

    media_group = []
    for img in images:
        media_group.append(types.InputMediaPhoto(media=FSInputFile(img)))

    await message.answer_media_group(media=media_group)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
