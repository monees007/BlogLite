from flask_login import UserMixin

import src.model


class User(UserMixin):
    def __init__(self, mid, name, email, profile_pic):
        self.id = mid
        self.name = name
        self.email = email
        self.profile_pic = profile_pic

    @staticmethod
    def get(user_id):
        db = src.model.get_db()
        print(user_id)
        user = db.execute(
            f"SELECT * FROM user WHERE id = '{user_id}'"
        ).fetchall()[0]
        # user = db.cursor().execute('select * from user where id =(?)', (user_id,).fetchone())
        if not user:
            return None

        user = User(
            mid=user[0],
            name=user[1],
            email=user[2],
            profile_pic=user[3]
        )
        return user

    @staticmethod
    def create(mid, name, email, profile_pic):
        db = src.model.get_db()
        db.execute(
            "Insert into user values(?,?,?,?)",
            (mid, name, email, profile_pic)
        )
        db.commit()
