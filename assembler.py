from mnemonic import Mnemonic
import re

"""
Assembly Command Structure:

Rules:
-`<>` means descriptive item
- ? means the item is optional
- Spaces are mandatory
- Commas are not mandatory

<op_code><cond_code><s?> <rd?>, <rn?>, <hex value up to 3 bytes>

Help:
-> op_code = the opperation to execute. e.g `ADD`
-> cond_code = the condition code. e.g `PL`. Defaults to `AL` if not specified
-> s = the s bit when applicable. Defaults to `0` if not specified
-> rd = desination register
-> rn = orign register
-> hex value = a hex value up to 3 bytes e.g. 0xFFFFFF (some commands max at 1-2 bytes)

"""

path = input("Enter a path to a command file:\r\n-> ")
mnemonic_dictionary = Mnemonic()
lines = []

# Read and parse file
with open(path, 'r') as file:
    for line in [i for i in file.readlines() if i]:
        if line is not None and not line.isspace(): lines.append(re.sub('\,|\\n|\(|\)', '', line))

parsed_mnemonics = [mnemonic_dictionary.parse_mnemonic(lines[i].split(' '), lines, i) for i in range(len(lines) - 1)]

encode = ''.join([h['encode'] for h in parsed_mnemonics])

# Encode binary into hex then to kernel7.img file
with open('kernel7.img', 'wb') as file:
    integers = []
    while encode:
        integers.append(int(encode[:2], 16))
        encode = encode[2:]
    file.write(bytearray(integers))

broken_parse = ''
for parse in parsed_mnemonics: broken_parse += f'{parse}\r\n'
print(f'Saved to kernel7.img\r\n\r\n-----Parsed Data-----\r\n{broken_parse}')
