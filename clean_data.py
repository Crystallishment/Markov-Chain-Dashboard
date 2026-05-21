from sqlalchemy import create_engine, text
from config import DB_URL, TABLE_NAME, PAGES


def clean_data():
    engine = create_engine(DB_URL)
    with engine.connect() as conn:
        conn.execute(text(f"CREATE TABLE IF NOT EXISTS {TABLE_NAME}_backup AS SELECT * FROM {TABLE_NAME}"))
        #back up file#

        conn.execute(text(f"""
            DELETE FROM {TABLE_NAME}
            WHERE page_path IS NULL
            OR hit_timestamp IS NULL
            OR client_id IS NULL"""))
            #delete empty rows#

#         conn.execute(text(f"""
#                     DELETE FROM {TABLE_NAME}
#                     WHERE (client_id, session_id, hit_timestamp, page_path) IN (
#         SELECT client_id, session_id, hit_timestamp, page_path
#         FROM (
#             SELECT client_id, session_id, hit_timestamp, page_path,
#             ROW_NUMBER() OVER (PARTITION BY client_id, session_id, hit_timestamp, page_path ORDER BY client_id) as rn
#             FROM {TABLE_NAME}
#         ) t WHERE rn > 1
#     )
# """))
            #delete duplicated rows#

        pages_str = ','.join([f"'{p}'" for p in PAGES])
        conn.execute(text(f"""
                    DELETE FROM {TABLE_NAME}
                    WHERE page_path NOT IN ({pages_str})
                    AND page_path IS NOT NULL"""))

        conn.execute(text(f"""
                    DELETE FROM {TABLE_NAME}
                    WHERE previous_page_path NOT IN ({pages_str})
                    AND previous_page_path IS NOT NULL"""))
        #delete rows with invalid page_path#

        conn.commit()


if __name__ == '__main__':
    clean_data()