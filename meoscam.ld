OUTPUT_FORMAT(binary)
SECTIONS {
	. = 0x0feffb;

	.data : {
			/* Just include the section here */
	}

	.text 0xff000 : {
		*(.text)
		*(.text.*)
    	*(.gnu.linkonce.t*)
	}

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
