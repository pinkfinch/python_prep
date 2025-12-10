# MEMORIZE THESE:

# Reading
df = pd.read_csv('file.csv', dtype={'col': 'string'}, parse_dates=['date_col'])

# Cleaning
df = df.drop_duplicates()
df = df.dropna(subset=['required_col'])
df['col'] = df['col'].str.strip()

# Dates
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d', errors='coerce')

# Filtering
df = df[df['age'] > 18]
df = df[df['status'].isin(['active', 'pending'])]

# Grouping
summary = df.groupby('category').agg({'amount': ['sum', 'mean', 'count']})

# Sorting
df = df.sort_values('date', ascending=False)
top_n = df.nlargest(10, 'revenue')

# Export
df.to_csv('output.csv', index=False)


