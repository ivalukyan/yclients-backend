from db.database import  Session, BotUser


def get_user_phone_number(user_id: int) -> str:

    db_session = Session()
    user = db_session.query(BotUser).filter(BotUser.telegram_id == user_id).first()

    if not user:
        return ""
    else:
        return user.phone