

def check_pub_key_is_valid(pub_key: str) -> [bool, str, bytes]:
    try:
        pub_key = bytes.fromhex(pub_key)
    except ValueError:
        return False, 'Invalid hex', b''
    if len(pub_key) != 32:
        return False, 'Invalid length', b''
    if pub_key[:1] * 32 == pub_key:  # fixme: maybe remove?
        return False, 'All bytes are same', b''
    return True, '', pub_key
