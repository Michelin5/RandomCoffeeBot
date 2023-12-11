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
CREATE TABLE IF NOT EXISTS interests
(
  id INTEGER AUTO_INCREMENT PRIMARY KEY,
  tg INTEGER,
  int1 VARCHAR(50),
  int2 VARCHAR(50),
  int3 VARCHAR(50)
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

UPDATE_USER = """
UPDATE users
SET sex = "{sex}",
    years = {years},
    city = "{city}"
WHERE tg = {tg};
"""

ADD_INTERESTS = """
INSERT INTO interests(tg, int1, int2, int3)
VALUES (
    {tg},
    "{int1}",
    "{int2}",
    "{int3}"
);
"""

UPDATE_INTERESTS = """
UPDATE interests
SET int1 = "{int1}",
    int2 = "{int2}",
    int3 = "{int3}"
WHERE tg = {tg};
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
        cur.execute(CREATE_TABLE_INTERESTS)

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
            UPDATE_USER.format(
                sex=user.sex,
                years=user.years,
                city=user.city,
                tg=user.tg
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

    def add_interests(self,
                      tg,
                      interests):
        conn = sqlite3.connect(self.base_name)
        cur = conn.cursor()

        cur.execute(
            ADD_INTERESTS.format(
                tg=tg,
                int1=interests[0],
                int2=interests[1],
                int3=interests[2],
            )
        )

        conn.commit()
        cur.close()
        conn.close()
    
    def update_interests(self,
                      tg,
                      interests):
        conn = sqlite3.connect(self.base_name)
        cur = conn.cursor()

        cur.execute(
            UPDATE_INTERESTS.format(
                tg=tg,
                int1=interests[0],
                int2=interests[1],
                int3=interests[2],
            )
        )

        conn.commit()
        cur.close()
        conn.close()

    def fetch_interests(self):
        conn = sqlite3.connect(self.base_name)
        cur = conn.cursor()
        
        cur.execute("SELECT tg, int1, int2, int3 FROM interests")
        l = list(cur.fetchall())
        
        cur.close()
        conn.close()
        
        return l
