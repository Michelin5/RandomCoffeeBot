import sqlite3

CREATE_TABLE_USERS = """
CREATE TABLE IF NOT EXISTS users
(
  id INT AUTO_INCREMENT PRIMARY KEY,
  tg INTEGER,
  sex VARCHAR(50),
  years INTEGER,
  city VARCHAR(50)
);
"""

CREATE_TABLE_INTERESTS = """
CREATE TABLE interests(
    id INT AUTO_INCREMENT PRIMARY KEY,

);
"""

ADD_USER = """
INSERT INTO users(sex, tg, years, city)
VALUES (
    "{sex}",
    {tg},
    {years},
    "{city}"
);
"""

SELECT_USER = """
SELECT sex, tg, years, city FROM users
WHERE tg = {tg};
"""

BASE_NAME = "my_base.db"


class User:
    def __init__(self,
                 tg,
                 sex,
                 years,
                 city,
                 interests=[]):
        self.sex = sex
        self.tg = tg
        self.years = years
        self.city = city
        self.interests = interests


class Base:
    def __init__(self, base_name=BASE_NAME):
        self.base_name = base_name
        conn = sqlite3.connect(self.base_name)
        cur = conn.cursor()

        cur.execute(CREATE_TABLE_USERS)

        conn.commit()
        cur.close()
        conn.close()

    def create_user(self, user):
        conn = sqlite3.connect(self.base_name)
        cur = conn.cursor()

        cur.execute(
            ADD_USER.format(
                tg=user.tg,
                sex=user.sex,
                years=user.years,
                city=user.city,
            )
        )

        conn.commit()
        cur.close()
        conn.close()

    def update_user(self, user):
        # TO_DO
        conn = sqlite3.connect(self.base_name)
        cur = conn.cursor()

        cur.execute(
            ADD_USER.format(
                tg=user.tg,
                sex=user.sex,
                years=user.years,
                city=user.city,
            )
        )

        conn.commit()
        cur.close()
        conn.close()

    def get_user_by_tg_id(self, tg):
        conn = sqlite3.connect(self.base_name)
        cur = conn.cursor()

        cur.execute(
            SELECT_USER.format(
                tg=tg,
            )
        )
        users = cur.fetchall()

        if len(users) == 0:
            return None

        user = User(
            tg=users[0][0],
            sex=users[0][1],
            years=users[0][2],
            city=users[0][3],
            interests=[],
        )

        cur.close()
        conn.close()

        return user

    def add_interests(
            self,
            tg,
            interests,
    ):
        pass
