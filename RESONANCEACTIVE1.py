# filename: main.py
import os
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
import discord
from discord.ext import commands

# ------------------- Discord bot -------------------
TOKEN = "Discord Token"
bot = commands.Bot(command_prefix="!")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} готов!")

# ------------------- FastAPI -------------------
app = FastAPI()

@app.post("/")
async def interactions(req: Request):
    data = await req.json()
    print("Получен запрос от Discord:", data)
    return JSONResponse(content={"type": 1})

# ------------------- Запуск вместе -------------------
async def start_bot():
    await bot.start(TOKEN)

if __name__ == "__main__":
    import threading

    # Запуск FastAPI
    def run_fastapi():
        PORT = int(os.environ.get("PORT", 8000))
        uvicorn.run(app, host="0.0.0.0", port=PORT)

    threading.Thread(target=run_fastapi, daemon=True).start()

    # Запуск Discord бота в основном потоке
    asyncio.run(start_bot())
