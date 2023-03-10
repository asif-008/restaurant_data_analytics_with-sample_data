import pandas as pd
from datetime import datetime, timedelta
import openpyxl
import random


# used in generate_day_sale_data
def get_daily_total(weekday_sale_distribution_dataframe, weekday_name):
    # Filter dataframe to get all rows for the given weekday
    weekday_data = weekday_sale_distribution_dataframe[weekday_sale_distribution_dataframe['day'] == weekday_name]

    # Convert the 'probability(in percent)' column to a list of integers
    probabilities = weekday_data['probability(in percent)'].astype(int).tolist()

    # Convert the 'sale range' column to a list of tuples containing the minimum and maximum values
    sale_ranges = [(int(x.split('-')[0]), int(x.split('-')[1])) for x in weekday_data['sale range'].tolist()]

    # Randomly select a sale range based on the given probabilities
    selected_range = random.choices(sale_ranges, weights=[p/100 for p in probabilities])[0]

    # Generate a random number within the selected sale range
    total = random.randint(selected_range[0], selected_range[1])

    return total

# used in get_distribution_of_sale_among_hours which is used in generate_day_sale_data
def divide_sale_num_among_hours(total, parts):
    # Generate a list of random integers between 1 and total - 1
    divisors = sorted(random.sample(range(1, total), parts - 1))
    # Calculate the differences between adjacent divisors and append total
    # to the list to get a list of parts that add up to total
    parts_list = [divisors[0]] + [divisors[i] - divisors[i - 1] for i in range(1, parts - 1)] + [total - divisors[-1]]

    return parts_list


def get_distribution_of_sale_among_hours(sale_per_time_of_day_dataframe, total_sale_num):
    distribution = {}
    for _, row in sale_per_time_of_day_dataframe.iterrows():
        time_period, sale_percentage = row['Time_of_day'], row['Sale_Percentage']
        start_hour, end_hour_plus_1 = [int(h) for h in time_period.split('-')]
        num_hours = end_hour_plus_1-start_hour
        end_hour = end_hour_plus_1 - 1
        num_of_sales = total_sale_num * float(sale_percentage)/ 100
        int_num_of_sales = int(num_of_sales)
        divided_sale_num_list = divide_sale_num_among_hours(int_num_of_sales, num_hours)
        counter = 0
        while num_hours !=0:
            distribution[start_hour] = divided_sale_num_list[counter]
            start_hour+=1
            num_hours -=1
    return distribution


# Define function to generate sales data for an hour
def generate_hour_sale_data(sale_id, date_obj, hour, total_sale_of_hour):
    pass

# Define function to generate sales data for a day
def generate_day_sale_data(sale_id, date):
    hour = 10
    day_data = []
    day_of_week = date.strftime('%A')  # get day of the week for the given date
    total_sale = get_daily_total(weekday_sale_distribution_data, day_of_week)  # generate total sale number for the day using weekday_sale_distribution_data
    distribution_of_sale_among_hours = get_distribution_of_sale_among_hours(sale_per_time_of_day_data, total_sale)
    while hour != 22:
        hourly_total = distribution_of_sale_among_hours[hour]
        hour_data, sale_id_ = generate_hour_sale_data(sale_id_, date, hour, hourly_total)
        day_data.append(hour_data)
        hour += 1

    print(day_data)
    return pd.concat(day_data), sale_id_


# Load data from Excel workbook
workbook = pd.read_excel('demo_sale_generator_constrains.xlsx', dtype=str, sheet_name=None)

# Extract each sheet as a separate DataFrame
menu_data = workbook['menu'].copy()

weekday_sale_distribution_data = workbook['weekday_sale_distribution'].copy()

sale_per_time_of_day_data = workbook['sale_per_time_of_day'].copy()

item_sale_probability_data = workbook['item_sale_probability'].copy()
# Convert probability percentages to decimal probabilities
item_sale_probability_data['Probability'] = item_sale_probability_data['Probability(in percentage)'].astype(float)/ 100.0

product_quantity_probability_data = workbook['Product_quantity_probability'].copy()
# Convert probability percentages to decimal probabilities
product_quantity_probability_data['Probability'] = product_quantity_probability_data['Probability(in percentage)'].astype(float) / 100.0

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