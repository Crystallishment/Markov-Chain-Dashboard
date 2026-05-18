import pandas as pd
from sqlalchemy import create_engine
from config import DB_URL, TABLE_NAME

def build_matrix():
    engine = create_engine(DB_URL)
    df = pd.read_sql(f"SELECT previous_page_path, page_path FROM {TABLE_NAME} WHERE previous_page_path IS NOT NULL", engine)

    counts = df.groupby(['previous_page_path', 'page_path']).size().unstack(fill_value=0)
    probability_matrix = counts.div(counts.sum(axis=1), axis=0)
    probability_dict = {
        row: dict(probability_matrix.loc[row])
        for row in probability_matrix.index
    }
    state_list = list(probability_dict.keys())
    return state_list, probability_dict

if __name__ == '__main__':
    state_list, probability_dict = build_matrix()
    print(state_list)
    print(probability_dict)