import asyncio
import logging
from typing import Any, List, Optional

import aiohttp

from http.client import HTTPConnection

from async_mojang.errors import (
    MojangError,
    BadRequest,
    Forbidden,
    NotFound,
    TooManyRequests,
    ServerError,
    Unauthorized,
)

_log = logging.getLogger(__name__)

class _HTTPClient:
    def __init__(
        self,
        session: Optional[aiohttp.ClientSession] = None,
        retry_on_ratelimit: Optional[bool] = False,
        ratelimit_sleep_time: Optional[int] = 60,
        debug_mode: Optional[bool] = False,
    ):
        self.ratelimit_sleep_time = ratelimit_sleep_time
        self.retry_on_ratelimit = retry_on_ratelimit
        self.session = session or aiohttp.ClientSession(
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}
        )

        if debug_mode:
            HTTPConnection.debuglevel = 1
            logging.basicConfig()
            logging.getLogger().setLevel(logging.DEBUG)
            aiohttp_log = logging.getLogger("aiohttp.client")
            aiohttp_log.setLevel(logging.DEBUG)
            aiohttp_log.propagate = True

    async def request(
        self,
        method: str,
        url: str,
        ignore_codes: Optional[List[int]] = None,
        **kwargs: Any,
    ) -> Any:
        """Internal request handler using aiohttp"""
        async with self.session.request(method, url, **kwargs) as resp:
            _log.debug(f"Making API request: {method} {url}\n")
            await resp.read()  # Ensure the whole response is read

            if resp.ok:
                return resp

            if ignore_codes and resp.status in ignore_codes:
                return resp

            if resp.status == 400:
                raise BadRequest

            if resp.status == 401:
                raise Unauthorized

            if resp.status == 403:
                raise Forbidden

            if resp.status == 404:
                raise NotFound

            if resp.status == 429:
                if self.retry_on_ratelimit:
                    _log.warning(f"We are being ratelimited. Sleeping for {self.ratelimit_sleep_time} seconds.")
                    await asyncio.sleep(self.ratelimit_sleep_time)
                    return await self.request(method, url, ignore_codes, **kwargs)
                else:
                    raise TooManyRequests

            if resp.status >= 500:
                raise ServerError

            raise MojangError(response=resp)

    async def close(self):
        """Close the aiohttp session."""
        await self.session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()