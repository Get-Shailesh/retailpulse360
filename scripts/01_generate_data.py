"""
RetailPulse 360 — Data Generation Script
Generates realistic synthetic retail datasets for NovaMart
"""
import pandas as pd
import numpy as np
import os
import random
from datetime import datetime, timedelta

random.seed(42)
np.random.seed(42)

OUT = "/home/claude/retailpulse360/data"
os.makedirs(OUT, exist_ok=True)

# ─── STORES ───────────────────────────────────────────────────────────────────
regions = ["North", "South", "East", "West", "Central"]
store_types = ["Flagship", "Standard", "Express"]
cities = {
    "North":   ["Chicago", "Minneapolis", "Detroit", "Milwaukee", "Indianapolis"],
    "South":   ["Houston", "Atlanta", "Miami", "New Orleans", "Nashville"],
    "East":    ["New York", "Boston", "Philadelphia", "Baltimore", "Newark"],
    "West":    ["Los Angeles", "San Francisco", "Seattle", "Portland", "Denver"],
    "Central": ["Dallas", "Kansas City", "St. Louis", "Omaha", "Tulsa"],
}

stores = []
sid = 1
for region, city_list in cities.items():
    for i, city in enumerate(city_list):
        stores.append({
            "store_id": f"S{sid:03d}",
            "store_name": f"NovaMart {city}",
            "city": city,
            "region": region,
            "store_type": store_types[i % 3],
            "open_date": (datetime(2019, 1, 1) + timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d"),
            "sqft": random.choice([8000, 12000, 18000, 25000, 35000]),
            "num_employees": random.randint(20, 120),
            "manager": f"Manager_{sid:03d}",
            "monthly_rent": random.randint(15000, 80000),
        })
        sid += 1

stores_df = pd.DataFrame(stores)
stores_df.to_csv(f"{OUT}/stores.csv", index=False)
print(f"✓ Stores: {len(stores_df)} rows")

# ─── PRODUCTS ──────────────────────────────────────────────────────────────────
categories = {
    "Electronics":    ["Smartphone", "Laptop", "Tablet", "Headphones", "Smartwatch", "Camera"],
    "Clothing":       ["T-Shirt", "Jeans", "Jacket", "Dress", "Shoes", "Accessories"],
    "Groceries":      ["Beverages", "Snacks", "Dairy", "Produce", "Bakery", "Frozen"],
    "Home & Kitchen": ["Cookware", "Furniture", "Bedding", "Lighting", "Decor", "Storage"],
    "Sports":         ["Fitness Equipment", "Sportswear", "Outdoor Gear", "Supplements", "Footwear"],
}
brands = ["NovaBrand", "AlphaLine", "PrimePlus", "ValuePro", "EliteChoice", "SmartPick", "NatureCo", "TechEdge"]

products = []
pid = 1
for cat, subcats in categories.items():
    for subcat in subcats:
        for _ in range(random.randint(6, 10)):
            cost = round(random.uniform(5, 400), 2)
            margin = random.uniform(0.25, 0.65)
            price = round(cost / (1 - margin), 2)
            products.append({
                "product_id": f"P{pid:04d}",
                "product_name": f"{random.choice(brands)} {subcat} {random.randint(100, 999)}",
                "category": cat,
                "subcategory": subcat,
                "brand": random.choice(brands),
                "unit_cost": cost,
                "unit_price": price,
                "margin_pct": round(margin * 100, 1),
                "supplier": f"Supplier_{random.randint(1, 30):02d}",
                "reorder_level": random.randint(10, 50),
                "weight_kg": round(random.uniform(0.1, 20), 2),
            })
            pid += 1

products_df = pd.DataFrame(products)
products_df.to_csv(f"{OUT}/products.csv", index=False)
print(f"✓ Products: {len(products_df)} rows")

# ─── CUSTOMERS ────────────────────────────────────────────────────────────────
first_names = ["James","Mary","John","Patricia","Robert","Jennifer","Michael","Linda",
               "William","Barbara","David","Susan","Richard","Jessica","Joseph","Karen",
               "Thomas","Sarah","Emma","Liam","Olivia","Noah","Ava","Isabella","Sophia"]
last_names  = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis",
               "Rodriguez","Martinez","Hernandez","Lopez","Gonzalez","Wilson","Anderson",
               "Taylor","Thomas","Moore","Jackson","Martin","Lee","Perez","Thompson"]

customers = []
for i in range(1, 10001):
    reg_date = datetime(2021, 1, 1) + timedelta(days=random.randint(0, 900))
    age = random.randint(18, 75)
    segment = np.random.choice(["Gold","Silver","Bronze","New"], p=[0.15, 0.30, 0.35, 0.20])
    customers.append({
        "customer_id": f"C{i:05d}",
        "first_name": random.choice(first_names),
        "last_name": random.choice(last_names),
        "email": f"customer{i}@email.com",
        "age": age,
        "gender": random.choice(["M","F","Other"]),
        "city": random.choice([c for cs in cities.values() for c in cs]),
        "registration_date": reg_date.strftime("%Y-%m-%d"),
        "loyalty_tier": segment,
        "email_opt_in": random.choice([True, False]),
        "lifetime_orders": 0,  # filled later
    })

customers_df = pd.DataFrame(customers)
customers_df.to_csv(f"{OUT}/customers.csv", index=False)
print(f"✓ Customers: {len(customers_df)} rows")

