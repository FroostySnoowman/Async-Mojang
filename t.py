import asyncio
from mojang import API

# Initialize the API client outside of the function, ensuring proper lifecycle management.
api = API()

async def get_uuid(username: str):
    # Ensure you call `api.get_uuid` to fetch UUID.
    uuid = await api.get_uuid(username)
    return uuid

async def main():
    async with api:
        uuid = await get_uuid("FroostySnoowman")
        print(uuid)

if __name__ == "__main__":
    asyncio.run(main())