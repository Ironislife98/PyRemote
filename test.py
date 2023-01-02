import asyncio
from typing import Callable


async def doSomething():
    print("Hello World")


async def wait(duration: int, func: Callable):
    await func()

asyncio.run(wait(3, doSomething))


