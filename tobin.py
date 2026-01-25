#!/bin/env python3

def splitByCount(s, n):
    return [s[i:i+n] for i in range(0, len(s), n)]

with open("meoscam_paired.csv") as inCsv:
	with open("meoscam_code_orig.bin", "wb") as outBin:
		for line in inCsv:
			line=line.strip()
			values=line.split(',')
			#address=int(values[0], 16)
			#hexWord=int(values[1], 16)
			groups = splitByCount(values[1], 2)
			# pnach forcing you to write the bytes in the wrong endian award
			hexWord = f'{groups[3]}{groups[2]}{groups[1]}{groups[0]}'
			outBin.write(bytes.fromhex(hexWord))

