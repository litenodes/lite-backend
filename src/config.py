import base64
import os

LS_PORT: int = int(os.environ.get('LS_PORT'))
LS_PUB_KEY_B64: str = os.environ.get('LS_PUB_KEY')
LS_PUB_KEY: bytes = base64.b64decode(LS_PUB_KEY_B64)
