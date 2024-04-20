import ast
import base64
import logging
import json
from typing import Any, List, Dict, Optional

from mojang._types import UserProfile
from mojang._http_client import _HTTPClient
from mojang.errors import MojangError

_log = logging.getLogger(__name__)

_API_BASE_URL = "https://api.mojang.com"
_SESSIONSERVER_BASE_URL = "https://sessionserver.mojang.com"
_AUTHSERVER_BASE_URL = "https://authserver.mojang.com"

class API(_HTTPClient):
    async def get_uuid(self, username: str, timestamp: Optional[int] = None) -> Optional[str]:
        """Convert a Minecraft name to a UUID. Current implementation ignores the timestamp parameter."""
        url = f"{_API_BASE_URL}/users/profiles/minecraft/{username}"
        if timestamp:
            url += f"?at={timestamp}"

        try:
            resp = await self.request("GET", url, ignore_codes=[400])
            data = await resp.json()
            return data["id"]
        except (KeyError, json.decoder.JSONDecodeError):
            return None

    async def get_uuids(self, names: List[str]) -> Dict[str, str]:
        """Convert up to 10 usernames to UUIDs in a single network request."""
        if len(names) > 10:
            names = names[:10]

        resp = await self.request(
            "POST",
            f"{_API_BASE_URL}/profiles/minecraft",
            ignore_codes=[400],
            json=names,
        )
        data = await resp.json()
        if not isinstance(data, list):
            raise MojangError(response=resp)
        return {name_data["name"]: name_data["id"] for name_data in data}

    async def get_username(self, uuid: str) -> Optional[str]:
        """Convert a UUID to a username."""
        resp = await self.request(
            "GET",
            f"{_SESSIONSERVER_BASE_URL}/session/minecraft/profile/{uuid}",
            ignore_codes=[400],
        )

        try:
            data = await resp.json()
            return data["name"]
        except json.decoder.JSONDecodeError:
            return None

    async def get_profile(self, uuid: str) -> Optional[UserProfile]:
        """Get more information about a user from their UUID."""
        resp = await self.request(
            "GET",
            f"{_SESSIONSERVER_BASE_URL}/session/minecraft/profile/{uuid}",
            ignore_codes=[400],
        )

        try:
            properties = await resp.json()
            value = properties["properties"][0]["value"]
            data = ast.literal_eval(base64.b64decode(value).decode())

            return UserProfile(
                id=data["profileId"],
                timestamp=data["timestamp"],
                name=data["profileName"],
                is_legacy_profile=bool(data.get("legacy")),
                cape_url=data["textures"].get("CAPE", {}).get("url"),
                skin_url=data["textures"].get("SKIN", {}).get("url"),
                skin_variant=data["textures"].get("SKIN", {}).get("metadata", {}).get("model", "classic"),
            )
        except (KeyError, json.decoder.JSONDecodeError):
            return None

    async def get_blocked_servers(self) -> List[str]:
        """Get a list of SHA1 hashes of blacklisted Minecraft servers."""
        resp = await self.request("GET", f"{_SESSIONSERVER_BASE_URL}/blockedservers")
        data = await resp.text()
        return data.splitlines()