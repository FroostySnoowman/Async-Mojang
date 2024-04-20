```Async-Mojang``` is a Python package for accessing Mojang's services. This library can be used to convert UUIDs, get a profile's information, change your Minecraft username or skin, and much more. 

There is one component to this package:

- **Public API** - Used to parse information about Minecraft profiles and more. Authentication is not required.

## Installation
**Python 3.7 or higher is required.**

The easiest way to install the library is using `pip`. Just run the following console command:

```
pip install -U git+https://github.com/FroostySnoowman/Async-Mojang
```

## **Public API Quickstart**

```py
from mojang import API

async def get_uuid(username: str):
    async with API() as api:
        uuid = await api.get_uuid(username)
        return uuid

async def get_username(uuid: str):
    async with API() as api:
        username = await api.get_username(uuid)
        return username
```