from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from pydantic import BaseModel

from pytoniq.liteclient import LiteClientError, RunGetMethodError
from pytoniq_core import Address

from .client import get_client, get_balancer
from .contracts_utils import is_payed_for_now, calc_pair_address, get_pair_data
from .config import LS_PUB_KEY
from .utils import check_pub_key_is_valid

router = APIRouter()


class CheckPayedResponse(BaseModel):
    ok: bool
    result: bool
    message: str


class GetPairResponse(BaseModel):
    ok: bool
    result: dict
    message: str


@router.get('/test')
def test():
    return {'ok': True}


def first_checks(pub_key) -> [Address, str]:
    is_valid, message, pub_key = check_pub_key_is_valid(pub_key)
    if not is_valid:
        return_message = 'Invalid public key: ' + message
        return None, return_message
    try:
        address = calc_pair_address(LS_PUB_KEY, pub_key)
        return address, ''
    except Exception as e:
        return_message = f'Failed to calc address: {type(e)}: {e}'
        return None, return_message


@router.get('/checkPayed')
@cache(expire=5)
async def check_payed(
        pub_key: str,
):
    address, message = first_checks(pub_key)
    if not address:
        return {'ok': False, 'message': message, 'result': False}
    try:
        balancer = await get_balancer()
        result = await is_payed_for_now(balancer, address)
    except RunGetMethodError as e:  # probably wrong account
        return {'ok': False, 'message': f'Failed to run get method: {e}', 'result': False}
    except LiteClientError as e:  # probably state doesn't exist
        return {'ok': False, 'message': f'Failed to fetch result: LiteClientError: {e}', 'result': False}
    except Exception as e:
        return {'ok': False, 'message': f'Failed to fetch result: {type(e)}: {e}', 'result': False}
    return {'ok': True, 'message': '', 'result': result}


@router.get('/getPair')
@cache(expire=5)
async def get_pair(
        pub_key: str,
):
    address, message = first_checks(pub_key)
    if not address:
        return {'ok': False, 'message': message, 'result': False}
    try:
        balancer = await get_balancer()
        result = await get_pair_data(balancer, address)
        return {'ok': True, 'message': '', 'result': result}
    except Exception as e:
        return {'ok': False, 'message': f'Failed to fetch result: {type(e)}: {e}', 'result': False}
