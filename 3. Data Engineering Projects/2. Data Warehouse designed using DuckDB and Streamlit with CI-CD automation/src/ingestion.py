import os
import random
from datetime import datetime, timedelta
import pandas as pd
import duckdb

def generate_mock_data():
    print("Generating mock e-commerce data...")
    random.seed(42)  # For reproducible results
    
    # 1. Customers
    countries = ["USA", "Canada", "UK", "Germany", "France", "Japan", "Australia"]
    first_names = ["John", "Jane", "Alice", "Bob", "Charlie", "David", "Emma", "Frank", "Grace", "Henry"]
    last_names = ["Smith", "Doe", "Johnson", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor", "Anderson"]
    
    customers = []
    start_date = datetime(2025, 1, 1)
    for i in range(1, 101):
        cust_id = f"CUST_{i:03d}"
        first = random.choice(first_names)
        last = random.choice(last_names)
        email = f"{first.lower()}.{last.lower()}@example.com"
        created_at = start_date + timedelta(days=random.randint(0, 365))
        country = random.choice(countries)
        customers.append({
            "customer_id": cust_id,
            "first_name": first,
            "last_name": last,
            "email": email,
            "created_at": created_at,
            "country": country
        })
    df_customers = pd.DataFrame(customers)
    
    # 2. Orders
    statuses = ["completed", "completed", "completed", "pending", "returned", "cancelled"]
    payment_methods = ["credit_card", "credit_card", "paypal", "bank_transfer"]
    
    orders = []
    order_id_seq = 1
    for cust in customers:
        num_orders = random.randint(0, 5)
        for _ in range(num_orders):
            order_date = cust["created_at"] + timedelta(days=random.randint(1, 60))
            if order_date > datetime(2026, 6, 1):
                continue
            
            orders.append({
                "order_id": f"ORD_{order_id_seq:04d}",
                "customer_id": cust["customer_id"],
                "order_date": order_date,
                "status": random.choice(statuses),
                "amount": round(random.uniform(10.0, 500.0), 2),
                "payment_method": random.choice(payment_methods)
            })
            order_id_seq += 1
    df_orders = pd.DataFrame(orders)
    
    # 3. Web Traffic / Events
    event_types = ["page_view", "page_view", "add_to_cart", "checkout"]
    devices = ["desktop", "mobile", "tablet"]
    
    events = []
    event_id_seq = 1
    for cust in customers:
        num_events = random.randint(5, 20)
        curr_time = cust["created_at"]
        for _ in range(num_events):
            curr_time += timedelta(minutes=random.randint(5, 1440))
            if curr_time > datetime(2026, 6, 1):
                continue
            events.append({
                "event_id": f"EVT_{event_id_seq:05d}",
                "customer_id": cust["customer_id"],
                "event_type": random.choice(event_types),
                "event_timestamp": curr_time,
                "device": random.choice(devices)
            })
            event_id_seq += 1
    df_events = pd.DataFrame(events)
    
    print(f"Generated {len(df_customers)} customers, {len(df_orders)} orders, and {len(df_events)} web events.")
    return df_customers, df_orders, df_events

def main():
    # Make sure target directories exist
    os.makedirs("data", exist_ok=True)
    
    db_path = "data/dev.duckdb"
    print(f"Connecting to DuckDB database at {db_path}...")
    conn = duckdb.connect(db_path)
    
    # Generate data
    df_customers, df_orders, df_events = generate_mock_data()
    
    # Create raw schema and register raw tables
    print("Writing raw tables to DuckDB...")
    conn.execute("CREATE SCHEMA IF NOT EXISTS raw;")
    
    # Write tables to raw schema
    conn.register("df_customers_temp", df_customers)
    conn.execute("CREATE OR REPLACE TABLE raw.raw_customers AS SELECT * FROM df_customers_temp;")
    conn.unregister("df_customers_temp")
    
    conn.register("df_orders_temp", df_orders)
    conn.execute("CREATE OR REPLACE TABLE raw.raw_orders AS SELECT * FROM df_orders_temp;")
    conn.unregister("df_orders_temp")
    
    conn.register("df_events_temp", df_events)
    conn.execute("CREATE OR REPLACE TABLE raw.raw_events AS SELECT * FROM df_events_temp;")
    conn.unregister("df_events_temp")
    
    # Close connection
    conn.close()
    print("Ingestion complete. Raw tables populated successfully!")

if __name__ == "__main__":
    main()
