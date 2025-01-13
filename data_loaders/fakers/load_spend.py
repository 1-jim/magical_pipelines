import io
import numpy as np
import pandas as pd
from faker import Faker
from faker.providers import BaseProvider
import random
from datetime import datetime, timedelta
from pandas import DataFrame

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@data_loader
def load_data_from_faker(*args, **kwargs):
    np.random.seed(42)

    # Parameters
    num_suppliers = int(kwargs['suppliers'])
    num_skus = int(kwargs['skus'])
    months = int(kwargs['months'])

    # set up fakes
    fake = Faker(['en-GB'])
    Faker.seed(1977)

    class MyFakes(BaseProvider):
        def suppliers(self) -> str:
            COMPANY_OPTIONS=[]
            for _ in range(num_suppliers):
                COMPANY_OPTIONS.append(fake.company().upper() + ' ' + fake.company_suffix().upper())
            return self.random_elements(COMPANY_OPTIONS, length=1)[0]
        
        def products(self) -> str:
            COLOUR_OPTIONS=['RED','BLUE','GREEN']
            PRODUCT_OPTIONS=[]
            for _ in range(num_skus):
                PRODUCT_OPTIONS.append(np.random.choice(COLOUR_OPTIONS) + ' ' + fake.word().upper())
            return self.random_elements(PRODUCT_OPTIONS, length=1)[0]

    fake.add_provider(MyFakes)

    # Generate supplier, SKU, category, and monthly spend data
    suppliers = [fake.suppliers() for i in range(1, num_suppliers + 1)]
    categories = ["Electronics", "Clothing", "Household", "Toys", "Sports"]
    skus = [fake.products() for i in range(1, num_skus + 1)]

    data = []

    # Simulate SKU data over a 6-month period
    for month in range(1, months + 1):
        for sku in skus:
            supplier = np.random.choice(suppliers)
            category = np.random.choice(categories)
            historical_spend = np.random.uniform(1000, 10000)
            demand_forecast = historical_spend * np.random.uniform(0.85, 1.15) # Random Threshold
            actual_sales = demand_forecast * np.random.uniform(0.85, 1.15)  # Simulating actual sales
            marketing_influence = np.random.choice([True, False], p=[0.2, 0.8])  # 20% chance of being in a campaign
            baseline_revenue = historical_spend * np.random.uniform(1.05, 1.2)
            post_marketing_revenue = baseline_revenue * np.random.uniform(0.7, 0.95) if marketing_influence else baseline_revenue
            optimized_price = demand_forecast * np.random.uniform(1.05, 1.15) # Optimisation can flex
            profit_margin_baseline = baseline_revenue - historical_spend
            profit_margin_optimized = optimized_price - historical_spend
            
            # Append data for each SKU/month
            data.append({
                "Month": month,
                "Supplier": supplier,
                "SKU": sku,
                "Category": category,
                "Historical_Spend": round(historical_spend, 2),
                "Demand_Forecast": round(demand_forecast, 2),
                "Actual_Sales": round(actual_sales, 2),
                "Marketing_Influence": marketing_influence,
                "Baseline_Revenue": round(baseline_revenue, 2),
                "Post_Marketing_Revenue": round(post_marketing_revenue, 2),
                "Optimized_Price": round(optimized_price, 2),
                "Profit_Margin_Baseline": round(profit_margin_baseline, 2),
                "Profit_Margin_Optimized": round(profit_margin_optimized, 2)
            })

    return pd.DataFrame(data)