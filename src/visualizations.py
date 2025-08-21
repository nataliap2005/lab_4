import matplotlib.pyplot as plt
import seaborn as sns

def plot_sales_by_category(df_cat):
    plt.figure(figsize=(8,5))
    sns.barplot(x='total_sales', y='category', data=df_cat, palette="viridis")
    plt.title("Ventas por categoría")
    plt.xlabel("Total de ventas")
    plt.ylabel("Categoría")
    plt.tight_layout()
    plt.show()

def plot_revenue_by_channel_time(df_rev):
    plt.figure(figsize=(10,6))
    sns.lineplot(x='month', y='revenue', hue='channel', data=df_rev, marker='o')
    plt.title("Ingresos por canal y mes")
    plt.xlabel("Mes")
    plt.ylabel("Ingreso")
    plt.legend(title="Canal")
    plt.tight_layout()
    plt.show()

def plot_margin_by_product(df_margin):
    plt.figure(figsize=(8,6))
    sns.barplot(x='margin_pct', y='name', data=df_margin, palette="magma")
    plt.title("Margen de ganancia por producto (%)")
    plt.xlabel("Margen (%)")
    plt.ylabel("Producto")
    plt.tight_layout()
    plt.show()

def plot_sales_by_location(df_loc):
    plt.figure(figsize=(10,6))
    sns.barplot(x='total_sales', y='city', hue='country', data=df_loc, dodge=True)
    plt.title("Ventas por ciudad y país")
    plt.xlabel("Total de ventas")
    plt.ylabel("Ciudad")
    plt.legend(title="País")
    plt.tight_layout()
    plt.show()