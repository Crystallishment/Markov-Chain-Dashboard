import pandas as pd
from sqlalchemy import create_engine
from config import DB_URL, TABLE_NAME


def import_data(file):
    df = pd.read_csv(file)

    engine = create_engine(DB_URL)
    df.to_sql(TABLE_NAME, engine, if_exists='replace', index=False)

    return len(df)
