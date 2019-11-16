#!/usr/bin/python3

import os
import argparse
import struct

PATCH_DIRECTORY = "patches"
BINARIES_DIRECTORY = "patches/binaries"

MAPPING_FUNC_BIN = "mapping-func.bin"
CALL_SITE_BIN = "call-site.bin"

NACE_PATCH = "NACE_base_patch.gzi"


def read_binary_file(path):
    with open(path, 'rb') as b:
        return bytearray(b.read())

def read_text_file(path):
    with open(path, 'r+') as t:
        return t.read()

def inject_options_to_mapping_func(binary, deadzone, extents):
    binary[48:56] = struct.pack('>d', extents['right'])
    binary[56:64] = struct.pack('>d', extents['left'])
    binary[64:72] = struct.pack('>d', extents['up'])
    binary[72:80] = struct.pack('>d', extents['down'])
    binary[88:96] = struct.pack('>d', deadzone)

def generate_gzi_section(offset, data):
    assert len(data) % 4 == 0

    section_text = ""

    index = 0
    while index < len(data):
        word_offset = offset + index
        word = (data[index] << 24) | (data[index + 1] <<
                                      16) | (data[index + 2] << 8) | data[index + 3]
        section_text = section_text + \
            ('0304 %08X %08X\n' % (word_offset, word))

        index = index + 4

    return section_text.strip()

def write_text_file(text, path):
    with open(path, 'w+') as sp:
        sp.write(text)


def main():
    def positive_int(value):
        try:
            value = int(value)
            if value < 0:
                raise Error()
        except:
            raise argparse.ArgumentTypeError(
                'Deadzone radius must be a positive integer')
        return float(value)

    def stick_extents(value):
        values = value.split(',')
        num_values = len(values)

        if num_values != 1 and num_values != 4:
            raise argparse.ArgumentTypeError(
                'Stick extents only accepts 1, or 4 arguments')

        int_values = []

        try:
            for v in values:
                int_values.append(int(v))
        except:
            argparse.ArgumentTypeError(
                'Stick extents values must be positive integers')

        if num_values == 1:
            return {"right": float(int_values[0]),
                    "left": float(int_values[0]),
                    "up": float(int_values[0]),
                    "down": float(int_values[0])}
        else:
            return {"right": float(int_values[0]),
                    "left": float(int_values[1]),
                    "up": float(int_values[2]),
                    "down": float(int_values[3])}

    parser = argparse.ArgumentParser()

    # parser.add_argument('-r', '--region', type=str, choices=[
    #                     'na', 'jp', 'eu'], help="Region of the targeted WAD", required=False)

    parser.add_argument('-d', '--deadzone', type=positive_int, default=0,
                        help="Radius of the control stick deadzone (default 0)",)
    parser.add_argument('-e', '--extents', type=stick_extents, default={'right': 106.0, 'left': 106.0, 'up': 106.0, 'down': 106.0 },
                        help="Maximum control stick value in each direction." +
                        "Specify 1 value to set all directions together or 4 values (right, left, up, down) " +
                        "separated by commas to set each direction individually (default 106)")
    args = parser.parse_args()

    patch = read_text_file(os.path.join(PATCH_DIRECTORY, NACE_PATCH))

    mapping_bin = read_binary_file(os.path.join(BINARIES_DIRECTORY, MAPPING_FUNC_BIN))
    call_site_bin = read_binary_file(os.path.join(BINARIES_DIRECTORY, CALL_SITE_BIN))

    inject_options_to_mapping_func(mapping_bin, deadzone=args.deadzone, extents=args.extents)

    mapping_patch_text = generate_gzi_section(0x1e00, mapping_bin)
    call_site_patch_text = generate_gzi_section(0x5e028, call_site_bin)

    patch = patch.replace('__MAPPING_FUNCTION_PATCH__', mapping_patch_text)
    patch = patch.replace('__CALL_SITE_PATCH__', call_site_patch_text)

    write_text_file(patch, 'stick-patch.gzi')

main()
