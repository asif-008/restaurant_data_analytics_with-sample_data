import pandas as pd
from datetime import datetime, timedelta
import openpyxl
import random


# Define function to get total sales of a given day
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


# Define function to divide total sale numbers among hours
def divide_sale_num_among_hours(total, parts):

    if total == 0:
        parts_list = [0] * parts  # assign 0 to each part if total is 0
        return parts_list
    elif total == 1:
        parts_list = [0] * (parts-1) + [1]  # assign 0 to each part if total is 0
        return parts_list

    elif parts > total:
        parts_list = [0] * (parts - 1) + [total]  # assign 0 to each part if total is 0
        return parts_list

    # Generate a list of random integers between 1 and 'total - 1'
    divisors = sorted(random.sample(range(1, total), parts - 1))
    # Calculate the differences between adjacent divisors and append total
    # to the list to get a list of parts that add up to total
    parts_list = [divisors[0]] + [divisors[i] - divisors[i - 1] for i in range(1, parts - 1)] + [total - divisors[-1]]
    return parts_list


# Define function to get sale distribution among hours
def get_distribution_of_sale_among_hours(sale_per_time_of_day_dataframe, total_sale_num):
    distribution = {}
    for _, row in sale_per_time_of_day_dataframe.iterrows():
        time_period, sale_percentage = row['Time_of_day'], row['Sale_Percentage']
        start_hour, end_hour_plus_1 = [int(h) for h in time_period.split('-')]
        num_hours = end_hour_plus_1-start_hour
        end_hour = end_hour_plus_1 - 1
        num_of_sales = total_sale_num * float(sale_percentage)/ 100
        int_num_of_sales = int(num_of_sales)
        # Divide total sale numbers among hours
        divided_sale_num_list = divide_sale_num_among_hours(int_num_of_sales, num_hours)
        counter = 0
        while num_hours !=0:
            distribution[start_hour] = divided_sale_num_list[counter]
            start_hour+=1
            num_hours -=1
            counter +=1
    return distribution


# Define function to generate number of products for a sale
def generate_number_of_products(product_quantity_probability_dataframe):
    options = product_quantity_probability_dataframe['Product quantity'].tolist()
    option_probabilities = product_quantity_probability_dataframe['Probability'].tolist()
    # Use the random.choices() method to randomly choose an option based on the probabilities
    chosen_option = random.choices(options, weights=option_probabilities)[0]
    if len(chosen_option)==1:
        return int(chosen_option)
    else:
        min_option = int(chosen_option[0])
        max_option = int(chosen_option[2:])
        chosen_number = random.randint(min_option, max_option)
        return chosen_number


# Define function to generate a random item from menu
def generate_item(item_sale_probability_dataframe):
    options = item_sale_probability_dataframe['Item'].tolist()
    option_probabilities = item_sale_probability_dataframe['Probability'].tolist()
    # Use the random.choices() method to randomly choose an option based on the probabilities
    chosen_option = random.choices(options, weights=option_probabilities)[0]
    return chosen_option


# Define function to generate the details of a single sale
def generate_single_sale(id_of_sale):
    single_sale = []
    items = {}
    num_products = generate_number_of_products(product_quantity_probability_data)  # get the number of products for the sale using product_quantity_probability_data
    for i in range(num_products):
        item = generate_item(item_sale_probability_data)  # randomly choose an item from the menu using item_sale_probability_data
        if item in items.keys():
            items[item] += 1
        else:
            items[item] = 1
    for product in items.keys():
        single_sale.append([product, items[product]])
    id_of_sale += 1

    return single_sale, id_of_sale


# Define function to get the price of an item from the menu
def get_price(menu_dataframe, item_list):
    single_price = menu_dataframe.loc[menu_dataframe['item_name']==item_list[0], 'price' ].values[0]
    price = float(single_price)*int(item_list[1])

    return price


# Define function to generate sales data for an hour
def generate_hour_sale_data(sale_id, date_obj, hour, total_sale_of_hour):
    time_instances = []
    while len(time_instances) < int(total_sale_of_hour):
        random_num = random.randint(0, 59)
        if random_num not in time_instances:
            time_instances.append(random_num)

    time_instances.sort()
    hour_data = []
    for item in time_instances:

        single_sale, sale_id = generate_single_sale(sale_id)
        for an_item in single_sale:

            if item >= 10:
                complete_representation = [sale_id-1, date_obj.strftime("%Y-%m-%d"), str(hour) + ":" + str(item), "", "",
                                           ""]
            else:
                complete_representation = [sale_id-1, date_obj.strftime("%Y-%m-%d"), str(hour) + ":" + '0' + str(item),
                                           "", "", ""]

            price = get_price(menu_data, an_item)
            complete_representation[3] = an_item[0]
            complete_representation[4] = an_item[1]
            complete_representation[5] = price
            hour_data.append(complete_representation)

    return hour_data, sale_id


# Define function to generate sales data for a day
def generate_day_sale_data(sale_id_, date):
    hour = 10
    day_data = []
    day_of_week = date.strftime('%A')  # get day of the week for the given date
    total_sale = get_daily_total(weekday_sale_distribution_data, day_of_week)  # generate total sale number for the day using weekday_sale_distribution_data
    distribution_of_sale_among_hours = get_distribution_of_sale_among_hours(sale_per_time_of_day_data, total_sale)

    while hour != 22:
        hourly_total = distribution_of_sale_among_hours[hour]
        hour_data, sale_id_ = generate_hour_sale_data(sale_id_, date, hour, hourly_total)
        for item in hour_data:
            day_data.append(item)
        hour += 1
    return day_data, sale_id_


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

sales_data = []

# Set parameters
unique_id = 37589
start_date = '2019-01-01'
end_date = '2021-12-31'

date = datetime.strptime(start_date, '%Y-%m-%d')

g_date = date.strftime('%Y-%m-%d')

while g_date != end_date and unique_id <= 87589:
    day_data, unique_id = generate_day_sale_data(unique_id, date)
    unique_id = int(unique_id)
    for an_item in day_data:
        sales_data.append(an_item)
    date += timedelta(days=1)
    g_date = date.strftime('%Y-%m-%d')

# Create empty DataFrame for sales data
df = pd.DataFrame(sales_data, columns=['Unique Id', 'Date', 'Time', 'Item', 'Item_quantity', 'Price'])

# Write the dataframe to an Excel file
df.to_excel(r"C:\Users\Admin\Documents\Restaurant_analytics_on_sample_data\ sample_data.xlsx", index=False, engine='openpyxl')