import asyncio
from dataclasses import dataclass

import aiohttp
import fire
import requests

import models

MAX_CONCURRENCY = 2_000
URL = "http://localhost:7777/"


@dataclass
class HttpResponse:
    status: int
    text: str
    obj: models.Hello
    data: dict | None = None


def sequential_requests(n_requests: int):
    url = URL

    responses: list[HttpResponse] = []
    for _ in range(n_requests):
        response = requests.get(url)
        obj = models.Hello.model_validate_json(response.text)
        responses.append(HttpResponse(status=response.status_code, text=response.text, obj=obj))

    print("sequential done")


async def async_request(sem: asyncio.Semaphore, session) -> HttpResponse:
    async with sem:
        async with session.get(URL) as resp:
            status = resp.status
            text = await resp.text()

    obj = models.Hello.model_validate_json(text)
    return HttpResponse(status=status, text=text, obj=obj)


async def async_requests(n_requests: int, max_concurrent: int):
    sem = asyncio.Semaphore(max_concurrent)

    async with aiohttp.ClientSession() as session:
        coroutines = [asyncio.create_task(async_request(sem, session)) for _ in range(n_requests)]
        results = await asyncio.gather(*coroutines)

    print("async done")


def async_main(n_requests: int, max_concurrent: int = MAX_CONCURRENCY):
    asyncio.run(async_requests(n_requests, max_concurrent))


if __name__ == "__main__":
    fire.Fire({"async": async_main, "sequential": sequential_requests})
