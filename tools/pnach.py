# Pnach writing helpers

import binascii

def splitByCount(s, n):
    return [s[i:i+n] for i in range(0, len(s), n)]

# A pnach cheat
class _PnachCheat:
    def __init__(self, pnach_writer):
        self._pnach_writer = pnach_writer

    # writes a pnach patch to write the given word into memory once
    # if the provided bytestring is not large enough, it is padded with 0 bytes
    def word(self, bytestring, reverse=False):
        self._pnach_writer._write_word(bytestring, reverse)

    # same as word, but writes a freeze line
    def wordFreeze(self, bytestring, reverse=False):
        self._pnach_writer._write_word_freeze(bytestring, reverse)

    def setAddress(self, address: int):
        self._pnach_writer._set_address(address)

    # writes a comment. if you want the comment to have an initial space,
    # the string you pass here must have it.
    def comment(self, com: str):
        self._pnach_writer._write_comment(com)

    # Context manager functions
    def __enter__(self):
        self._old_address = self._pnach_writer._get_address()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._pnach_writer._set_address(self._old_address)


# A basic writer for pnach files. Supports usage as a context manager,
# so it's quite easy to use and code shouldn't get to ratty.
class PnachWriter:
    _addr: int

    # helper method which returns a pnach writer with the file open already
    @staticmethod
    def file(filename: str):
        return PnachWriter(open(filename, 'w'))

    def __init__(self, file):
       self._file = file
       self._addr = 0x0

    def _get_address(self) -> int:
        return self._addr

    def _set_address(self, address: int):
       self._addr = address

    def close(self):
        self._file.close()
        self._addr = 0x0

    # Begins cheat. Returns a object which can be used to add
    # patche lines to the cheat
    def cheat(self, section_name, author, comment) -> _PnachCheat:
       self._file.write(f'[{section_name}]\n')
       if author:
           self._file.write(f'author={author}\n')
       if comment:
           self._file.write(f'comment={comment}\n')
       return _PnachCheat(self)


    def _write_comment(self, comment):
       self._file.write(f'//{comment}\n')

    # writes a pnach patch to write the given word into memory
    # if the provided bytestring is not large enough, it is padded with 0 bytes
    def _write_word_cpu_mode(self, mode, cpu, bytestring, reverse=False):
       pad_length = len(bytestring) % 4

       if reverse:
        put_bytes = bytes(reversed(bytestring))
       else:
        put_bytes = bytes(bytestring)

       if pad_length:
            put_bytes += bytes(4 - len(bytestring))
       byte_string = binascii.hexlify(put_bytes).decode('utf-8')
       self._file.write(f'patch={mode},{cpu},20{self._addr:06x},extended,{byte_string}\n')
       self._addr += 0x4

    def _write_word(self, bytestring, reverse=False):
       self._write_word_cpu_mode('0', 'EE', bytestring, reverse)

    def _write_word_freeze(self, bytestring, reverse=False):
       self._write_word_cpu_mode('1', 'EE', bytestring, reverse)

    # IOP methods?

    # Context manager functions
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
