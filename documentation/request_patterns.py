# MEMORIZE THIS:

import requests
from time import sleep

def fetch_with_retry(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response.json()
        except requests.Timeout:
            if attempt == max_retries - 1:
                return None
            sleep(1)
    return None



# 1. Basic GET request
response = requests.get(url, params=params, timeout=5)

# 2. Check status
if response.status_code == 200:
    data = response.json()

# 3. Error handling with retries
max_retries = 3
for attempt in range(max_retries):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            break
    except requests.Timeout:
        if attempt == max_retries - 1:
            # Handle final failure
            pass
        sleep(1)

# 4. Safe JSON navigation
value = data.get('key', {}).get('nested_key', 'default')

# 5. Extract from JSON arrays
items = [item['field'] for item in data.get('results', []) if 'field' in item]


# EDGE CASES
# ALWAYS CHECK:
# - Empty DataFrames: if len(df) == 0
# - Missing values: df['col'].notna()
# - Invalid types: pd.to_numeric(df['col'], errors='coerce')
# - Empty strings: df['col'].str.strip() != ''
# - Duplicates: df.drop_duplicates()