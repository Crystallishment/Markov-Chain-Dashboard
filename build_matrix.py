import pandas as pd
import pandas as pd
from sqlalchemy import create_engine
from config import DB_URL, TABLE_NAME


def build_matrix():
    engine = create_engine(DB_URL)

    df = pd.read_sql(f"""
        SELECT client_id, session_id, hit_timestamp, page_path, previous_page_path
        FROM {TABLE_NAME}
        ORDER BY client_id, session_id, hit_timestamp
    """, engine)

    transition_counts = {}

    for _, row in df.iterrows():
        from_state = row["previous_page_path"]
        to_state = row["page_path"]

        if pd.isna(from_state) or pd.isna(to_state):
            continue

        if from_state not in transition_counts:
            transition_counts[from_state] = {}

        transition_counts[from_state][to_state] = (
            transition_counts[from_state].get(to_state, 0) + 1
        )

    # 关键：state_list 必须包含 from_state 和 to_state
    states = set()

    for from_state, transitions in transition_counts.items():
        states.add(from_state)

        for to_state in transitions:
            states.add(to_state)

    state_list = sorted(list(states))

    probability_dict = {}

    for from_state, transitions in transition_counts.items():
        total = sum(transitions.values())

        if total == 0:
            continue

        probability_dict[from_state] = {
            to_state: count / total
            for to_state, count in transitions.items()
        }

    return state_list, probability_dict



if __name__ == '__main__':
    state_list, probability_dict = build_matrix()
    print(state_list)
    print(probability_dict)