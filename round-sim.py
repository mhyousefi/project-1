import requests
import time
import json
from bs4 import BeautifulSoup
import re
from itertools import groupby
import math

PAGE_COUNT = {
    "910": 200,
    "911": 40,
    "912": 1200,
    "913": 150,
    "914": 15,
    "915": 300,
    "916": 35,
    "917": 120,
    "918": 15,
    "919": 120,
}

def request_phone_numbers(prefix, page_number):
    """
    :argument prefix: one of "910", "911", "912", ..., "919"
    :argument page_number: an integer greater than or equal to 1
    :returns list of dicts. each dict has 'phone_number' and 'price' fields.
    """
    result = requests.get('https://www.rond.ir/SearchSim/Mci/%s/Permanent' % prefix, dict(
        ItemPerPage=120,
        StateId=0,
        SimOrderBy='Update',
        page=page_number,
    ))
    soup = BeautifulSoup(result.text, 'html.parser')
    return [dict(
        phone_number=element.get_text().replace(' ', ''),
        price=re.sub(r'[^\d]', '', element.find_parent('tr').find_all('td')[2].get_text()),
    ) for element in soup.find_all('a', class_='t-link')]

def retrieve_data_from_website():
    """
    Retreives data from rond.ir and saves it in a "database.txt" file in the project directory
    """
    databaseFile = open("database.txt", mode='w+')
    dataList = []
    temp = []
    for prefix_value in range(910, 920, 1):
        print("***Retrieving data for prefix %d\n\n" %prefix_value)
        for i in range(PAGE_COUNT[str(prefix_value)]):
            temp = request_phone_numbers(prefix_value, i + 1)
            for j in temp:
                dataList.append(j)
            print("\nData saved for prefix, %d\tPage number: %d" % (prefix_value, i + 1))
            time.sleep(0.3)
    json.dump(dataList, databaseFile)

#Functions obtaining attributes regarding how ROUND a phone number is

def are_the_first_3digits_special(phone_number_dict):
    """

    :param phone_number_dict: a dictionary containing the phone number
    :return: returns True if the phone number starts with special 3-digit streaks:
    110, 111, 112 ... 119
    """

    if(str(phone_number_dict['phone_number'])[4:7] in
           ["110","111","112","113","114","115","116,","117","118","119"]):
        return True
    return False

def is_the_first_digit_1(phone_number_dict):
    """

    :param phone_number_dict: a dictionary containing the phone number
    :return: returns True if the phone number starts with 1
    """

    if (str(phone_number_dict['phone_number'])[4] == '1'):
        return True
    return False

def is_there_a_four_digit_symmetry(phone_number_dict):
    """

    :param phone_number_dict: a dictionary containing the phone number
    :return: returns True if there is a four-digit symmetry in the phone number like: 1221, 4334, ...
    """
    temp = str(phone_number_dict['phone_number'])
    for i in range(len(temp) - 3):
        if (temp[i] == temp[i+3] and temp[i+1] == temp[i+2]):
            return True
    return False

def num_of_zeros(phone_number_dict):
    """

    :param phone_number_dict: a dictionary containing the phone number
    :return: the number of zeros in the phone number
    """
    return (str(phone_number_dict['phone_number']).count('0') - 1)

def are_the_first_3digits_same_as_prefix(phone_number_dict):
    """

    :param phone_number_dict: a dictionary containing the phone number
    :return: True if such cases are present:
    0912 912...., 0913 913...., 0914 914....
    """
    if(phone_number_dict['phone_number'][1:4] ==
       phone_number_dict['phone_number'][4:7]):
        return True
    return False

def are_there_any_consecutive_similar_2digit_cases(phone_number_dict):
    """

    :param phone_number_dic: a dictionary containing the phone number
    :return: True if there are any cases of similar 2-digit numbers that have the same first digit
    Examples include: (12 14), (23 25), (34 36) ...
    """
    temp = str(phone_number_dict['phone_number'])
    for i in range(len(temp) - 3):
        if(temp[i] == temp[i+2]):
            return True
    return False

def are_there_any_consecutive_similar_3digit_cases(phone_number_dict):
    """

    :param phone_number_dic: a dictionary containing the phone number
    :return: True if there are any cases of similar 3-digit numbers that have the same first digit
    Examples include: (121 144), (236 254), (347 361) ...
    """
    temp = str(phone_number_dict['phone_number'])
    for i in range(len(temp) - 5):
        if (temp[i] == temp[i + 3]):
            return True
    return False

def list_of_consecutive_repetitions(phone_number_dict):
    """

    :param phone_number_dict: a dictionary containing the phone number
    :return: returns a list of tuples containing the numbers that have
    a streak and the length of the streak
    e.g. for 09121114358: ('1', 3)
    """
    phone_number_str = str(phone_number_dict['phone_number'])
    groups = groupby(phone_number_str)
    temp = [(label, sum(1 for _ in group)) for label, group in groups]
    result = []
    for item in temp:
        if item[1] > 1:
            result.append(item)
    return result

