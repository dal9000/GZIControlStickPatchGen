.PHONY: all

all: mapping-func.bin call-site.bin

clean:
	rm -f mapping-func.bin mapping-func.o call-site.bin call-site.o

mapping-func.o: mapping-func.asm
	powerpc-eabi-as -o $@ $<

mapping-func.bin: mapping-func.o
	powerpc-eabi-objcopy -O binary $< $@

call-site.o: call-site.asm
	powerpc-eabi-as -o $@ $<

call-site.bin: call-site.o
	powerpc-eabi-objcopy -O binary $< $@


