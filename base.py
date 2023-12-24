import sqlite3
from interests import get_data, get_tables, get_group_avgs
import numpy as np

CREATE_TABLE_USERS = """
CREATE TABLE IF NOT EXISTS users
(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  tg INTEGER,
  sex VARCHAR(50),
  years INTEGER,
  city VARCHAR(50)
);
"""

CREATE_TABLE_INTERESTS = """
CREATE TABLE IF NOT EXISTS interests
(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  tg INTEGER,
  int1 VARCHAR(50),
  int2 VARCHAR(50),
  int3 VARCHAR(50)
);
"""

CREATE_TABLE_GROUPS = """
CREATE TABLE IF NOT EXISTS groups
(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
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
INSERT INTO users(tg, sex, years, city)
VALUES (
    {tg},
    "{sex}",
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
SELECT tg, sex, years, city FROM users
WHERE tg = {tg};
"""

SELECT_GROUP_COUNT = """
SELECT count FROM groups
WHERE id = {group_id};
"""

SELECT_GROUP_USERS = """
SELECT tg1, tg2, tg3, tg4, tg5, tg6, tg7, tg8, tg9, tg10 FROM groups
WHERE id = {group_id};
"""

SELECT_GROUP_ID = """
SELECT id FROM groups
WHERE tg1 = {tg}
OR tg2 = {tg}
OR tg3 = {tg}
OR tg4 = {tg}
OR tg5 = {tg}
OR tg6 = {tg}
OR tg7 = {tg}
OR tg8 = {tg}
OR tg9 = {tg}
OR tg10 = {tg};
"""

BASE_NAME = "my_base.db"


class User:
    def __init__(self,
                 tg,
                 sex,
                 years,
                 city,
                 interests=[]):
        self.tg = tg
        self.sex = sex
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
                tgn="tg" + str(count + 1),
                tg=tg,
            )
        )

        conn.commit()
        cur.close()
        conn.close()
        
    def fetch_groups(self):
        conn = sqlite3.connect(self.base_name)
        cur = conn.cursor()
        
        cur.execute("SELECT tg1, tg2, tg3, tg4, tg5, tg6, tg7, tg8, tg9, tg10 FROM groups")
        l = list(cur.fetchall())
        
        cur.close()
        conn.close()
        
        return l

    def fetch_group_user_tgs(self, group_id):
        conn = sqlite3.connect(self.base_name)
        cur = conn.cursor()

        cur.execute(SELECT_GROUP_USERS.format(group_id = group_id))
        l = list(cur.fetchall())

        cur.close()
        conn.close()

        if (len(l)) == 0:
            return None

        l = list(l[0])
        while (l[-1] == None):
            l.pop()

        return l

    def fetch_group_id_by_user(self, tg):
        conn = sqlite3.connect(self.base_name)
        cur = conn.cursor()

        cur.execute(SELECT_GROUP_ID.format(tg = tg))
        l = list(cur.fetchall())

        cur.close()
        conn.close()

        l = [i[0] for i in l]

        return l

    def find_group(self, tg):
        groups = self.fetch_groups()
        user_interests = self.fetch_interests()

        data = get_data(user_interests)
        tables = get_tables(data)
        group_avgs = get_group_avgs(tables, groups)

        list_of_good = []
        
        for group_id in group_avgs.columns:
            difference = np.sqrt(((tables[0][tg] - group_avgs[group_id]) ** 2).sum())
            if (difference < 1.25 and self.get_group_count_by_id(group_id) < 10 and tg not in groups[group_id - 1]):
                list_of_good.append((difference, group_id))

        list_of_good.sort()
        if (len(list_of_good)) == 0:
            return None
        else:
            return list_of_good[0][1]

    def match(self, tg):
        conn = sqlite3.connect(self.base_name)
        cur = conn.cursor()

        user_interests = self.fetch_interests()

        cur.close()
        conn.close()

        data = get_data(user_interests)
        tables = get_tables(data)

        list_of_others = []
        
        for other_tg in tables[0].columns:
            if (other_tg != tg):
                difference = np.sqrt(((tables[0][tg] - tables[0][other_tg]) ** 2).sum())
                list_of_others.append((other_tg, difference))

        list_of_others.sort(key = lambda i: i[1])
        
        if (len(list_of_others)) == 0:
            return None
        else:
            return list_of_others[np.random.randint(0, int(np.sqrt(len(list_of_others))))][0]
