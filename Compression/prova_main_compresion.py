# import magic
#
#
# blob = open('unknown-file').read()
# m = magic.Magic(mime_encoding=True)
# encoding = m.from_buffer(blob)
#
#
# #read input file
# with codecs.open('USERS.CSV', 'r', encoding = 'latin-1') as file:
# lines = file.read()
#
# #write output file
# with codecs.open('1_UserPython.CSV', 'w', encoding = 'utf_8_sig') as file:
# file.write(lines)
#
#
# import io
# f = io.open("test", mode="r", encoding="utf-8")
#
# import codecs
# f = codecs.open("test", "r", "utf-8")
#
# f.read()
# u'Capit\xe1l\n\n'


import zlib

text = "hola avui fa molt sol, sol solet vinam a veure que fa sol"
compressed_text = zlib.compress(text.encode("utf-16"))
print(compressed_text)
text2 = zlib.decompress(compressed_text)
print(text2.decode("utf-16"))

