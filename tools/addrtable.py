#!/bin/env python3

from elftools.elf.elffile import ELFFile
from elftools.elf.sections import SymbolTableSection

__all__ = [ 'addrTable', 'populateAddressTable' ]

# Table of name -> int address pair. Populated by populateAddressTable().
addrTable : dict[str, int] = {}

def findSymbolInElf(elfObject: ELFFile, symbolName: str):
    section = elfObject.get_section_by_name('.symtab')
    if not section:
        raise ValueError('ELF does not have a symbol table? WTF')
    if not isinstance(section, SymbolTableSection):
        raise ValueError('not a symbol table section? What?')

    for symbol in section.iter_symbols():
        if symbol.name == symbolName:
            return symbol['st_value']


def populateAddressTable(elfFileName: str):
    print(f'Loading code blob ELF file \'{elfFileName}\'')
    # Addresses which we care about here
    caredAddresses = [
        'meosCamText', # start of .text code section
        'meosFreecamEntryHook',
        'meosFreecamFunc1',
        'meosFreecamFunc2',
        'meosFreecamFunc3',
        'meosFreecamFunc4'
    ]
    with open(elfFileName, 'rb') as elfFile:
        elfObject = ELFFile(elfFile)
        for symName in caredAddresses:
            addrTable[symName] = findSymbolInElf(elfObject, symName)
            print(f'Located {symName} @ {addrTable[symName]:08x}')
