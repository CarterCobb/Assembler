# Dynamic Assembler

This assebler is writed in python. It takes common assembly commands and creates a `kerne7.img` that can be run on a [raspberry pi](https://www.raspberrypi.com/). This assemble has more potential as is collects and stores more data than is used to create that file.

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

- `<>` means descriptive item
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

## Example Assembly File

For testing purposes and proof of concept, an assemly command file is provided in this repo. It can be found [here](https://github.com/CarterCobb/Assembler/blob/master/assembly.txt).

This assembly will create output on the 21st GPIO pin on a raspberry pi and blink an LED bulb connected to that with a resistor.

## Roadmap

Currenlty this parser does not support register values pared with opperations. It currenlty only will handle immediate values. A plan to add register support is in place.

## Additional Details

This was built as an assignment for a college class at [Neumont College of Computer Science](https://www.neumont.edu/). Please do not use any part of this project in any way that would be considered plagiarism.
