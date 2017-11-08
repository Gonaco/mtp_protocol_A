# coding=utf-8

import zlib
import io
import numpy as np

# file_input = io.open("input.txt", mode="r", encoding="utf-16")
# file_output_c = io.open("output_compressed.txt", mode="wb")
#
#
# for line in file_input:
#     print(line)
#     compressed_line = zlib.compress(line.encode("utf-16"))
#     file_output_c.write(compressed_line)
# file_output_c.close()
# file_input.close()

file_input = io.open("input.txt", mode="r", encoding="utf-16")
file_output_c = io.open("output_compressed.txt", mode="wb")

i = 0
ii= 0
num_comp  =0
lines = file_input.readlines()
line = lines[0]
comps_res = np.array([], dtype=np.bool).reshape(0,len(line))
for line in lines:
    char_line = np.array(list(line))
    i = i+1
    ii=0
    for line2 in lines:
        ii = ii+1
        if (ii>=i): #pendent a optimitzar per fer tots amb tots
            char_line2 = np.array(list(line2))
            comp_res = char_line==char_line2
            comps_res = np.vstack((comps_res,comp_res))
            print(line2)
            num_comp = num_comp +1
print(num_comp)
results = np.mean(comps_res, axis=0)
where = np.where(results < 0.3)[0]
#enviar numericament millor?
#optimitzar string?
where_str = map(str, where)
str_indices = ''
for str in where_str:
    str_indices = str_indices + str + "¬"

str_send = ''

for line in lines:
    char_line = np.array(list(line))
    char_line_send = char_line[where]
    for elem in char_line_send:
        str_send = str_send + elem
    str_send = str_send + '¬'

to_tx = lines[1] + '&' + str_indices + '&' + str_send

for line in file_input:
    print(line)
    compressed_line = zlib.compress(line.encode("utf-16"))
    file_output_c.write(compressed_line)
file_output_c.close()
file_input.close()