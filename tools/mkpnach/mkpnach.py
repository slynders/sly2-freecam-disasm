#!/bin/env python3

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# modules we depend on
from utils.mips import Mips
from utils.pnach import PnachWriter

# local modules
from regionconsts import REGION_TABLE
from addrtable import populateAddressTable, addrTable

# Reads a file in 4 byte (EE word) yielded chunks
def readWordChunks(file):
    while True:
        data = file.read(4)
        if not data:
            break
        yield data

# The fun begins...
def main():
    REGION_NAME = sys.argv[1]
    MATCHING = sys.argv[2]

    try:
        region = REGION_TABLE[REGION_NAME]
    except:
        print(f'Region {REGION_NAME} is not implemented yet')
        exit(1)

    # gather the correct blob filename based on whether or not it's matching.
    if MATCHING == 'y':
        BLOB_FILENAME = 'meoscam_code'
    else:
        BLOB_FILENAME = 'meoscam_code_nonmatching'

    # Populate the address table from the ELF.
    populateAddressTable(f'obj/{REGION_NAME}/{BLOB_FILENAME}_linked.elf')

    # Write the pnach out.

    pnachAuthor = 'Meos for original freecam, modeco80 initial disassembly.'
    pnachComment = 'Press L3 to enable freecam. See original Meos pnach for other controls.'

    with PnachWriter.file(f'{region['pnachCRC']}.freecam.pnach') as pnachWriter:
            with pnachWriter.cheat('Freecam', pnachAuthor, pnachComment) as cheat:
                cheat.comment(' For detailed contributor information to the disassembly,')
                cheat.comment(' see https://github.com/modeco80/sly2-freecam-disasm/graphs/contributors')

                # Poke in the hooks to the game code
                # vtable entry hook
                cheat.setAddress(region['entryHookAddress'])
                cheat.word(Mips.jal(addrTable['meosFreecamEntryHook']))

                cheat.setAddress(region['func1HookAddress'])
                cheat.word(Mips.jal(addrTable['meosFreecamFunc1']))
                cheat.word(Mips.nop()) # delay slot nop

                cheat.setAddress(region['func2HookAddress'])
                cheat.word(Mips.j(addrTable['meosFreecamFunc2']))

                cheat.setAddress(region['func3HookAddress'])
                cheat.word(Mips.jal(addrTable['meosFreecamFunc3']))

                cheat.setAddress(region['func4HookAddress'])
                cheat.word(Mips.jal(addrTable['meosFreecamFunc4']))

                # For our last step, poke in the code blob.
                cheat.setAddress(addrTable['meosCamText'])
                with open(f'obj/{REGION_NAME}/{BLOB_FILENAME}.bin', 'rb') as codeFile:
                    for word in readWordChunks(codeFile):
                            cheat.word(word)

    print('pnach file written successfully')

if __name__ == '__main__':
    main()
