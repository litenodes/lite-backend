from pytoniq_core import Address, Cell, Slice, StateInit, begin_cell
from pytoniq import LiteClientLike, RunGetMethodError

from .config import PAIR_CODE_BOC, LS_DEPLOYER_CODE_BOC


PAIR_CODE = Cell.one_from_boc('b5ee9c7241020c0100021b000114ff00f4a413f4bcf2c80b0102012004020196f23331d074d721d30801d70130018308d71820d31fd33ffa4030ed44d0d20001f861d3ff01f862fa4001f863d31f01f864fa0001f865d3ff01f866fa4030f86702c000e3025f05841ff2f00300d4f841f2e068f8425250ba8e163401f901f8424130f910f2a3f8008b02585f0370f8618e22f84615ba8e1501f901f8464130f910f2a3f8008b02025f0370f861955f04f2c12ce2e270f861f846f844f842f841c8ca00cbfff843cf16cb1ff845fa02cbfff847cf16c9ed540201480a0502012009060201620807006db282bb51343480007e1874ffc07e18be90007e18f4c7c07e193e80007e1974ffc07e19be900c3e19fe107e10be10fe113e117e11be11e0006fb38ffb51343480007e1874ffc07e18be90007e18f4c7c07e193e80007e1974ffc07e19be900c3e19fe09dbc43e08fe11287e116a006d8220008bbedfb76a268690000fc30e9ff80fc317d2000fc31e98f80fc327d0000fc32e9ff80fc337d20187c33fc20c8b870fc13b7887c11fc2250fc22d400c10498968050dcc8bff038401c0d032d0d3030171b0925f03e0fa403021d749c25f9501d31f3101deed44d0d20001f861d3ff01f862fa4001f863d31f01f864fa0001f865d3ff01f866fa4030f867f843c705f2e065f84158b1f845a73bb9f2e066fa0030f8657ff861f823f8640b0040f846f844f842f841c8ca00cbfff843cf16cb1ff845fa02cbfff847cf16c9ed545f3eb37d')
LS_DEPLOYER_CODE = Cell.one_from_boc('b5ee9c72410208010001d2000114ff00f4a413f4bcf2c80b010202d0030200df69c3232c7c4b2cffe10be80b2405c3e104872328032fffe0a33c5b2c7dc3e80b2ffe2c0b3c5b25c3e11487232c07d0004bd0032c032483e401c1d3232c0b281f2fff2741de0043232c15633c59c3e80b2daf3333260103ec03e117e113e10fe107232fffe10be80b2c7f2c7f3327b55204f5d76d176fd9998e8698180b8d848adf07d201800e98fe99f9141082c6848fcdd4722b61169ffc1846b8c6a1868107c80aa0811fc887951fd00187c215d797032fc21d27c225df9703378037c21d27c31fc22fc227c21fc20e465fffc217d01658fe58fe664f6aa701890e000718110e000718100e00071812dc20fc070605040004f2f000bcf843c200f2e0cad3ff3070f84121c8ca00cbfff828cf16cb1f70fa02cbff8b02cf16c970f84521c8cb01f40012f400cb00c9f9007074c8cb02ca07cbffc9d001c705f2e0caf845f844f843f841c8cbfff842fa02cb1fcb1fccc9ed54db31005e6c218308d71820f901f8414130f910f2a3d31f30f864f845f844f843f841c8cbfff842fa02cb1fcb1fccc9ed54db31006c6c21f843c000f2e0c98308d71820f901f8414130f910f2a3fa0030f862f845f844f843f841c8cbfff842fa02cb1fcb1fccc9ed54db3187f03c42')


def pack_pair_data(ls_pubkey: bytes, user_pub_key: bytes) -> Cell:
    return (begin_cell()
            .store_int(0, 1)
            .store_bytes(ls_pubkey)
            .store_address(calc_ls_deployer_address(ls_pubkey))
            .store_uint(0, 32)
            .store_coins(0)
            .store_bytes(user_pub_key)
            .store_address(None)
            .end_cell())


def calc_pair_address(ls_pubkey: bytes, user_pubkey: bytes):
    data = pack_pair_data(ls_pubkey, user_pubkey)
    state_init = StateInit(data=data, code=PAIR_CODE)
    return Address((0, state_init.serialize().hash))  # pair should be in basechain


def pack_ls_deployer_data(ls_pubkey: bytes) -> Cell:
    return (begin_cell()
            .store_bytes(ls_pubkey)
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
