from pytoniq import LiteClient, LiteBalancer

from .config import LS_PORT, LS_PUB_KEY_B64


client = LiteClient(
    host='127.0.0.1',
    port=LS_PORT,
    server_pub_key=LS_PUB_KEY_B64,
    timeout=6,
    trust_level=2  # we can fully trust own liteserver
)

balancer = LiteBalancer([client], timeout=6)
# balancer = LiteBalancer.from_mainnet_config(1)


async def get_client():
    if not client.inited:
        await client.connect()
    return client


async def get_balancer():
    if not balancer._alive_peers:
        try:
            await balancer.close_all()
        except:
            pass
        await balancer.start_up()
    return balancer
