import sqlite3
import pandas as pd

CREATE_TABLE_USERS = """
CREATE TABLE IF NOT EXISTS users
(
  id INTEGER AUTO_INCREMENT PRIMARY KEY,
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

CREATE_TABLE_GROUPS = """
CREATE TABLE IF NOT EXISTS groups
(
  id INTEGER AUTO_INCREMENT PRIMARY KEY,
  count INTEGER,
  tg1 INTEGER,
  tg2 INTEGER,
  tg3 INTEGER,
  tg4 INTEGER,
  tg5 INTEGER,
  tg6 INTEGER,
  tg7 INTEGER,
  tg8 INTEGER,
  tg9 INTEGER,
  tg10 INTEGER
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

CREATE_GROUP = """
INSERT INTO groups(count, tg1)
VALUES (
    1,
    {tg}
);
"""

UPDATE_GROUP = """
UPDATE groups
SET count = count + 1,
    {tgn} = {tg}
WHERE id = {group_id};
"""

SELECT_USER = """
SELECT sex, tg, years, city FROM users
WHERE tg = {tg};
"""

SELECT_GROUP_COUNT = """
SELECT count FROM groups
WHERE id = {group_id};
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
        cur.execute(CREATE_TABLE_GROUPS)

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

        cur.execute(
            ADD_INTERESTS.format(
                tg=user.tg,
                int1=user.interests[0].lower(),
                int2=user.interests[1].lower(),
                int3=user.interests[2].lower(),
            )
        )

        conn.commit()
        cur.close()
        conn.close()

    def update_user(self, user):
        conn = sqlite3.connect(self.base_name)
        cur = conn.cursor()

        cur.execute(
            UPDATE_USER.format(
                sex=user.sex,
                years=user.years,
                city=user.city,
                tg=user.tg,
            )
        )

        cur.execute(
            UPDATE_INTERESTS.format(
                tg=user.tg,
                int1=user.interests[0].lower(),
                int2=user.interests[1].lower(),
                int3=user.interests[2].lower(),
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

    def get_group_count_by_id(self, group_id):
        conn = sqlite3.connect(self.base_name)
        cur = conn.cursor()

        cur.execute(
            SELECT_GROUP_COUNT.format(
                group_id=group_id,
            )
        )
        
        count = cur.fetchall()
        
        cur.close()
        conn.close()

        return count[0][0]

    def fetch_interests(self):
        conn = sqlite3.connect(self.base_name)
        cur = conn.cursor()
        
        cur.execute("SELECT tg, int1, int2, int3 FROM interests")
        l = list(cur.fetchall())
        
        cur.close()
        conn.close()
        
        return {l[i][0]: [l[i][1], l[i][2], l[i][3]] for i in range(len(l))}

    def create_group(self,
                     tg):
        conn = sqlite3.connect(self.base_name)
        cur = conn.cursor()

        cur.execute(
            CREATE_GROUP.format(
                tg=tg,
            )
        )

        conn.commit()
        cur.close()
        conn.close()
    
    def add_to_group(self,
                     group_id,
                     tg):
        conn = sqlite3.connect(self.base_name)
        cur = conn.cursor()

        count = self.get_group_count_by_id(group_id)

        cur.execute(
            UPDATE_GROUP.format(
                group_id=group_id,
                tgn="tg"+str(count+1),
                tg=tg,
            )
        )

        conn.commit()
        cur.close()
        conn.close()
