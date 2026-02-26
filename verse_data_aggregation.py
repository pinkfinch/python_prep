"""
Generate business intelligence report from orders data.

CSV: orders.csv
order_id,customer_id,product_id,quantity,price,category,order_date,region
O001,C001,P100,2,29.99,Electronics,2024-01-15,East
O002,C002,P101,1,15.50,Home,2024-01-15,West
O003,C001,P102,1,199.99,Electronics,2024-01-16,East
O004,C003,P100,3,29.99,Electronics,2024-01-16,North

Tasks:
Create a comprehensive report with:
1. Total revenue by category and region
2. Top 5 customers by total spend
3. Average order value by region
4. Month-over-month growth rate
5. Products with declining sales (compare first vs second half of month)
6. Customer retention (customers who ordered multiple times)
"""
import pandas as pd
import logging

logger = logging.getLogger("ecommerce_report")
logging.basicConfig(
    level=logging.INFO
    # format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def generate_ecommerce_report(csv_path):
    """
    Returns dict with all metrics
    """

    df = pd.read_csv(csv_path, parse_dates=['order_date'])
    # Calculate revenue for each order
    df['revenue'] = df['quantity'] * df['price']

    # Group by category and region, sum the revenue
    revenue_by_cat_region = df.groupby(['category', 'region'])['revenue'].sum().reset_index()
    spend_by_customer = df.groupby(['customer_id'])['revenue'].sum().nlargest(5).reset_index()
    average_order_value_by_region = df.groupby('region')['revenue'].mean()
    month_over_month_growth = df['order_date'].dt.month
    customer_orders = df.groupby('customer_id')['order_id'].count().reset_index()
    customer_orders.columns = ['customer_id', 'order_count']
    repeat_customers = customer_orders[customer_orders['order_count'] > 1]

    logger.info(f"Revenue by category and region: {revenue_by_cat_region} ")
    logger.info(f"Spend by customer: {spend_by_customer} ")
    logger.info(f"Average order value by region: {average_order_value_by_region} ")
    logger.info(f"Month over month growth: {month_over_month_growth} ")
    logger.info(f"Repeat customers: {repeat_customers} ")


generate_ecommerce_report("test_files/orders.csv")
"""
Analyze patient visit patterns and generate summary statistics.

CSV: patient_visits.csv
visit_id,patient_id,visit_date,doctor_id,diagnosis_code,duration_min,cost
V001,P001,2024-01-15,D001,E11,30,150.00
V002,P002,2024-01-15,D002,I10,45,200.00
V003,P001,2024-02-10,D001,E11,30,150.00
V004,P003,2024-02-15,D001,Z00,60,100.00
V005,P002,2024-03-01,D002,I10,40,200.00

Tasks:
1. Calculate readmission rate (same patient, same diagnosis within 30 days)
2. Average visits per patient
3. Most common diagnoses by month
4. Doctor utilization (number of patients, total duration)
5. Revenue by diagnosis code
6. Identify patients with multiple chronic conditions
"""

def analyze_patient_visits(csv_path):
    df = pd.read_csv(csv_path, parse_dates=['visit_date'])
    readmission = df.groupby(['patient_id', 'diagnosis_code'])['visit_id'].count()
    readmission.columns = ['patient_id', 'visit_count']
    readmission_rate = readmission[readmission['visit_count'] > 1]
    logger.info(f"patient readmission rate: {readmission_rate}")

    visits_per_patient = df.groupby(['patient_id'])['visit_id'].mean()
    logger.info(f"visits per patient {visits_per_patient}")

    diagnosis_by_month = df.groupby(['diagnosis_code'])['visit_date'].dt.month
    logger.info(f"Diagnosis by month {diagnosis_by_month}")

    doctor_utilization_patient = df.groupby(['doctor_id'])['patient_id'].count()
    doctor_utilization_duration = df.groupby()



