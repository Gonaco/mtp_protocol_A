import zlib
import io
import numpy as np

file_input = io.open("input.txt", mode="r", encoding="utf-16")
file_output_c = io.open("output_compressed.txt", mode="w", encoding="utf-16")

i = 0
ii= 0
num_comp=0
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
str_indices=str_indices[0:-1]
str_send = ''

for line in lines:
    char_line = np.array(list(line))
    char_line_send = char_line[where]
    for elem in char_line_send:
        str_send = str_send + elem
    str_send = str_send + '¬'
to_tx = lines[0] + '&' + str_indices + '&' + str_send


file_input.close()
file_output_c.write(to_tx)
file_output_c.close()

file_input2 = io.open("output_compressed.txt", mode="r", encoding="utf-16")
text = file_input2.read()

lines = text.split('&')

original = lines[0]
positions = lines[1].split('¬')
lines = lines[2].split('¬')

file_input2.close()
print("WRITING!!!!")
file_output= io.open("output.txt", mode="w", encoding="utf-16")
#file_output.write(original)
print(original)
for line in lines:
    line = list(line)
    next_line = original
    next_line = list(next_line)
    i = 0
    for pos in positions:
        intpos = int(pos)
        next_line[intpos] = line[i]
        i = i+1
    next_line = "".join(next_line)
    print(next_line)
    file_output.write(next_line)

print("fi programa")
