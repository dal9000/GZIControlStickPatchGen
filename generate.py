#!/usr/bin/python3

import os

PATCH_DIRECTORY = "patches"
BINARIES_DIRECTORY = "patches/binaries"

MAPPING_FUNC_BIN = "mapping-func.bin"
CALL_SITE_BIN = "call-site.bin"

NACE_PATCH = "NACE_base_patch.gzi"

def read_in_mapping_func():
    with open(os.path.join(BINARIES_DIRECTORY, MAPPING_FUNC_BIN), 'rb') as mb:
        mapping_bin = mb.read()
        return mapping_bin    

def read_in_call_site_hook():
    with open(os.path.join(BINARIES_DIRECTORY, CALL_SITE_BIN), 'rb') as cs:
        call_site_bin = cs.read()
        return call_site_bin

def read_in_base_patch():
    with open(os.path.join(PATCH_DIRECTORY, NACE_PATCH), 'r+') as bp:
        patch_text = bp.read()
        return patch_text

def generate_gzi_section(offset, data):
    assert len(data) % 4 == 0

    section_text = ""

    index = 0
    while index < len(data):
        word_offset = offset + index
        word = (data[index] << 24) | (data[index + 1] << 16) | (data[index + 2] << 8) | data[index + 3]
        section_text = section_text + ('0304 %08X %08X\n' % (word_offset, word))

        index = index + 4
    
    return section_text.strip()

def write_final_patch(patch_text):
    with open('stick-patch.gzi', 'w+') as sp:
        sp.write(patch_text)

def main():
    patch = read_in_base_patch()
    mapping_bin = read_in_mapping_func()
    call_site_bin = read_in_call_site_hook()

    mapping_patch_text = generate_gzi_section(0x1e00, mapping_bin)
    call_site_patch_text = generate_gzi_section(0x5e028, call_site_bin)

    patch = patch.replace('__MAPPING_FUNCTION_PATCH__', mapping_patch_text)
    patch = patch.replace('__CALL_SITE_PATCH__', call_site_patch_text)
    
    write_final_patch(patch)

main()