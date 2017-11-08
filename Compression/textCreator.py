from random import randint
import sys
import matplotlib.pyplot as plt

filename = "input - copia.txt"

text_file = open(filename, "w")

N = 20000
for i in range(1, N):
    rand = randint(0, 9)
    text_file.write("%d\tAvui fa un dia fantàstic MTP-S17	Equip D	SRI-1	%d\n" %(i,rand))

# text_file.close()

size_raw = sys.getsizeof(text_file)
print ("Size of raw text: ", size_raw, "B")