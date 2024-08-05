from sqlalchemy import select

from madr.models import User


def test_create_user(session):
    new_user = User(
        username='arthur', email='arthur@email.com', password='pwd123'
    )
    session.add(new_user)
    session.commit()

    user_db = session.scalar(select(User).where(User.username == 'arthur'))

    assert user_db.id == 1
