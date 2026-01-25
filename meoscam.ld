OUTPUT_FORMAT(binary)
SECTIONS {
	. = 0xff000;
	_begin = 0xff000;

	.text 0xff000 : {
		*(.text)
		*(.text.*)
    	*(.gnu.linkonce.t*)
	}

	/* Only code is in here, no data */
	/DISCARD/ : {
		*(.reginfo)
		*(.MIPS.abiflags)

		*(.data)
		*(.data.*)
    	*(.gnu.linkonce.d*)

		*(.rodata)
		*(.rodata.*)
		*(.gnu.linkonce.r*)

		*(.rdata)
		*(.lit8)
		*(.lit4)

		*(.sdata)
		*(.sbss)
		*(.scommon)
		*(.bss)
	}

	_end = .;
}
