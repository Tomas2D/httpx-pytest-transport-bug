import asyncio
from typing import List, Optional

import httpx
from httpx import HTTPStatusError, Request, RequestError, Response

__all__ = ["AsyncRetryTransport"]


class AsyncRetryTransport(httpx.AsyncHTTPTransport):
    def __init__(self, *args, retry_status_codes: Optional[List[int]] = None, backoff_factor: float = 0.2, **kwargs):
        self.retry_status_codes = retry_status_codes or [
            httpx.codes.TOO_MANY_REQUESTS,
            httpx.codes.BAD_GATEWAY,
            httpx.codes.SERVICE_UNAVAILABLE,
        ]
        self.backoff_factor = backoff_factor
        self.retries = kwargs.get("retries", 0)
        super().__init__(*args, **kwargs)

    def _get_retry_delays(self):
        yield 0
        for i in range(self.retries):
            yield self.backoff_factor * (2**i)

    async def handle_async_request(
        self,
        request: Request,
    ) -> Response:
        latest_err: Optional[Exception] = None

        for delay in self._get_retry_delays():
            if delay > 0:
                await asyncio.sleep(delay)

            try:
                response = await super().handle_async_request(request)
                response.request = request
                response.raise_for_status()
                return response
            except HTTPStatusError as ex:
                latest_err = ex
                if ex.response.status_code in self.retry_status_codes:
                    continue
                raise ex

        raise RequestError(f"Failed to handle request to {request.url}", request=request) from latest_err
