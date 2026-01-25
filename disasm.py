#!/bin/env python3

import rabbitizer

# Enable stuff
rabbitizer.config.pseudos_enablePseudos = True

# origin
org = 0x000FF000

with open("meoscam_paired.csv") as inCsv:
	with open("meoscam.asm", "w") as outBin:
		outBin.write('.ps2\n')
		outBin.write(f'.create "meoscam_code.bin",{hex(org)}\n')
		outBin.write(f'.org {hex(org)}\n')

		for line in inCsv:
			line=line.strip()
			values=line.split(',')
			address=int(values[0], 16)
			hexWord=int(values[1], 16)
			instr = rabbitizer.Instruction(hexWord, vram=address, category=rabbitizer.InstrCategory.R5900)
			outBin.write(f'{instr.disassemble().replace('func_', '0x')}\n')
		outBin.write('.close')

