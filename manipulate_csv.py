"""
CSV: patient_records.csv (create this file to practice)

patient_id,name,dob,last_visit,condition,medication,dosage
P001,  John Doe  ,1980-05-15,2024-01-15,Diabetes,Metformin,500mg
P002,Jane Smith,15/05/1975,2024-01-20,Hypertension,Lisinopril,10mg
P003,Bob Johnson,1990-08-22,invalid_date,Diabetes,,500mg
P001,John Doe,1980-05-15,2024-01-15,Diabetes,Metformin,500mg
P004,Alice,1985-03-10,2024-01-25,,Aspirin,81mg
,Mike Davis,1978-11-30,2024-01-30,Hypertension,Amlodipine,5mg

COMPLETE THIS IN 45 MINUTES:
    # 2. Remove whitespace from all string columns

    # 3. Remove duplicate rows

    # 4. Parse dates (handle multiple formats: YYYY-MM-DD and DD/MM/YYYY)

    # 5. Remove rows with invalid dates

    # 6. Remove rows missing patient_id or name

    # 7. Fill missing conditions with "Unknown"

    # 8. Calculate patient age from DOB

    # 9. Group by condition and count patients

    # 10. Export cleaned data
"""
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def clean_patient_data(csv_path):
    try:
        # 1. Load CSV
        # df = pd.read_csv(csv_path, parse_dates=["dob","last_visit"])
        df = pd.read_csv(csv_path)
        df.drop_duplicates(subset="patient_id", keep="first", inplace=True)
        df['dob'] = df['dob'].apply(parse_flexible_date)
        df['last_visit'] = df['last_visit'].apply(parse_flexible_date)
        df.dropna(subset=['dob', 'last_visit', 'patient_id','name'], inplace=True)
        df.fillna({"condition": "Unknown"}, inplace=True)
        df['name'] = df['name'].str.strip()
        today = datetime.now()
        df['age']  =  (today - df['dob']).dt.days // 365

        df = df[(df['age'] >= 13) & (df['age'] <= 120)]

        # Aggregation
        condition_summary = df.groupby('condition').size().reset_index(name='patient_count')
        print("\nCondition Summary:")
        print(condition_summary)

        df.to_csv("test_files/patient_output.csv", index=False)
        return df, condition_summary
    except FileNotFoundError:
        print("File not found!")
    except pd.errors.EmptyDataError:
        print("CSV file is empty!")
    except pd.errors.ParserError:
        print("Error parsing CSV file!")
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()  # This helps debug!

def parse_flexible_date(date):
    """Parse single date with multiple format attempts"""
    if pd.isna(date):
        return None
    for fmt in  ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y']:
        try :
            return pd.to_datetime(date, format=fmt)
        except (ValueError, TypeError):
            continue
    return None

clean_patient_data('test_files/patient_records.csv')