```Async-Mojang``` is a Python package for accessing Mojang's services. This library can be used to convert UUIDs, get a profile's information, change your Minecraft username or skin, and much more. 

There is one component to this package:

- **Public API** - Used to parse information about Minecraft profiles and more. Authentication is not required.

## Installation
**Python 3.7 or higher is required.**

The easiest way to install the library is using `pip`. Just run the following console command:

```
pip install async-mojang
```

## **Public API Quickstart**
```py
import asyncio
from async_mojang import API

async def get_uuid(username: str):
    async with API() as api:
        uuid = await api.get_uuid(username)
        return uuid

async def get_formatted_uuid(username: str):
    async with API() as api:
        formatted_uuid = await api.get_formatted_uuid(username)
        return formatted_uuid

async def get_stripped_uuid(username: str):
    async with API() as api:
        stripped_uuid = await api.get_stripped_uuid(username)
        return stripped_uuid

async def get_username(uuid: str):
    async with API() as api:
        username = await api.get_username(uuid)
        return username

async def get_profile(uuid: str):
    async with API() as api:
        profile = await api.get_profile(uuid)
        return profile

async def get_blocked_servers():
    async with API() as api:
        blocked_servers = await api.get_blocked_servers()
        return blocked_servers

async def main():
    uuid = await get_uuid("FroostySnoowman")
    print(uuid)

    formatted_uuid = await get_formatted_uuid("FroostySnoowman")
    print(formatted_uuid)

    stripped_uuid = await get_stripped_uuid("FroostySnoowman")
    print(stripped_uuid)

    username = await get_username(uuid)
    print(username)

    profile = await get_profile(uuid)
    print(profile)

    blocked_servers = await get_blocked_servers()
    print(blocked_servers)

if __name__ == "__main__":
    asyncio.run(main())
```