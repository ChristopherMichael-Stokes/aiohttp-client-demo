import asyncio

from fastapi import FastAPI

from models import Hello

app = FastAPI()


# TODO: make endpoint to generate some random client looking data
@app.get("/")
async def root() -> Hello:
    # await asyncio.sleep(random.uniform(0.5, 7))
    await asyncio.sleep(2)
    return Hello(message="Hello world")
