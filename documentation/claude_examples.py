import pandas as pd

# Read sales data with proper types and date parsing
df = pd.read_csv('sales.csv',
                 dtype={
                     'order_id': 'string',
                     'customer_id': 'int64',
                     'product': 'string',
                     'quantity': 'int32',
                     'price': 'float64'
                 },
                 parse_dates=['order_date'])

# Basic exploration
print(f"Shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(df.head())
print(df.info())

# Handle missing values
print(f"Missing values:\n{df.isnull().sum()}")

# Drop rows with any missing values
df_clean = df.dropna()

# USER DATA with complex cleaning
import pandas as pd
import re

# Read user data
df = pd.read_csv('users.csv',
                 na_values=['', 'NA', 'N/A', 'null'],
                 dtype={
                     'user_id': 'string',
                     'username': 'string',
                     'email': 'string',
                     'age': 'Int64',  # Nullable integer
                     'signup_date': 'string',
                     'country': 'string'
                 })

print(f"Original shape: {df.shape}")

# Remove duplicate users (keep first occurrence)
df = df.drop_duplicates(subset=['user_id'], keep='first')
print(f"After deduplication: {df.shape}")

# Clean email addresses
def clean_email(email):
    if pd.isna(email):
        return None
    email = email.strip().lower()
    # Basic email validation
    if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        return email
    return None

df['email'] = df['email'].apply(clean_email)

# Remove rows with invalid emails
df = df[df['email'].notna()]

# Clean and validate age
df = df[(df['age'] >= 13) & (df['age'] <= 120)]

# Parse dates with multiple formats
def parse_flexible_date(date_str):
    if pd.isna(date_str):
        return None
    for fmt in ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y']:
        try:
            return pd.to_datetime(date_str, format=fmt)
        except ValueError:
            continue
    return None

df['signup_date'] = df['signup_date'].apply(parse_flexible_date)

# Remove rows with unparseable dates
df = df[df['signup_date'].notna()]

# Standardize country names
country_mapping = {
    'USA': 'United States',
    'US': 'United States',
    'U.S.A.': 'United States',
    'UK': 'United Kingdom',
    'U.K.': 'United Kingdom'
}
df['country'] = df['country'].str.strip().replace(country_mapping)

# Create age groups
df['age_group'] = pd.cut(df['age'],
                         bins=[0, 18, 30, 50, 100],
                         labels=['Under 18', '18-30', '31-50', '50+'])

# Summary statistics
print("\nAge distribution:")
print(df['age'].describe())

print("\nUsers by country:")
print(df['country'].value_counts())

print("\nUsers by age group:")
print(df['age_group'].value_counts())

# Export cleaned data
df.to_csv('users_cleaned.csv', index=False)

# Export summary report
summary = {
    'total_users': len(df),
    'countries': df['country'].nunique(),
    'avg_age': df['age'].mean(),
    'median_age': df['age'].median()
}
print(f"\nSummary: {summary}")

# Or fill missing numeric values with mean

# Data transformation
df['total_amount'] = df['quantity'] * df['price']
df['order_year'] = df['order_date'].dt.year
df['order_month'] = df['order_date'].dt.month

# Aggregation
monthly_sales = df.groupby(['order_year', 'order_month']).agg({
    'total_amount': 'sum',
    'order_id': 'count'
}).rename(columns={'order_id': 'order_count'})

print(monthly_sales)

# Export cleaned data
df_clean.to_csv('sales_cleaned.csv', index=False)

#LARGE DATA CHUNKING
import pandas as pd

# For very large files, read in chunks
chunk_size = 10000
chunks = []

for chunk in pd.read_csv('large_file.csv', chunksize=chunk_size):
    # Process each chunk
    chunk_filtered = chunk[chunk['value'] > 100]
    chunks.append(chunk_filtered)

# Combine all chunks
df = pd.concat(chunks, ignore_index=True)

# Alternative: Process chunks without storing all in memory
total_sum = 0
row_count = 0

for chunk in pd.read_csv('large_file.csv', chunksize=chunk_size):
    total_sum += chunk['value'].sum()
    row_count += len(chunk)

average = total_sum / row_count
print(f"Average: {average}")

#COMMON DATA CLEANING
import pandas as pd

df = pd.read_csv('data.csv')

# Remove whitespace from all string columns
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# Convert column names to lowercase and replace spaces
df.columns = df.columns.str.lower().str.replace(' ', '_')

# Remove rows with all NaN values
df = df.dropna(how='all')

# Remove columns with all NaN values
df = df.dropna(axis=1, how='all')

# Remove duplicate rows
df = df.drop_duplicates()

# Reset index after cleaning
df = df.reset_index(drop=True)

# Filter rows based on conditions
df = df[(df['age'] > 0) & (df['salary'] < 1000000)]

# Sort data
df = df.sort_values(['date', 'name'], ascending=[False, True])

#ERROR HANDLING
import pandas as pd

try:
    df = pd.read_csv('data.csv')
except FileNotFoundError:
    print("File not found!")
except pd.errors.EmptyDataError:
    print("CSV file is empty!")
except pd.errors.ParserError:
    print("Error parsing CSV file!")
except Exception as e:
    print(f"Unexpected error: {e}")

# Read with error handling for bad lines
df = pd.read_csv('data.csv', on_bad_lines='skip')  # Skip problematic rows
# or
df = pd.read_csv('data.csv', on_bad_lines='warn')  # Warn but skip


# Interview reference:
# Basic conversion
df['date'] = pd.to_datetime(df['date'])

# With format for speed
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

# Handle errors gracefully (MOST COMMON IN INTERVIEWS)
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df = df[df['date'].notna()]  # Remove invalid dates

# Multiple formats
def parse_date(date_str):
    for fmt in ['%Y-%m-%d', '%m/%d/%Y']:
        try:
            return pd.to_datetime(date_str, format=fmt)
        except:
            continue
    return None

df['date'] = df['date'].apply(parse_date)

# Extract date parts
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day_name'] = df['date'].dt.day_name()