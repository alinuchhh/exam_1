

import pandas as pd
from datetime import datetime

def parse_log_line(line):
    timestamp_str, status = line.strip().split('] ')
    timestamp_str = timestamp_str[1:]  # Убираем открывающую квадратную скобку
    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
    return timestamp, status

def load_log_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    timestamps, statuses = zip(*[parse_log_line(line) for line in lines])
    return pd.DataFrame({'timestamp': timestamps, 'status': statuses})

def count_statuses_per_minute(df):
    df['minute'] = df['timestamp'].dt.floor('T')
    counts = df.groupby(['minute', 'status']).size().unstack(fill_value=0)
    return counts

def main(file_path):
    df = load_log_file(file_path)
    counts = count_statuses_per_minute(df)
    print(counts)

if __name__ == "__main__":
    file_path = 'events.txt'
    main(file_path)