import httpx
import pytest
from pytest_httpx import HTTPXMock
from contextlib import nullcontext as does_not_raise

from main import run


@pytest.mark.asyncio
async def test_main(httpx_mock: HTTPXMock):
    httpx_mock.add_response(method="POST", status_code=httpx.codes.TOO_MANY_REQUESTS, json={})
    httpx_mock.add_response(method="POST", status_code=httpx.codes.OK, json={
        "id": 1,
    })

    # It should not throw, because the second request shall pass
    with does_not_raise():
        response = await run()
        assert response is not None