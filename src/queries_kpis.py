# queries.py
import pandas as pd
from connection import get_conn_db

MYSQL_DB = "retail_dw"

# Queries
def sales_by_category():
    conn = get_conn_db(MYSQL_DB)
    query = """
    SELECT p.category,
           SUM(s.line_total) AS total_sales,
           SUM(s.quantity)   AS units
    FROM Sales s
    JOIN Products p ON s.product_id = p.product_id
    GROUP BY p.category
    ORDER BY total_sales DESC;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def revenue_by_channel_time():
    conn = get_conn_db(MYSQL_DB)
    query = """
    SELECT c.channel,
           d.year, d.month,
           SUM(s.line_total) AS revenue
    FROM Sales s
    JOIN Channels c ON s.channel_id = c.channel_id
    JOIN Dates d  ON s.date_id = d.date_id
    GROUP BY c.channel, d.year, d.month
    ORDER BY d.year, d.month, c.channel;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def profit_margin_by_product():
    conn = get_conn_db(MYSQL_DB)
    query = """
    SELECT p.name,
           SUM(s.line_total - (s.quantity * p.unit_cost)) AS total_profit,
           ROUND(SUM(s.line_total - (s.quantity * p.unit_cost))/NULLIF(SUM(s.line_total),0)*100,2) AS margin_pct
    FROM Sales s
    JOIN Products p ON s.product_id = p.product_id
    GROUP BY p.name
    ORDER BY total_profit DESC;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def sales_by_location():
    conn = get_conn_db(MYSQL_DB)
    query = """
    SELECT c.country, c.city,
           SUM(s.line_total) AS total_sales
    FROM Sales s
    JOIN Customers c ON s.customer_id = c.customer_id
    GROUP BY c.country, c.city
    ORDER BY total_sales DESC;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# KPIs
def total_sales_by_category(df_cat):
    return df_cat['total_sales'].sum()

def avg_units_per_category(df_cat):
    return df_cat['units'].mean()

def avg_margin_by_product(df_margin):
    return df_margin['margin_pct'].mean()

def sales_by_country(df_loc):
    return df_loc.groupby('country')['total_sales'].sum()