import pandas as pd
import random
from datetime import datetime, timedelta

pages = ['/home', '/search', '/product', '/cart', '/checkout', '/exit']

rows = []
for user_id in range(1, 1001):
    session_id = f's{user_id:04d}'
    timestamp = datetime(2024, 1, 1, 10, 0, 0) + timedelta(minutes=random.randint(0, 1440))
    prev_page = None
    for _ in range(random.randint(3, 10)):
        page = random.choice(pages)
        rows.append({
            'client_id': f'u{user_id:04d}',
            'session_id': session_id,
            'hit_timestamp': timestamp,
            'page_path': page,
            'previous_page_path': prev_page
        })
        timestamp += timedelta(seconds=random.randint(5, 60))
        prev_page = page
        if page == '/exit':
            break

df = pd.DataFrame(rows)
df.to_csv('/Users/lyudaili/Downloads/clickstream.csv', index=False)
print(df.head(10))

df.to_csv('/Users/lyudaili/Desktop/clickstream.csv', index=False)