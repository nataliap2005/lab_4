from create_db import run as create_schema
from load_db import load_all
import queries_kpis
import visualizations

def main():
    print("🚀 Creando base y tablas...")
    create_schema()
    print("✔ Esquema creado.")

    print("📥 Cargando datos desde CSV...")
    load_all()
    print("✔ Datos cargados.")

    df_cat = queries_kpis.sales_by_category()
    df_rev = queries_kpis.revenue_by_channel_time()
    df_margin = queries_kpis.profit_margin_by_product()
    df_loc = queries_kpis.sales_by_location()

    print("KPI - Total ventas:", queries_kpis.total_sales_by_category(df_cat))
    print("KPI - Promedio unidades por categoría:", queries_kpis.avg_units_per_category(df_cat))
    print("KPI - Margen promedio por producto (%):", queries_kpis.avg_margin_by_product(df_margin))
    print("KPI - Ventas por país:\n", queries_kpis.sales_by_country(df_loc))

    visualizations.plot_sales_by_category(df_cat)
    visualizations.plot_revenue_by_channel_time(df_rev)
    visualizations.plot_margin_by_product(df_margin)
    visualizations.plot_sales_by_location(df_loc)

if __name__ == "__main__":
    main()
