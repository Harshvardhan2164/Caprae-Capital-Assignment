import time
import random

def rand_delay(min=1, max=3):
    time.sleep(random.uniform(min, max))