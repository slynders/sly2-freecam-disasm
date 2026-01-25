
AS := binutils/mips-ps2-decompals-as
LD := binutils/mips-ps2-decompals-ld
OBJCOPY := binutils/mips-ps2-decompals-objcopy

all: meoscam_code.bin

clean:
	rm meoscam_code.o meoscam_code.bin

#meoscam_code.bin: meoscam_code.elf
#	$(OBJCOPY) -O binary $< $@

meoscam_code.bin: meoscam_code.o
	$(LD) -T meoscam.ld $< -o $@


meoscam_code.o: meoscam.labels.asm
	$(AS) -EL -G0 -g -march=r5900 $< -o $@
