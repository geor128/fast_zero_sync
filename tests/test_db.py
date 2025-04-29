from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    # engine = create_engine('sqlite:///database.db')
    # engine = create_engine(
    #     'sqlite:///:memory:'
    # )  # é um banco em memória que criar no test e recria novamente
    # table_registry.metadata.create_all(engine)
    # with Session(engine) as session:
    user = User(
        username='dunossauro2',
        email='dunasauro2@gmail.com',
        password='minha_senha-boa',
    )
    session.add(user)
    session.commit()
    # session.srefresh(user)
    result = session.scalar(
        select(User).where(User.email == 'dunasauro2@gmail.com')
    )
    assert result.username == 'dunossauro2'
