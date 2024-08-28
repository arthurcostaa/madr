from sqlalchemy import select

from madr.models import Novelist, User


def test_create_user(session):
    new_user = User(
        username='arthur', email='arthur@email.com', password='pwd123'
    )
    session.add(new_user)
    session.commit()

    user_db = session.scalar(select(User).where(User.username == 'arthur'))

    assert user_db.id == 1


def test_create_novelist(session):
    new_novelist = Novelist(name='Clarice Lispector')
    session.add(new_novelist)
    session.commit()

    novelist_db = session.scalar(
        select(Novelist).where(Novelist.name == 'Clarice Lispector')
    )

    assert novelist_db.id == 1
