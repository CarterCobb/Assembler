
from posixpath import split
from pprint import pprint
import re


class Mnemonic:

    def __init__(self):
        self.op_codes = {
            'AND': 0b1000,
            'EOR': 0b0001,
            'SUB': 0b0010,
            'RSB': 0b0011,
            'ADD': 0b0100,
            'ADC': 0b1010,
            'SBC': 0b0110,
            'RSC': 0b0111,
            'TST': 0b1000,
            'TEQ': 0b1001,
            'CMP': 0b1010,
            'CMN': 0b1011,
            'ORR': 0b1100,
            'MOV': 0b1101,
            'BIC': 0b1110,
            'MVN': 0b1111,
            'B': 0b1010,
            'LDR': 0b01000001,
            'STR': 0b01000000,
            'LDM': 0b100, # PUSW1
            'STM': 0b100 # PUSW0
        }
        self.mov_large = {
            'MOVW': 0b00110000,
            'MOVT': 0b00110100
        }
        self.condition_codes = {
            'EQ': 0b0000,
            'NE': 0b0001,
            'CS': 0b0010,
            'CC': 0b0011,
            'MI': 0b0100,
            'PL': 0b0101,
            'VS': 0b0110,
            'VC': 0b0111,
            'HI': 0b1000,
            'LS': 0b1001,
            'GE': 0b1010,
            'LT': 0b1011,
            'GT': 0b1100,
            'LE': 0b1101,
            'AL': 0b1110
        }
        self.b_op_codes = {
            'L': 0b1011,
            'X': 0b0001
        }

    def parse_mnemonic(self, mnemonic, lines: list = None, parse_index = 0):
        print(mnemonic)
        mnemonic_action = mnemonic[0]
        m_len = len(mnemonic_action)
        if (m_len in [4, 6, 7]) and 'MOV' in mnemonic_action:
            mov_cond_code = mnemonic_action[-2:] if m_len == 6 else 'AL'
            cond = self._ensure_bits(self.condition_codes[mov_cond_code], 4)
            op = self._ensure_bits(self.mov_large.get(mnemonic_action[0:4]), 8)
            imm = self._split_16_bit(mnemonic[2].replace('0x', ''))
            rd = self._ensure_bits(mnemonic[1].replace('R', ''), 4)
            imm4, imm12 = imm[0], imm[1]
            binary = f'{cond}{op}{imm4}{rd}{imm12}'
            hex_conversion = self._bits_to_hex(binary)
            return {
                'binary': binary,
                'hex': hex_conversion[0],
                'encode': hex_conversion[1],
                'cond_code': mov_cond_code,
                's': False,  # MOVT & MOVW cannot have an 's' bit
                'op_code': mnemonic_action[0:4],
                'assembly': ' '.join(mnemonic)
            }
        op_code = 'B' if mnemonic_action[0] == 'B' else mnemonic_action[0:3]
        cond_code = mnemonic_action[-2:] if m_len in [5, 6] else 'AL'
        if op_code == 'B' and m_len == 3:
            cond_code = mnemonic_action[-2:] if m_len in [3] else 'AL'
        cond = self._ensure_bits(self.condition_codes[cond_code], 4)
        s = False
        if mnemonic_action[0:3] in ['LDR', 'STR']:
            op = self._ensure_bits(self.op_codes.get(mnemonic_action[0:3]), 8)
            rd = self._ensure_bits(mnemonic[1].replace('R', ''), 4)
            rn = self._ensure_bits(mnemonic[2].replace('R', ''), 4)
            offest = '000000000000'
            if len(mnemonic) in [4, 5]: offest = self._ensure_bits(int(mnemonic[3].replace('0x', ''), 16), 12)
            binary = f'{cond}{op}{rn}{rd}{offest}'
        elif mnemonic_action[0:3] in ['LDM', 'STM']:
            rn = self._ensure_bits(re.sub('R|\!', '', mnemonic[1]), 4)
            chunk = ['0'] * 5
            if 'P' in mnemonic[0]: chunk[0] = '1' # pre/post
            if 'U' in mnemonic[0]: chunk[1] = '1' # up/down
            if '!' in mnemonic[1]: chunk[3] = '1' # writeback
            if 'LDM' in mnemonic[0]: chunk[4] = '1' # set on to load
            r_list = ['1'] * 16
            if '-' in mnemonic[2]: 
                split_r = [int(r.replace('R', '')) for r in mnemonic[2].split('-')]
                small, big = split_r[0], split_r[1] + 1
                for i in range(16): 
                    if small <= i and i >= big: r_list[i] = '0' 
            binary = f"{cond}100{''.join(chunk)}{rn}{''.join(r_list[::-1])}"
        elif op_code == 'B':
            if m_len == 2:
                op = self._ensure_bits(self.b_op_codes.get(mnemonic_action[1:2]), 4)
                if ':' in mnemonic[1]:
                    label_i = self._get_lable_line(lines, mnemonic)
                    binary = f'{cond}{op}{self._ensure_bits(label_i - parse_index - 2, 24)}'
                else:
                    rn = self._ensure_bits(mnemonic[1].replace('R', ''), 4)
                    binary = f'{cond}{op}00101111111111110001{rn}'
            else:
                branch_back = self._hex_to_binary_safe(mnemonic[1])
                binary = self._pad_zeros(f'{cond}1010', branch_back)
        else:
            s_arr = [2, 3, 4, 5, 7]
            op = self._ensure_bits(self.op_codes.get(op_code), 4)
            s = mnemonic_action[-1] == 'S' if m_len in s_arr else False
            i = '0' if 'R' in mnemonic[-1] else '1'
            if i == '0':
                # TODO: implement register conversions vs the following immediate values
                binary = None
            else:
                rd = self._ensure_bits(mnemonic[1].replace('R', ''), 4)
                rn = self._ensure_bits(mnemonic[2].replace('R', ''), 4)
                imm = self._hex_to_binary_safe(mnemonic[3])
                binary = self._pad_zeros(
                    f"{cond}00{i}{op}{'1' if s else '0'}{rn}{rd}", imm)
        hex_conversion = self._bits_to_hex(binary)
        return {
            'binary': binary,
            'hex': hex_conversion[0],
            'encode': hex_conversion[1],
            'cond_code': cond_code,
            's': s,
            'op_code': op_code,
            'assembly': ' '.join(mnemonic)
        }

    def _split_16_bit(self, num):
        binary = bin(int(num, 16))[2:].rjust(16, '0')
        return (f'{binary[0:4]}', f'{binary[4:16]}')

    def _ensure_bits(self, num, bits):
        return bin(int(num))[2:].rjust(bits, '0')

    def _hex_to_binary_safe(self, hex_in):
        decimal_val = int(hex_in, 16)
        simplified = hex(decimal_val).replace('0x', '')
        return bin(int(simplified, 16))[2:].zfill(len(simplified) * 4)

    def _pad_zeros(self, front, proposed):
        num_zeros = 32 - (len(front) + len(proposed))
        zeros_str = '0' * num_zeros
        return f'{front}{zeros_str}{proposed}'

    def _bits_to_hex(self, binary):
        binary_to_hex = [hex(int(b, 2)).replace('0x', '') for b in re.findall('....', binary)]
        return (''.join(re.findall('..', ''.join(binary_to_hex))), ''.join(re.findall('..', ''.join(binary_to_hex))[::-1]))

    def _get_lable_line(self, lines, mnemonic):
        return max(loc for loc, val in enumerate(lines) if mnemonic[1] in val)