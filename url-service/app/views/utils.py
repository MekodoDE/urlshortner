import random
import string

# Function to generate a random string
def generate_random_url_key(length=3):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))