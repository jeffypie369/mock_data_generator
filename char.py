
import random
from faker import Faker


random.seed(0)
Faker.seed(0)

fake = Faker()

# def id_generator(max_length=50, num_rows=100):
#   # Define the list of possible characters to use in the mock data
#   possible_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

#   # Generate the mock data
#   mock_data = []
#   for i in range(num_rows):
#       # Generate a random length for the VARCHAR string
#       length = random.randint(1, max_length)
#       # Generate a random string of the desired length using the possible_chars
#       varchar_data = ''.join(random.choice(possible_chars) for _ in range(length))
#       mock_data.append(varchar_data)

#   return mock_data





