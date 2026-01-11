import asyncio
from aiogram import Bot, Dispatcher, types
from playwright.async_api import async_playwright
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

BOT_TOKEN = "8133122805:AAEGRJHcMuV4hG-NYelb1aVKgKdixoo2oVI"

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Отправить ссылку")]],
    resize_keyboard=True
)

@dp.message(commands=["start"])
async def start_cmd(message: types.Message):
    await message.answer(
        "Нажми кнопку ниже и отправь ссылку на game pass",
        reply_markup=keyboard
    )

@dp.message()
async def handle_message(message: types.Message):
    if not message.text or "roblox.com/game-pass" not in message.text:
        return

    await message.answer("⏳ Обрабатываю ссылку...")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.goto(message.text, timeout=60000)
        await page.wait_for_timeout(5000)

        await page.evaluate("""
            () => {
                document.querySelectorAll("button").forEach(btn => {
                    if (btn.innerText && btn.innerText.includes("Buy")) {
                        btn.innerText = "Inventory";
                    }
                });
            }
        """)

        await page.wait_for_timeout(1000)
        await page.screenshot(path="result.png", full_page=True)
        await browser.close()

    await message.answer_photo(types.FSInputFile("result.png"))

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
