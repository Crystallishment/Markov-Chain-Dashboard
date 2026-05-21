from collections import Counter
import pandas as pd
from simulation import MarkovChain


def build_step_flow_from_csv(
    file_path,
    min_step=1,
    max_steps=5,
    start_page=None,
    exit_page=None
):
    df = pd.read_csv(file_path)
    df = df.sort_values(["client_id", "session_id", "hit_timestamp"])

    transition_counter = Counter()

    grouped = df.groupby(["client_id", "session_id"])

    for (_, _), group in grouped:
        path = group["page_path"].dropna().tolist()

        if not path:
            continue

        if start_page and path[0] != start_page:
            path = [start_page] + path

        if exit_page and path[-1] != exit_page:
            path = path + [exit_page]

        for i in range(len(path) - 1):
            step = i + 1

            if step < min_step or step > max_steps:
                continue

            source = f"step{step}:{path[i]}"
            target = f"step{step + 1}:{path[i + 1]}"

            transition_counter[(source, target)] += 1

    return [
        {
            "source": source,
            "target": target,
            "value": count
        }
        for (source, target), count in transition_counter.items()
    ]


def build_step_flow_from_simulation(
    state_list,
    probability_dict,
    num_sessions=1000,
    min_step=1,
    max_steps=5,
    start_page=None,
    exit_page=None
):
    transition_counter = Counter()

    for _ in range(num_sessions):
        mc = MarkovChain(
            state_list,
            probability_dict,
            initial_state=start_page,
            terminal_state=exit_page
        )

        path = [mc.current_state]

        for _ in range(max_steps):
            next_state = mc.transfer_state()

            if next_state is None:
                break

            path.append(next_state)
            mc.current_state = next_state

        for i in range(len(path) - 1):
            step = i + 1

            if step < min_step or step > max_steps:
                continue

            source = f"step{step}:{path[i]}"
            target = f"step{step + 1}:{path[i + 1]}"

            transition_counter[(source, target)] += 1

    return [
        {
            "source": source,
            "target": target,
            "value": count
        }
        for (source, target), count in transition_counter.items()
    ]