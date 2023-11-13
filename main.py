import asyncio

from httpx import AsyncClient

from http_utils import AsyncRetryTransport

async def run():
    client = AsyncClient(
        transport=AsyncRetryTransport(retries=2)
    )
    result = await client.post(url="https://jsonplaceholder.typicode.com/posts", json={
        "title": "foo",
        "body": "bar",
        "userId": 1,
    })

    if result.is_success:
        return result.json()
    else:
        raise Exception("Failed to create a resource.")

if __name__ == '__main__':
    asyncio.run(run())

