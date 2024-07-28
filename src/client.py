import asyncio
import httpx
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.asyncio import connect
from aioquic.quic.configuration import QuicConfiguration
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.asyncio import connect
from httpx import AsyncClient

async def main():
    configuration = QuicConfiguration(is_client=True)
    configuration.verify_mode = False  # For testing purposes; remove in production

    async with connect(
        "localhost",
        4443,
        configuration=configuration,
    ) as protocol:
        async with AsyncClient(http2=True, transport=protocol) as client:
            response = await client.get("https://localhost:4443")
            print(response.status_code)
            print(response.text)

if __name__ == "__main__":
    asyncio.run(main())