# ─── TRANSACTIONS ─────────────────────────────────────────────────────────────
store_ids    = stores_df["store_id"].tolist()
product_ids  = products_df["product_id"].tolist()
customer_ids = customers_df["customer_id"].tolist()

# Build price lookup
price_lookup = dict(zip(products_df["product_id"], products_df["unit_price"]))
cost_lookup  = dict(zip(products_df["product_id"], products_df["unit_cost"]))

transactions = []
tid = 1
start_date = datetime(2022, 1, 1)
end_date   = datetime(2024, 12, 31)

# Seasonal multipliers per month
season = {1:0.85,2:0.80,3:0.95,4:1.0,5:1.05,6:1.1,
           7:1.0,8:0.95,9:1.05,10:1.15,11:1.35,12:1.5}

current = start_date
while current <= end_date:
    month_mult = season[current.month]
    daily_txns = int(np.random.normal(130 * month_mult, 20))
    daily_txns = max(50, daily_txns)

    for _ in range(daily_txns):
        store  = random.choice(store_ids)
        cust   = random.choice(customer_ids)
        prod   = random.choice(product_ids)
        qty    = random.randint(1, 5)
        price  = price_lookup[prod]
        cost   = cost_lookup[prod]
        discount = round(random.choice([0, 0, 0, 0.05, 0.10, 0.15, 0.20]) * price, 2)
        final_price = round(price - discount, 2)
        payment = random.choice(["Credit Card","Debit Card","Cash","Mobile Pay"])
        channel = random.choice(["In-Store","In-Store","In-Store","Online"])

        transactions.append({
            "transaction_id": f"T{tid:07d}",
            "date": current.strftime("%Y-%m-%d"),
            "store_id": store,
            "customer_id": cust,
            "product_id": prod,
            "quantity": qty,
            "unit_price": price,
            "discount_amount": discount,
            "final_unit_price": final_price,
            "total_revenue": round(final_price * qty, 2),
            "total_cost": round(cost * qty, 2),
            "gross_profit": round((final_price - cost) * qty, 2),
            "payment_method": payment,
            "channel": channel,
        })
        tid += 1

    current += timedelta(days=1)

trans_df = pd.DataFrame(transactions)
trans_df.to_csv(f"{OUT}/transactions.csv", index=False)
print(f"✓ Transactions: {len(trans_df):,} rows")

# ─── INVENTORY ────────────────────────────────────────────────────────────────
inventory = []
for sid_val in store_ids:
    sampled = random.sample(product_ids, k=int(len(product_ids)*0.6))
    for pid_val in sampled:
        rl = products_df[products_df.product_id==pid_val]["reorder_level"].values[0]
        qty_on_hand = random.randint(0, 200)
        inventory.append({
            "store_id": sid_val,
            "product_id": pid_val,
            "qty_on_hand": qty_on_hand,
            "reorder_level": rl,
            "last_restocked": (datetime(2024, 12, 1) - timedelta(days=random.randint(0,60))).strftime("%Y-%m-%d"),
            "status": "Low Stock" if qty_on_hand < rl else ("Out of Stock" if qty_on_hand == 0 else "In Stock"),
        })

inv_df = pd.DataFrame(inventory)
inv_df.to_csv(f"{OUT}/inventory.csv", index=False)
print(f"✓ Inventory: {len(inv_df):,} rows")

# ─── CUSTOMER REVIEWS ─────────────────────────────────────────────────────────
positive = [
    "Amazing product, exceeded my expectations!", "Great value for money, highly recommend.",
    "Fast shipping and excellent quality.", "Will definitely buy again, very satisfied.",
    "Perfect for my needs, love the quality.", "Outstanding service and product quality!",
    "Best purchase I've made this year.", "Incredibly impressed with this item.",
]
neutral = [
    "Decent product, does what it says.", "OK quality for the price.",
    "Nothing special but gets the job done.", "Average experience, could be better.",
    "Product works fine, delivery was slow.", "Met my basic expectations.",
]
negative = [
    "Very disappointed with the quality.", "Poor customer service, won't buy again.",
    "Product broke after one week of use.", "Terrible quality, complete waste of money.",
    "Arrived damaged, very frustrating experience.", "Not as described, very misleading.",
    "Worst purchase ever, do not recommend.", "Extremely unhappy with this product.",
]

reviews = []
sampled_trans = trans_df.sample(n=min(8000, len(trans_df)), random_state=42)
for _, row in sampled_trans.iterrows():
    sentiment = np.random.choice(["Positive","Neutral","Negative"], p=[0.60, 0.25, 0.15])
    if sentiment == "Positive":
        text = random.choice(positive)
        rating = random.randint(4, 5)
    elif sentiment == "Neutral":
        text = random.choice(neutral)
        rating = random.randint(3, 3)
    else:
        text = random.choice(negative)
        rating = random.randint(1, 2)

    reviews.append({
        "review_id": f"R{len(reviews)+1:05d}",
        "transaction_id": row["transaction_id"],
        "customer_id": row["customer_id"],
        "product_id": row["product_id"],
        "store_id": row["store_id"],
        "review_date": row["date"],
        "rating": rating,
        "sentiment": sentiment,
        "review_text": text,
    })

reviews_df = pd.DataFrame(reviews)
reviews_df.to_csv(f"{OUT}/reviews.csv", index=False)
print(f"✓ Reviews: {len(reviews_df):,} rows")

print("\n✅ All datasets generated successfully!")
print(f"   Total transaction revenue: ${trans_df['total_revenue'].sum():,.0f}")
print(f"   Date range: {trans_df['date'].min()} → {trans_df['date'].max()}")
