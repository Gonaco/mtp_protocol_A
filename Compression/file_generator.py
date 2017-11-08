import string
import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
num_characters = 1000

def randomword(length):
   letters = string.ascii_lowercase + string.digits
   x = np.linspace(0, 1, len(letters))
   pdf = np.exp(x)
   pdf = pdf/np.sum(pdf)
   return ''.join(random.choice(list(letters), pdf) for i in range(length))

string_random = randomword(100)
h = plt.hist(string_random)
plt.show()
# file = open("file.txt", "w")
# file.write("Calibrated pixel size (um): " +str(pixel_size*1000)+"\n")


