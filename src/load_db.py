# src/load_db.py
import os
import pandas as pd
from datetime import timedelta
from connection import get_conn_db

# Ruta relativa robusta (funciona al subir a GitHub)
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

def insert_df(conn, df, table, cols):
    placeholders = ",".join(["%s"] * len(cols))
    sql = f"INSERT INTO {table} ({','.join(cols)}) VALUES ({placeholders})"
    cur = conn.cursor()
    cur.executemany(sql, df[cols].astype(object).values.tolist())
    conn.commit()

def build_dates(min_d, max_d):
    """Genera dimensión de fechas día a día entre min_d y max_d (ambas incluidas)."""
    days = []
    d = min_d
    while d <= max_d:
        date_id = d.year*10000 + d.month*100 + d.day
        days.append({
            "date_id": date_id,
            "full_date": d,                      # datetime.date
            "day": d.day,
            "month": d.month,
            "month_name": d.strftime("%B"),
            "quarter": (d.month-1)//3 + 1,
            "year": d.year,
            "day_of_week": d.isoweekday(),      # 1..7 (Mon..Sun)
            "week_of_year": int(d.strftime("%V"))
        })
        d += timedelta(days=1)
    return pd.DataFrame(days)

def load_all():
    # 1) Leer CSVs
    products  = pd.read_csv(os.path.join(DATA_DIR, "products.csv"))
    customers = pd.read_csv(os.path.join(DATA_DIR, "customers.csv"))
    channels  = pd.read_csv(os.path.join(DATA_DIR, "channels.csv"))
    sales     = pd.read_csv(os.path.join(DATA_DIR, "sales.csv"), parse_dates=["sale_date"])

    # 2) Rango de fechas y Dates
    min_d, max_d = sales["sale_date"].min().date(), sales["sale_date"].max().date()
    dates = build_dates(min_d, max_d)

    # 3) Convertir a tipos compatibles con MySQL
    #    Para Series de pandas se usa .dt.date, no .date
    sales["sale_date"] = pd.to_datetime(sales["sale_date"]).dt.date
    # dates["full_date"] ya es datetime.date por build_dates,
    # pero si quieres forzar conversión segura, descomenta la línea siguiente:
    # dates["full_date"] = pd.to_datetime(dates["full_date"]).dt.date

    # 4) Asignar date_id en Sales
    sales["date_id"] = sales["sale_date"].apply(lambda d: d.year*10000 + d.month*100 + d.day)

    # 5) Insertar en orden: dimensiones → hechos
    with get_conn_db() as conn:
        insert_df(conn, products,  "Products",  ["product_id","name","category","brand","unit_price","unit_cost"])
        insert_df(conn, customers, "Customers", ["customer_id","name","city","country","age"])
        insert_df(conn, channels,  "Channels",  ["channel_id","channel"])
        insert_df(conn, dates,     "Dates",     ["date_id","full_date","day","month","month_name","quarter","year","day_of_week","week_of_year"])
        insert_df(conn, sales,     "Sales",     ["sale_id","product_id","customer_id","channel_id","date_id","sale_date","quantity","unit_price_sale"])
    print("✔ Datos cargados en la BD.")
