from connection import get_conn, get_conn_db

DDL = """
DROP DATABASE IF EXISTS retail_dw;
CREATE DATABASE retail_dw;
"""

TABLES = [
"""
CREATE TABLE IF NOT EXISTS Products (
  product_id INT PRIMARY KEY,
  name       VARCHAR(200) NOT NULL,
  category   VARCHAR(100) NOT NULL,
  brand      VARCHAR(100) NOT NULL,
  unit_price DECIMAL(10,2) NOT NULL,
  unit_cost  DECIMAL(10,2) NOT NULL,
  INDEX idx_products_category (category),
  INDEX idx_products_brand (brand)
) ENGINE=InnoDB;
""",
"""
CREATE TABLE IF NOT EXISTS Customers (
  customer_id INT PRIMARY KEY,
  name        VARCHAR(150) NOT NULL,
  city        VARCHAR(120) NOT NULL,
  country     VARCHAR(120) NOT NULL,
  age         TINYINT      NOT NULL,
  INDEX idx_customers_city (city),
  INDEX idx_customers_country (country)
) ENGINE=InnoDB;
""",
"""
CREATE TABLE IF NOT EXISTS Channels (
  channel_id  TINYINT PRIMARY KEY,
  channel     VARCHAR(50) NOT NULL
) ENGINE=InnoDB;
""",
"""
CREATE TABLE IF NOT EXISTS Dates (
  date_id      INT PRIMARY KEY,
  full_date    DATE NOT NULL,
  day          TINYINT NOT NULL,
  month        TINYINT NOT NULL,
  month_name   VARCHAR(20) NOT NULL,
  quarter      TINYINT NOT NULL,
  year         SMALLINT NOT NULL,
  day_of_week  TINYINT NOT NULL,
  week_of_year TINYINT NOT NULL,
  UNIQUE KEY uniq_full_date (full_date)
) ENGINE=InnoDB;
""",
"""
CREATE TABLE IF NOT EXISTS Sales (
  sale_id         BIGINT PRIMARY KEY,
  product_id      INT NOT NULL,
  customer_id     INT NOT NULL,
  channel_id      TINYINT NOT NULL,
  date_id         INT NOT NULL,
  sale_date       DATE NOT NULL,
  quantity        INT NOT NULL CHECK (quantity > 0),
  unit_price_sale DECIMAL(10,2) NOT NULL,
  line_total      DECIMAL(12,2) GENERATED ALWAYS AS (quantity * unit_price_sale) STORED,

  INDEX idx_sales_date (date_id),
  INDEX idx_sales_product (product_id),
  INDEX idx_sales_customer (customer_id),
  INDEX idx_sales_channel (channel_id),

  CONSTRAINT fk_sales_products  FOREIGN KEY (product_id)  REFERENCES Products(product_id),
  CONSTRAINT fk_sales_customers FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
  CONSTRAINT fk_sales_channels  FOREIGN KEY (channel_id)  REFERENCES Channels(channel_id),
  CONSTRAINT fk_sales_dates     FOREIGN KEY (date_id)     REFERENCES Dates(date_id)
) ENGINE=InnoDB;
"""
]

def run():
    with get_conn() as conn:
        cur = conn.cursor()
        for statement in DDL.split(";"):
            if statement.strip():
                cur.execute(statement)
        conn.commit()
        print("✔ Base de datos eliminada y recreada (retail_dw)")

    with get_conn_db() as conn:
        cur = conn.cursor()
        for sql in TABLES:
            cur.execute(sql)
        conn.commit()
        print("✔ Tablas creadas.")
