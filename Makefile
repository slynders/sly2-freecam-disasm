# place decompals binutils in binutils/ to build it
AS := binutils/mips-ps2-decompals-as
LD := binutils/mips-ps2-decompals-ld
OBJCOPY := binutils/mips-ps2-decompals-objcopy

ifeq ($(MATCHING),)
MATCHING:=y
endif

REGION=pal

ifneq ($(REGION),pal)
MATCHING := n
endif

OBJDIR := obj/$(REGION)

# objects (in the correct order)
OBJECTS := \
	$(OBJDIR)/main.o \
	$(OBJDIR)/hooks.o \
	$(OBJDIR)/vars.o

ifeq ($(MATCHING),y)
all: $(OBJDIR)/ $(OBJDIR)/meoscam_code.bin check
else
all: $(OBJDIR)/ $(OBJDIR)/meoscam_code_nonmatching.bin
	./mkusapnach.py
endif

matrix:
	$(MAKE)
	$(MAKE) REGION=usa

matrixclean:
	$(MAKE) clean
	$(MAKE) REGION=usa clean

clean:
	rm -rf $(OBJDIR)

# check sha256sum matches, for PAL only
ifeq ($(MATCHING),y)
check:
	echo "b5c2ae13fdfc88fdf83ebb6acb83802cc3e9a5f680396cd39bda378068f7ec00  obj/pal/meoscam_code.bin" | sha256sum -c -
endif

$(OBJDIR)/:
	mkdir -p $@

ifeq ($(MATCHING),y)
$(OBJDIR)/meoscam_code.bin: $(OBJECTS)
	sed 's|REGIONLD|regions/$(REGION).ld|' src/meoscam.ld | sed 's|OBJDIR|$(OBJDIR)|' - > /tmp/lds_$(REGION).ld
	$(LD) -T /tmp/lds_$(REGION).ld $(OBJECTS) -o $(OBJDIR)/meoscam_code_linked.bin
	dd if=$(OBJDIR)/meoscam_code_linked.bin of=$@ bs=1 skip=5 status=none
else
$(OBJDIR)/meoscam_code_nonmatching.bin: $(OBJECTS)
	sed 's|REGIONLD|regions/$(REGION).ld|' src/meoscam.ld > /tmp/lds_$(REGION).ld
	$(LD) -T /tmp/lds_$(REGION).ld $(OBJECTS) -o $(OBJDIR)/meoscam_code_nonmatching_linked.bin
	dd if=$(OBJDIR)/meoscam_code_nonmatching_linked.bin of=$@ bs=1 skip=5 status=none
	rm /tmp/lds_$(REGION).ld
endif

$(OBJDIR)/%.o: src/%.asm
	$(AS) -EL -G0 -g -march=r5900 $< -o $@
