import pandas as pd
from datetime import datetime, timedelta
import openpyxl


def generate_day_sale_data(sale_id, date):
    pass


# Load data from Excel workbook
workbook = pd.read_excel('demo_sale_generator_constrains.xlsx', dtype=str, sheet_name=None)

# Extract each sheet as a separate DataFrame
menu_data = workbook['menu'].copy()

weekday_sale_distribution_data = workbook['weekday_sale_distribution'].copy()

sale_per_time_of_day_data = workbook['sale_per_time_of_day'].copy()

item_sale_probability_data = workbook['item_sale_probability'].copy()

product_quantity_probability_data = workbook['Product_quantity_probability'].copy()

# Create empty DataFrame for sales data
sales_data = pd.DataFrame(columns=['Unique Id', 'Date', 'Time', 'Item', 'Item_quantity', 'Price'])

# Set parameters
unique_id = 37589
start_date = '2019-01-01'
end_date = '2021-12-31'

date = datetime.strptime(start_date, '%Y-%m-%d')

g_date = date.strftime('%Y-%m-%d')

while g_date != end_date or unique_id != 37610:
    day_data, unique_id = generate_day_sale_data(unique_id, date)
    sales_data = sales_data.append(day_data, ignore_index=True)
    date += timedelta(days=1)
    g_date = date.strftime('%Y-%m-%d')