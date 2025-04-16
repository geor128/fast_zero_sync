from fast_zero.models import User
from sqlalchemy import create_engine

def test_create_user():
    engine = create_engine(
        'sqlite:///:memory:'
    )

    user = User(
        username='dunossauro',
        email='geor128@gmail.com',
        password='minha_senha-boa',
    )

    assert user.username == 'dunossauro'
