import requests
from bs4 import BeautifulSoup
import re


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


print(request_phone_numbers(prefix='910', page_number=1))
