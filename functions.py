# Generate mock postcode
import math
import random
import string
import numpy as np
from collections import OrderedDict
from faker import Faker

locales = OrderedDict([
    ('en-US', 1),
    ('fr_FR', 2),
])

def postcode_generator(num_rows=10, selectivity=0.2, exclusion=None):
    fake = Faker()
    if exclusion is None:
        exclusion = []

    if selectivity == 0 or 1 / selectivity > num_rows:
        unique_data = num_rows
    else:
        unique_data = math.ceil(1 / selectivity)

    unique_postcodes = []
    while len(unique_postcodes) < unique_data:
        postcode = fake.unique.postcode()
        if postcode not in exclusion:
            unique_postcodes.append(postcode)

    postcodes = []
    for i in range(num_rows):
        postcodes.append(unique_postcodes[i % unique_data])

    random.shuffle(postcodes)
    return postcodes

# Generate mock credit card numbers
def credit_card_number_generator(num_rows=10, selectivity=0.2, exclusion=None):
    fake = Faker()
    if exclusion is None:
        exclusion = []

    if selectivity == 0 or 1 / selectivity > num_rows:
        unique_data = num_rows
    else:
        unique_data = math.ceil(1 / selectivity)

    unique_card_numbers = []
    while len(unique_card_numbers) < unique_data:
        card_number = fake.unique.credit_card_number(card_type='visa')
        if card_number not in exclusion:
            unique_card_numbers.append(card_number)

    card_numbers = []
    for i in range(num_rows):
        card_numbers.append(unique_card_numbers[i % unique_data])

    random.shuffle(card_numbers)
    return card_numbers

# Generate mock isbn
def isbn_generator(num_rows=10, selectivity=0.2, exclusion=None):
    fake = Faker()
    if exclusion is None:
        exclusion = []

    if selectivity == 0 or 1 / selectivity > num_rows:
        unique_data = num_rows
    else:
        unique_data = math.ceil(1 / selectivity)

    unique_isbns = []
    while len(unique_isbns) < unique_data:
        isbn = fake.unique.isbn10()
        if isbn not in exclusion:
            unique_isbns.append(isbn)

    isbns = []
    for i in range(num_rows):
        isbns.append(unique_isbns[i % unique_data])

    random.shuffle(isbns)
    return isbns

