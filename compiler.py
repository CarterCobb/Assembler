import subprocess
import re


class Compiler():

    def compile_blink_delay(self, n):
        lines = []
        with open('blink_template.txt') as file:
            for line in file.readlines():
                lines.append(line.replace('[N_TIMES]', hex(
                    n)) if '[N_TIMES]' in line else line)
        with open('__assembly__.txt', 'w') as file:
            file.writelines(lines)
        stdout_data = subprocess.run(
            ['python', 'assembler.py'], universal_newlines=True, capture_output=True, input='__assembly__.txt')
        print(re.sub(r'\n+(?=\n)', '', stdout_data.stdout))


if __name__ == '__main__':
    path = input("Enter a path to a program file:\r\n-> ")
    lines = []
    with open(path, 'r') as file:
        for line in [i for i in file.readlines() if i]:
            if line is not None and not line.isspace():
                lines.append(re.sub('\,|\\n|\(|\)', '', line))
    try:
        amount = int(lines[0]) - 1
        Compiler().compile_blink_delay(amount)
    except:
        print('------------- .porg file must contain an integer on line 1 -------------')
