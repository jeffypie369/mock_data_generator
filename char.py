import random
from faker import Faker
import string

random.seed(0)
Faker.seed(0)
fake = Faker()


"""
Generates random strings of specified length and pattern.

Args:
    length (int): Length of the generated strings. Default is 10.
    pattern (list): List of characters types to use for each position in the string.
        The characters types can be "letter", "digit", or any other character.
        Default is None, which generates a string with random characters.
    num_strings (int): Number of strings to generate. Default is 1.

Returns:
    list: List of randomly generated strings.

Raises:
    ValueError: If the length of the pattern is not equal to the specified length.
"""
def generate_random_strings(length=10, pattern=None, num_strings=1):
    if pattern is None:
        pattern = [None] * length

    if len(pattern) != length:
        raise ValueError("Length of the pattern must be equal to the specified length")

    def random_char(char_type):
        if char_type == "letter":
            return random.choice(string.ascii_letters)
        elif char_type == "digit":
            return random.choice(string.digits)
        else:
            return random.choice(string.ascii_letters + string.digits)

    def random_string():
        return ''.join(random_char(char_type) for char_type in pattern)

    return [random_string() for _ in range(num_strings)]

def id_generator(max_length=50, num_rows=100):
  # Define the list of possible characters to use in the mock data
  possible_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

  # Generate the mock data
  mock_data = []
  for i in range(num_rows):
      # Generate a random length for the VARCHAR string
      length = random.randint(1, max_length)
      # Generate a random string of the desired length using the possible_chars
      varchar_data = ''.join(random.choice(possible_chars) for _ in range(length))
      mock_data.append(varchar_data)

  return mock_data

# Generate mock postcode
def postcode_generator(num_rows=10):
  postcodes = [fake.unique.postcode() for i in range(num_rows)]
  return postcodes





