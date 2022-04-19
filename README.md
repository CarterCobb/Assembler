# Dynamic Assembler

This assembler is writed in python. It takes common assembly commands and creates a `kernel7.img` that can be run on a [raspberry pi](https://www.raspberrypi.com/). This assembler has more potential as is collects and stores more data than is used to create that file.

## Supported Opperation Codes

A list of supported OpCodes is as follows:

| Code | Code | Code | Code |
| ---- | ---- | ---- | ---- |
| AND  | ADC  | CMP  | MVN  |
| EOR  | SBC  | CMN  | B    |
| SUB  | RSC  | ORR  | LDR  |
| RSB  | TST  | MOV  | STR  |
| ADD  | TEQ  | BIC  | MOVW |
| MOVT | --   | --   | --   |

The assembler is capable of more. It follows dynamic rules to parse the commands.

## Supported Condition Codes

| Code | Code | Code |
| ---- | ---- | ---- |
| EQ   | PL   | GE   |
| NE   | VS   | LT   |
| CS   | VC   | GT   |
| CC   | HI   | LS   |
| MI   | LS   | AL   |

## Assembly Command Syntax

`<op_code><cond_code><s?> <rd?>, <rn?>, <hex value up to 3 bytes>`

Rules:

- `<>` means descriptive item; dont include the angle brackets
- `?` means the item is optional
- Spaces are mandatory
- Commas are not mandatory

Help:

- `op_code` = the opperation to execute. e.g `ADD`
- `cond_code` = the condition code. e.g `PL`. Defaults to `AL` if not specified
- `s` = the s bit when applicable. Defaults to `0` if not specified
- `rd` = desination register
- `rn` = orign register
- `hex value` = a hex value up to 3 bytes e.g. 0xFFFFFF (some commands max at 1-2 bytes)

## Running The Program

Please ensure you have at least Python V3 installed. `f` strings are used and will not compile on older versions of Python.

- In the project root run the `assembler.py` file with `python3`
- You will be promted for a file path to your assembly command file; enter that. e.g `./assembly.txt`

### Example Output

```text
Saved to kernel7.img

-----Parsed Data-----
{'binary': '11100011000000000100000000000000', 'cond_code': 'AL', 's': False, 'op_code': 'MOVW', 'assembly': 'MOVW R4 0x0'}
{'binary': '11100011010000110100111100100000', 'cond_code': 'AL', 's': False, 'op_code': 'MOVT', 'assembly': 'MOVT R4 0x3F20'}
{'binary': '11100010100001000010000000001000', 'cond_code': 'AL', 's': False, 'op_code': 'ADD',  'assembly': 'ADD R2 R4 0x08'}
{'binary': '11100100000100100011000000000000', 'cond_code': 'AL', 's': False, 'op_code': 'LDR',  'assembly': 'LDR R3 R2'}
{'binary': '11100011100000110011000000001000', 'cond_code': 'AL', 's': False, 'op_code': 'ORR',  'assembly': 'ORR R3 R3 0x000008'}
{'binary': '11100100000000100011000000000000', 'cond_code': 'AL', 's': False, 'op_code': 'STR',  'assembly': 'STR R3 R2'}
{'binary': '11100010100001000011000000011100', 'cond_code': 'AL', 's': False, 'op_code': 'ADD',  'assembly': 'ADD R3 R4 0x1c'}
{'binary': '11100011000000000010000000000000', 'cond_code': 'AL', 's': False, 'op_code': 'MOVW', 'assembly': 'MOVW R2 0x0000'}
{'binary': '11100011010000000010000000100000', 'cond_code': 'AL', 's': False, 'op_code': 'MOVT', 'assembly': 'MOVT R2 0x0020'}
{'binary': '11100100000000110010000000000000', 'cond_code': 'AL', 's': False, 'op_code': 'STR',  'assembly': 'STR R2 R3'}
{'binary': '11100011000001000101001001000000', 'cond_code': 'AL', 's': False, 'op_code': 'MOVW', 'assembly': 'MOVW R5 0x4240'}
{'binary': '11100011010000000101000000001111', 'cond_code': 'AL', 's': False, 'op_code': 'MOVT', 'assembly': 'MOVT R5 0x000F'}
{'binary': '11100010010101010101000000000001', 'cond_code': 'AL', 's': True,  'op_code': 'SUB',  'assembly': 'SUBS R5 R5 0x1'}
{'binary': '01011010111111111111111111111101', 'cond_code': 'PL', 's': False, 'op_code': 'B',    'assembly': 'BPL 0xFFFFFD'}
{'binary': '11100010100001000011000000101000', 'cond_code': 'AL', 's': False, 'op_code': 'ADD',  'assembly': 'ADD R3 R4 0x28'}
{'binary': '11100011000000000010000000000000', 'cond_code': 'AL', 's': False, 'op_code': 'MOVW', 'assembly': 'MOVW R2 0x0000'}
{'binary': '11100011010000000010000000100000', 'cond_code': 'AL', 's': False, 'op_code': 'MOVT', 'assembly': 'MOVT R2 0x0020'}
{'binary': '11100100000000110010000000000000', 'cond_code': 'AL', 's': False, 'op_code': 'STR',  'assembly': 'STR R2 R3'}
{'binary': '11100011000001000101001001000000', 'cond_code': 'AL', 's': False, 'op_code': 'MOVW', 'assembly': 'MOVW R5 0x4240'}
{'binary': '11100011010000000101000000001111', 'cond_code': 'AL', 's': False, 'op_code': 'MOVT', 'assembly': 'MOVT R5 0x000F'}
{'binary': '11100010010101010101000000000001', 'cond_code': 'AL', 's': True,  'op_code': 'SUB',  'assembly': 'SUBS R5 R5 0x1'}
{'binary': '01011010111111111111111111111101', 'cond_code': 'PL', 's': False, 'op_code': 'B',    'assembly': 'BPL 0xFFFFFD'}
{'binary': '11101010111111111111111111101110', 'cond_code': 'AL', 's': False, 'op_code': 'B',    'assembly': 'B 0xFFFFEE'}
```

## Example Assembly File

For testing purposes and proof of concept, an assembly command file is provided in this repo. It can be found [here](https://github.com/CarterCobb/Assembler/blob/master/assembly.txt).

This assembly will create output on the 21st GPIO pin on a raspberry pi and blink an LED bulb connected to that with a resistor.

## Roadmap

Currently this parser does not support register values pared with opperations. It currenlty only will handle immediate values. A plan to add register support is in place.

## Additional Details

This was built as an assignment for a college class at [Neumont College of Computer Science](https://www.neumont.edu/). Please do not use any part of this project in any way that would be considered plagiarism.
