from pytoniq_core import Address, Cell, Slice, StateInit, begin_cell
from pytoniq import LiteClientLike


PAIR_CODE = Cell.one_from_boc('')
LS_DEPLOYER_CODE = Cell.one_from_boc('')


def pack_pair_data(ls_pubkey: bytes, user_pub_key: bytes) -> Cell:
    return (begin_cell()
            .store_int(0, 1)
            .store_uint(ls_pubkey, 256)
            .store_address(calc_ls_deployer_address(ls_pubkey))
            .store_uint(0, 32)
            .store_coins(0)
            .store_uint(user_pub_key, 256)
            .store_address(None)
            .end_cell())


def calc_pair_address(ls_pubkey: bytes, user_pubkey: bytes, ):
    data = pack_pair_data(ls_pubkey, user_pubkey)
    state_init = StateInit(data=data, code=PAIR_CODE)
    return Address((0, state_init.serialize().hash))  # pair should be in basechain


def pack_ls_deployer_data(ls_pubkey: bytes) -> Cell:
    return (begin_cell()
            .store_uint(ls_pubkey, 256)
            .store_coins(0)
            .store_uint(0, 32)
            .store_uint(0, 32)
            .store_ref(PAIR_CODE)
            .end_cell())


def calc_ls_deployer_address(ls_pubkey: bytes):
    data = pack_ls_deployer_data(ls_pubkey)
    state_init = StateInit(data=data, code=LS_DEPLOYER_CODE)
    return Address((0, state_init.serialize().hash))  # ls_deployer should be in basechain


async def get_pair_data(client: LiteClientLike, address: str):
    result = await client.run_get_method(address, 'get_pair_data', [])
    # todo: parse data to dict
    return {}


async def get_pair_state_init(client: LiteClientLike, address: str):
    return await client.get_account_state(address)


async def is_payed_for_now(client: LiteClientLike, address: str) -> bool:
    return (await client.run_get_method(address, 'payed_for_now?', []))[0] == -1
