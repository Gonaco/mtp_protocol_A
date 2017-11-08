import string
import random
import numpy as np
import matplotlib.pyplot as plt


def randomword(length):
    letters = ['a', 'b', 'c', 'd']
    p = [0.7, 0.1, 0.1, 0.1]
    p = np.array(p, dtype="float")
    return np.random.choice(letters, 15, p)


def randomword2(length):
   letters = string.ascii_lowercase + string.digits
   letters = ['a', 'b', 'c', 'd']
   x = np.linspace(0, 1, len(letters))
   pdf = np.exp(x)
   pdf = pdf/np.sum(pdf)

   np.array(list(pdf), dtype="|S1")
   array_str = np.array(list(letters), dtype="|S1")
   array_str = ['a', 'b', 'c', 'd']
   return random.choice(array_str, 15, pdf)

string_random = randomword(100)
string_random = randomword2(100)
print(string_random)