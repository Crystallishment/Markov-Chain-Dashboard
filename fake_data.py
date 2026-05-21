import pandas as pd
import random
from datetime import datetime, timedelta
import os

transition_rules = {
    "/home": ["/search", "/product", "/exit"],
    "/search": ["/product", "/home", "/exit"],
    "/product": ["/cart", "/search", "/home", "/exit"],
    "/cart": ["/checkout", "/product", "/exit"],
    "/checkout": ["/exit"],
    "/exit": []
}

rows = []

for user_id in range(1, 1001):
    session_id = f"s{user_id:04d}"
    client_id = f"u{user_id:04d}"
    timestamp = datetime(2024, 1, 1, 10, 0, 0) + timedelta(minutes=random.randint(0, 1440))

    current_page = "/home"
    prev_page = None
    max_steps = random.randint(3, 10)

    for _ in range(max_steps):
        rows.append({
            "client_id": client_id,
            "session_id": session_id,
            "hit_timestamp": timestamp,
            "page_path": current_page,
            "previous_page_path": prev_page
        })

        if current_page == "/exit":
            break

        possible_next_pages = transition_rules[current_page]
        next_page = random.choice(possible_next_pages)

        prev_page = current_page
        current_page = next_page
        timestamp += timedelta(seconds=random.randint(5, 60))

    if rows[-1]["session_id"] == session_id and rows[-1]["page_path"] != "/exit":
        rows.append({
            "client_id": client_id,
            "session_id": session_id,
            "hit_timestamp": timestamp + timedelta(seconds=random.randint(5, 60)),
            "page_path": "/exit",
            "previous_page_path": rows[-1]["page_path"]
        })

df = pd.DataFrame(rows)

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
output_path = os.path.join(desktop_path, "clickstream.csv")

df.to_csv(output_path, index=False)

print(df.head(10))
print(f"CSV file saved to: {output_path}")