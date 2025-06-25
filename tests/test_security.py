from jwt import decode
from fast_zero.security import create_access_token, settings
# from fast_zero.security import (
#     SECRET_KEY,
#     create_access_token,
# )


def test_jwt():
    data = {'test': 'test'}
    token = create_access_token(data)

    decoded = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    assert decoded['test'] == data['test']
    assert 'exp' in decoded
