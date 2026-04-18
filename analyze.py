import pandas as pd
import json
import os

def analyze_data():
    # 1. Load data
    df = pd.read_csv('data/superstore.csv', encoding='latin1')
    
    # 2. Cleaning
    # Convert dates to datetime objects
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date'] = pd.to_datetime(df['Ship Date'])
    
    # Check for nulls (optional, but good practice)
    # df.isnull().sum()
    
    # 3. Aggregations for Insights
    
    # Total Sales and Profit
    total_sales = float(df['Sales'].sum())
    total_profit = float(df['Profit'].sum())
    total_orders = int(df['Order ID'].nunique())
    
    # Products best sellers (by sales)
    top_products = df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10).reset_index()
    top_products_data = top_products.to_dict(orient='records')
    
    # Regions best revenue
    region_sales = df.groupby('Region')['Sales'].sum().sort_values(ascending=False).reset_index()
    region_sales_data = region_sales.to_dict(orient='records')
    
    # Seasonality (Sales per month)
    df['MonthYear'] = df['Order Date'].dt.to_period('M').astype(str)
    seasonality = df.groupby('MonthYear')['Sales'].sum().sort_index().reset_index()
    seasonality_data = seasonality.to_dict(orient='records')
    
    # Top Customers
    top_customers = df.groupby('Customer Name')['Sales'].sum().sort_values(ascending=False).head(10).reset_index()
    top_customers_data = top_customers.to_dict(orient='records')
    
    # Category composition
    category_sales = df.groupby('Category')['Sales'].sum().reset_index()
    category_data = category_sales.to_dict(orient='records')

    # Sub-category Analysis (to find underperforming ones)
    subcat_profit = df.groupby('Sub-Category')['Profit'].sum().sort_values().reset_index()
    subcat_profit_data = subcat_profit.to_dict(orient='records')

    # 4. Save results to JSON
    summary = {
        "kpis": {
            "total_sales": total_sales,
            "total_profit": total_profit,
            "total_orders": total_orders,
            "avg_ticket": total_sales / total_orders if total_orders > 0 else 0
        },
        "top_products": top_products_data,
        "region_sales": region_sales_data,
        "seasonality": seasonality_data,
        "top_customers": top_customers_data,
        "category_sales": category_data,
        "subcat_profit": subcat_profit_data
    }
    
    with open('data/summary.json', 'w') as f:
        json.dump(summary, f, indent=4)
        
    print("Analysis complete. Results saved to data/summary.json")

if __name__ == "__main__":
    analyze_data()