def repetition_streaks(phone_number_dict):
    """

    :param str: the last 7 digits of a phone number
    :return: a dictionary: [2_digit_long_repetitions,
                            3_digit_long_repetitions,
                            4_digit_long_repetitions,
                            5_digit_long_repetitions,
                            6_digit_long_repetitions,
                            7_digit_long_repetitions]
    """
    consecutive_rep_list = list_of_consecutive_repetitions(phone_number_dict)
    consecutive_reps = [0,0,0,0,0,0,0]

    for item in consecutive_rep_list:
        if item[1] == 2:
            consecutive_reps[0] += 1
        if item[1] == 3:
            consecutive_reps[1] += 1
        if item[1] == 4:
            consecutive_reps[2] += 1
        if item[1] == 5:
            consecutive_reps[3] += 1
        if item[1] == 6:
            consecutive_reps[4] += 1
        if item[1] == 7:
            consecutive_reps[5] += 1
        if item[1] == 8:
            consecutive_reps[6] += 1
    return consecutive_reps

#Functions processing data

def decode_locally_stored_data():
    """

    :return: loads and decodes the data saved with a json format in a (project directory) file and returns a list containing it
    """
    database_file = open("database.txt", mode='r', errors='i', encoding='utf-8')
    temp = database_file.readline()
    return json.loads(temp, encoding='utf-8')

def calculate_roundness_coefficient(phone_number_dict):
    """

    :param phone_number_dict: a dictionary containing a phone_number and a price
    :return: roundness coefficient for a phone number
    """
    roundness_coeff = 0
    streak_list = repetition_streaks(phone_number_dict)

    roundness_coeff += num_of_zeros(phone_number_dict)

    if are_there_any_consecutive_similar_2digit_cases(phone_number_dict):
        roundness_coeff += 5
    if are_there_any_consecutive_similar_3digit_cases(phone_number_dict):
        roundness_coeff += 2

    for i in range(0,7,1):
        roundness_coeff += streak_list[i]*(i+2)

    if is_the_first_digit_1(phone_number_dict):
        roundness_coeff += 2
    if are_the_first_3digits_special(phone_number_dict):
        roundness_coeff += 5

    if are_the_first_3digits_same_as_prefix(phone_number_dict):
        roundness_coeff += 5

    if is_there_a_four_digit_symmetry(phone_number_dict):
        roundness_coeff += 3

    return roundness_coeff

def filter_unuseful_data(data):
    """

    :param data: a list of phone number dictionaries
    :return: returns a version of the data in which those with empty price & non-digit phone-numbers are omitted
    """
    result = []
    for dict in data:
        if dict['price'] != "" and str(dict['phone_number']).isdigit():
            result.append(dict)
    return result

def find_max_metric(list):
    """

    :param list: an arbitrary list of dictionaries containing phone numbers and prices
    :return: a dic containing the maximum metric value and the list index where it is located
    """
    max = 0
    max_index = 0
    for j in range(len(list)):
        if list[j]["metric_value"] > max:
            max = list[j]["metric_value"]
            max_index = j
    return {"max_metric_value": max, "max_metric_index": max_index}

def normalize_data(list,max_metric_value):
    """

    :param list: a list of phone numbers dictionaries
    :param max_metric_value: the maximum metric value present in the list
    :return: returns a normalized version of the list
    """
    for i in list:
        i["metric_value"] = i["metric_value"] / max_metric_value
    return list

def process_data(data):
    """

    :return: applies the metric to data and returns a new list with another value, "metric_value"
    which is also normalized according to the maximum value
    """
    processed_data = []
    for item in data:
        temp = calculate_roundness_coefficient(item)
        processed_data.append({"phone_number": item["phone_number"], "price": item["price"], "metric_value": temp})

    max_metric = find_max_metric(processed_data)
    return normalize_data(processed_data,max_metric["max_metric_value"])

def top_numbers_for_max_price(max_num_of_phone_numbers, max_price, processed_data):
    """

    :param max_num_of_phone_numbers: the maximum number of phone numbers the user wishes to view
    :param max_price: the maximum price the user is willing to pay
    :param processed_data: data that has undergone all needed processes
    :return: returns the top phone numbers that match the users "max_price" criterion
    """
    roundest_phone_numbers = []
    processed_data_copy = []
    temp = {}

    for i in processed_data:
        processed_data_copy.append(i)

    for i in range(max_num_of_phone_numbers):
        while True:
            temp = find_max_metric(processed_data_copy)
            if int(processed_data_copy[temp["max_metric_index"]]["price"]) <= max_price:
                roundest_phone_numbers.append(processed_data_copy[temp["max_metric_index"]])
                processed_data_copy.remove(processed_data_copy[temp["max_metric_index"]])
                break
            else:
                processed_data_copy.remove(processed_data_copy[temp["max_metric_index"]])
    return roundest_phone_numbers

def main():
    #retrieve_data_from_website()
    raw_data = decode_locally_stored_data()
    processed_data = filter_unuseful_data(process_data(raw_data))
    max_price = int(input("Please enter the maximum price: "))
    max_num_of_phone_numbers = int(input("Please enter the maximum number of phone numbers to see: "))
    print(top_numbers_for_max_price(max_num_of_phone_numbers, max_price, processed_data))


main()
