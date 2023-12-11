import pandas as pd
import numpy as np
import sqlite3

def get_data(user_interests):
    word_bag = set()
    for i in user_interests:
        word_bag = word_bag.union(set(user_interests[i]))
    word_bag = sorted(list(word_bag))
    return((word_bag, user_interests))

def get_tables(data):
    word_bag = data[0]
    user_interests = data[1]
    table = pd.DataFrame(data = np.zeros([len(word_bag), len(user_interests)]), index = word_bag, columns = user_interests)
    term_frequencies = pd.DataFrame(data = np.zeros([len(word_bag), 2]), index = word_bag, columns = ["df", "idf"])
    for i in user_interests:
        for j in range(3):
            table[i][user_interests[i][j]] += 1
    term_frequencies["df"] = table.sum(axis = 1)
    term_frequencies["idf"] = np.log((len(user_interests) + 1) / (term_frequencies["df"] + 1)) + 1
    for i in table.columns:
        table[i] *= term_frequencies["idf"]
        table[i] /= np.sqrt((table[i] ** 2).sum())
    return (table, term_frequencies)

def get_group_avgs(tables, groups):
    ppl_table = tables[0]
    group_ids = [i + 1 for i in range(len(groups))]
    groups_table = pd.DataFrame(data = np.zeros([len(ppl_table.index), len(group_ids)]), index = ppl_table.index, columns = group_ids)
    for group_id in group_ids:
        counter = 0
        for member in groups[group_id - 1]:
            if (member == None):
                break
            counter += 1
            groups_table[group_id] += ppl_table[member]
        groups_table[group_id] /= counter
    return groups_table