def id_generator(min=1, max=50, selectivity=0, exclusion=[], num_rows=100):
  # Define the list of possible characters to use in the mock data
  possible_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

  # Generate the mock data
  mock_data = []

  # Selectivity
  # Repeat value num_rows * selectivity times
  # Distribute remainder = num_rows - num_rows // (1/selectivity) evenly among values
  if selectivity > 0:
    num_values = int(1 // selectivity)
    seq = []
    for i in range(num_values):
      # Generate a random length for the VARCHAR string
      length = random.randint(min, max)
      # Generate a random string of the desired length using the possible_chars
      varchar_data = ''.join(random.choice(possible_chars) for _ in range(length))
      # Check nonequality constraint
      while varchar_data in exclusion:
        varchar_data = ''.join(random.choice(possible_chars) for _ in range(length))
      seq.append(varchar_data)
    num_repeats = num_rows // num_values
    remainder = num_rows - num_repeats * num_values
    seq = num_repeats * seq + seq[:remainder]
    np.random.shuffle(seq)
    mock_data = seq
  else:
    for i in range(num_rows):
      # Generate a random length for the VARCHAR string
      length = random.randint(min, max)
      # Generate a random string of the desired length using the possible_chars
      varchar_data = ''.join(random.choice(possible_chars) for _ in range(length))
      # Check nonequality constraint
      while varchar_data in exclusion:
        varchar_data = ''.join(random.choice(possible_chars) for _ in range(length))
      mock_data.append(varchar_data)

  return mock_data

def name_generator(max=50, num_rows=10, selectivity=0.2, exclusion=None, region='en_US'):
    fake = Faker(locales)
    if exclusion is None:
        exclusion = []

    if selectivity == 0 or 1 / selectivity > num_rows:
        unique_data = num_rows
    else:
        unique_data = math.ceil(1 / selectivity)

    unique_names = []
    while len(unique_names) < unique_data:
        name = fake[region].name()
        if name[:max] not in exclusion:
            unique_names.append(name[:max])

    names = []
    for i in range(num_rows):
        names.append(unique_names[i % unique_data])

    random.shuffle(names)
    return names

def address_generator(max=50, num_rows=10, selectivity=0.2, exclusion=None, region='en_US'):
    fake = Faker(locales)
    if exclusion is None:
        exclusion = []

    if selectivity == 0 or 1 / selectivity > num_rows:
        unique_data = num_rows
    else:
        unique_data = math.ceil(1 / selectivity)

    unique_addresses = []
    while len(unique_addresses) < unique_data:
        address = fake[region].address().replace('\n', ', ')
        if address[:max] not in exclusion:
            unique_addresses.append(address[:max])

    addresses = []
    for i in range(num_rows):
        addresses.append(unique_addresses[i % unique_data])

    random.shuffle(addresses)
    return addresses

def email_generator_from_names(names_list=[], max=50, num_rows=10, exclusion=None):
    if exclusion is None:
        exclusion = []

    possible_domains = ["@gmail.com", "@hotmail.com", "@outlook.com", "@yahoo.com"]
    emails = []

    # Loop until the desired number of email addresses is generated
    while len(emails) < num_rows:
        # Cycle through the names in the names_list
        for name in names_list:
            if len(emails) >= num_rows:
                break

            # Convert the name to lowercase and remove spaces
            name_parts = name.lower().split()
            name_email_base = "".join(name_parts)

            while True:
                # Add a random domain to the name
                name_email = name_email_base + random.choice(possible_domains)

                # If the generated email is not in the exclusion list, add it to the emails list
                if name_email not in exclusion:
                    emails.append(name_email[:max])
                    break

    return emails

def email_generator(max=50, selectivity=0, exclusion=[], num_rows=100, region='en_US'):
  fake = Faker(locales)
  possible_domains = ["@gmail.com", "@hotmail.com", "@outlook.com", "@yahoo.com"]
  mock_data = []

  if selectivity > 0:
    num_values = int(1 // selectivity)
    seq = []
    for i in range(num_values):
      name = fake[region].name().lower().replace(" ", "")
      email = name + random.choice(possible_domains)
      # Check nonequality constraint
      while email in exclusion:
        email = name + str(random.randint(1,99))+ random.choice(possible_domains)
      seq.append(email)
    num_repeats = num_rows // num_values
    remainder = num_rows - num_repeats * num_values
    seq = num_repeats * seq + seq[:remainder]
    np.random.shuffle(seq)
    mock_data = seq
  else:
    for i in range(num_rows):
      name = fake.name().lower().replace(" ", "")
      email = name + random.choice(possible_domains)
      # Check nonequality constraint
      while email in exclusion:
        email = name + str(random.randint(1,99))+ random.choice(possible_domains)
      mock_data.append(email)
  return mock_data

def generate_random_strings(length=10, pattern=None, num_rows=1, selectivity=0.2, exclusion=None):
    if exclusion is None:
        exclusion = []

    if selectivity == 0 or 1 / selectivity > num_rows:
        unique_data = num_rows
    else:
        unique_data = math.ceil(1 / selectivity)

    if pattern is None:
        pattern = [None] * length

    if len(pattern) != length:
        raise ValueError("Length of the pattern must be equal to the specified length")

    def random_char(char_type):
        if char_type == "l":
            return random.choice(string.ascii_letters)
        elif char_type == "d":
            return random.choice(string.digits)
        else:
            return random.choice(string.ascii_letters + string.digits)

    def random_string():
        return ''.join(random_char(char_type) for char_type in pattern)

    unique_strings = []
    while len(unique_strings) < unique_data:
        rand_string = random_string()
        if rand_string not in exclusion:
            unique_strings.append(rand_string)

    strings = []
    for i in range(num_rows):
        strings.append(unique_strings[i % unique_data])

    random.shuffle(strings)
    return strings

def int_generator(n, min, max, exclusion=None, unique=False, selectivity=0):

  """
  n: total count of integers to generate
  min: min value of list of integers
  max: max value of list of integers
  exclusion: list of unique values in (min, max) to be excluded from generation
  unique: True if integers generated must be unique, tops up with NULL values if number of different integers available < number of integers to generate
  selectivity: percentage in (0,1] for probability that any row is a particular value
  """

  range_size = max-min+1
  valid_range_size = range_size
  options = set(np.arange(min, max+1))

  probabilities = None
  if exclusion is not None:
    valid_range_size -= len(exclusion)
    probabilities = np.array(range_size*[1/valid_range_size])
    for num in exclusion:
      options.remove(num)
      probabilities[num-min] = 0

  rng = np.random.default_rng()
  options = sorted(options)

  if unique == False:

    if selectivity == 0: # default selectivity = (1 / valid range size) ie all options appear at least once

      complete_sets, remainder = divmod(n, valid_range_size)
      seq = complete_sets * options

      if remainder > 0:
        seq += list(rng.choice(options, size=remainder, replace=False))
      
    else: # custom selectivity
      n, total_n = round(1/selectivity), n

      if n > valid_range_size:
        return int_generator(n, min, max, exclusion = exclusion, unique=False, selectivity=0)
      
      seq = list(rng.choice(options, size=n, replace=False))
      
      np.random.shuffle(seq)
      repeats, remainder = divmod(total_n, n)
      seq = repeats*seq + seq[:remainder]
  
  else: # unique == True
    top_up = n - len(options)
    if top_up >= 0:
      seq = options + top_up * [None]
    else:
      seq = list(rng.choice(np.arange(min, max+1), size=n, replace=False, p=probabilities))

  np.random.shuffle(seq)
  return seq

def float_generator_normal(n, min, max, decimals=2):

  """
  n: total count of floating point numbers to generate
  min: min value of list of floats
  max: max value of list of floats
  decimals: number of digits after decimal point
  """

  normalized_seq = list(np.random.normal(0, 1, n))

  half_range = (max-min) / 2
  midpoint = min + half_range
  seq = [(normalized_val / 3.0902 * half_range) + midpoint for normalized_val in normalized_seq]
  seq = [round(val, decimals) for val in seq]

  return seq

def float_generator_uniform(n, min, max, exclusion=None, decimals=2, unique=False, selectivity=0):

  """
  n: total count of floats to generate
  min: min value of list of floats
  max: max value of list of floats
  exclusion: list of unique values in (min, max) to be excluded from generation
  decimals: number of digits after decimal point
  unique: True if floats generated must be unique, tops up with NULL values if number of different floats available < number of floats to generate
  selectivity: percentage in (0,1] for probability that any row is a particular value
  """

  pow = 10**decimals
  seq = int_generator(n, pow*min, pow*max, exclusion = None if exclusion is None else [pow*val for val in exclusion], unique=unique, selectivity=selectivity)
  seq = [val/pow for val in seq]

  return seq