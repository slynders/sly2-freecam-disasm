OUTPUT_FORMAT(binary)
SECTIONS {
	. = 0xfeffb;

	.data 0x0feffb: {
		*(.data)
		*(.data.*)
    	*(.gnu.linkonce.d*)
	}


	.text 0xff000 : {
		*(.text)
		*(.text.*)
    	*(.gnu.linkonce.t*)
	}

	/DISCARD/ : {
		*(.reginfo)
		*(.MIPS.abiflags)


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

	/* Sly functions/variables that are referenced
	 TODO for region independence: seperate include file*/

	/* Functions. Names for these
	 may come from the May prototype of Sly 1. */
	FFloatsNear = 0x11d4d0;
	LoadRotateMatrixEuler = 0x11b628;
	SetCmMat = 0x14e190;

	/* Variables */
	CameraMatrix = 0x2e53a0;
	CameraUnk = 0x2e52e0;
	CameraZoom = 0x2e5364;

	HUDScaleX = 0x2a44e0;
	HUDScaleY = 0x2a44ec;

	GameClockSpeed = 0x2e52d8;
	EngineClockSpeed = 0x2e52f4;

	UnkVar = 0x2e6fc0;

	/* not sure */
	ControllerButtons = 0x2e80b4;

	ControllerButtonMaskLUT = 0x2c5bf0;

	_end = .;
}
