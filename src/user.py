from flask_login import UserMixin

import src.model


class User(UserMixin):
    def __init__(self, mid, name, email, profile_pic):
        self.id = mid
        self.name = name
        self.email = email
        self.username = email.split("@")[0]
        self.profile_pic = profile_pic

    @staticmethod
    def get(user_id):
        db = src.model.get_db()
        # print(user_id)
        user = db.execute(
            f"SELECT * FROM user WHERE id = '{user_id}'"
        ).fetchall()[0]
        # user = db.cursor().execute('select * from user where id =(?)', (user_id,).fetchone())
        if not user:
            return None

        user = User(
            mid=user['id'],
            name=user['name'],
            email=user['email'],
            profile_pic=user['profile_pic']
        )
        return user


    @staticmethod
    def get_email(user_id):
        db = src.model.get_db()
        # print(user_id)
        user = db.execute(
            f"SELECT * FROM user WHERE email = '{user_id}'"
        ).fetchall()[0]
        # user = db.cursor().execute('select * from user where id =(?)', (user_id,).fetchone())
        if not user:
            return None

        user = User(
            mid=user['id'],
            name=user['name'],
            email=user['email'],
            profile_pic=user['profile_pic']
        )
        return user

    @staticmethod
    def create(mid, name, email, profile_pic, password=None):
        db = src.model.get_db()
        db.execute(
            "Insert into user values(?,?,?,?)",
            (mid, name, email, profile_pic)
        )
        db.commit()

    @staticmethod
    def get_uname( uid):
        db = src.model.get_db()
        # print(user_id)
        user = db.execute(
            f"SELECT * FROM users WHERE username = '{uid}'"
        ).fetchall()[0]
        # user = db.cursor().execute('select * from user where id =(?)', (user_id,).fetchone())
        if not user:
            return None

        return user
