#!/usr/bin/python3

import os
import argparse
import struct

PATCH_DIRECTORY = "patches"
BINARIES_DIRECTORY = "patches/binaries"

MAPPING_FUNC_BIN = "mapping-func.bin"
CALL_SITE_BIN = "call-site.bin"

NACE_PATCH = "NACE_base_patch.gzi"
NACJ_PATCH = "NACJ_base_patch.gzi"
NACP_PATCH = "NACP_base_patch.gzi"

NACE_CALL_SITE_OFFSET = 0x5e028
NACJ_CALL_SITE_OFFSET = 0x5df98
NACP_CALL_SITE_OFFSET = 0x5e068

MAPPING_FUNC_OFFSET = 0x1e00

INTERRUPT_SECTION_OFFSET = 0x100
INTERRUPT_SECTION_ADDRESS = 0x80004000
PROGRAM_SECTION_OFFSET = 0x25E0
PROGRAM_SECTION_ADDRESS = 0x80007020


def read_binary_file(path):
    with open(path, 'rb') as b:
        return bytearray(b.read())


def read_text_file(path):
    with open(path, 'r+') as t:
        return t.read()


def write_text_file(text, path):
    with open(path, 'w+') as sp:
        sp.write(text)


def encode_bl_instruction(branch_offset):
    return 0x48000000 | (branch_offset & 0x03FFFFFC) | 0x1


def inject_options_to_mapping_func(binary, deadzone, extents):
    binary[48:56] = struct.pack('>d', float(extents['right']))
    binary[56:64] = struct.pack('>d', float(extents['left']))
    binary[64:72] = struct.pack('>d', float(extents['up']))
    binary[72:80] = struct.pack('>d', float(extents['down']))
    binary[88:96] = struct.pack('>d', float(deadzone))


def inject_branch_to_call_site(binary, call_site_offset):
    bl_inst_offset = 32
    mapping_func_start_offset = 96

    mapping_func_raw_address = INTERRUPT_SECTION_ADDRESS + \
        MAPPING_FUNC_OFFSET - INTERRUPT_SECTION_OFFSET

    call_site_raw_address = PROGRAM_SECTION_ADDRESS + \
        call_site_offset - PROGRAM_SECTION_OFFSET

    bl_distance = (call_site_raw_address + bl_inst_offset) - \
        (mapping_func_raw_address + mapping_func_start_offset)

    bl_inst = encode_bl_instruction(-bl_distance)

    binary[bl_inst_offset:bl_inst_offset + 4] = struct.pack('>I', bl_inst)


def generate_gzi_section(offset, data):
    assert len(data) % 4 == 0

    section_text = ""

    index = 0
    while index < len(data):
        word_offset = offset + index
        word = struct.unpack('>I', data[index:index+4])[0]
        section_text = section_text + \
            ('0304 %08X %08X\n' % (word_offset, word))

        index = index + 4

    return section_text.strip()


def parse_cmd_arguments():
    def positive_int(value):
        value = int(value)
        if value < 0:
            raise ValueError

        return value

    def deadzone(value):
        try:
            return positive_int(value)
        except:
            raise argparse.ArgumentTypeError(
                'Deadzone radius must be a positive integer')

    def stick_extents(value):
        try:
            values = [positive_int(v) for v in value.split(',')]
            num_values = len(values)

            if num_values == 1:
                return {"right": values[0],
                        "left": values[0],
                        "up": values[0],
                        "down": values[0]}
            elif num_values == 4:
                return {"right": values[0],
                        "left": values[1],
                        "up": values[2],
                        "down": values[3]}
            else:
                raise argparse.ArgumentTypeError(
                    'Stick extents only accepts 1 or 4 arguments')

        except ValueError:
            raise argparse.ArgumentTypeError(
                'Stick extents values must be positive integers')

    parser = argparse.ArgumentParser()

    parser.add_argument('-r', '--region', type=str, choices=['na', 'jp', 'eu'],
                        help="Region of the targeted WAD", required=True)

    parser.add_argument('-d', '--deadzone', type=deadzone, default=0,
                        help="Radius of the control stick deadzone (default: 0)",)

    parser.add_argument('-e', '--extents', type=stick_extents, default={'right': 106.0, 'left': 106.0, 'up': 106.0, 'down': 106.0},
                        help="Maximum control stick value in each direction." +
                        "Specify 1 value to set all directions together or 4 values (right, left, up, down) " +
                        "separated by commas to set each direction individually (default: 106)")

    parser.add_argument('-o', '--output-file', type=str, default='stick-patch.gzi',
                        help="Name of the output patch file (default: stick-patch.gzi)")

    return parser.parse_args()


def main():
    args = parse_cmd_arguments()

    region = args.region

    base_patch = ""
    call_site_offset = 0

    if region == 'na':
        base_patch = NACE_PATCH
        call_site_offset = NACE_CALL_SITE_OFFSET
    elif region == 'jp':
        base_patch = NACJ_PATCH
        call_site_offset = NACJ_CALL_SITE_OFFSET
    else:
        base_patch = NACP_PATCH
        call_site_offset = NACP_CALL_SITE_OFFSET

    # Read base patch for the selected region
    patch = read_text_file(os.path.join(PATCH_DIRECTORY, base_patch))

    # Read in the raw binaries for the mapping function and call site patches
    mapping_bin = read_binary_file(os.path.join(
        BINARIES_DIRECTORY, MAPPING_FUNC_BIN))
    call_site_bin = read_binary_file(
        os.path.join(BINARIES_DIRECTORY, CALL_SITE_BIN))

    # Inject the selected options for the deadzone and stick extents into the mapping function
    inject_options_to_mapping_func(
        mapping_bin, deadzone=args.deadzone, extents=args.extents)

    # Inject the correct branch instruction to jump to the mapping function
    inject_branch_to_call_site(
        call_site_bin, call_site_offset=call_site_offset)

    # Generate the GZI text for both sections
    mapping_patch = generate_gzi_section(MAPPING_FUNC_OFFSET, mapping_bin)
    call_site_patch = generate_gzi_section(call_site_offset, call_site_bin)

    # Insert the generated sections into the patch file
    patch = patch.replace('__MAPPING_FUNCTION_PATCH__', mapping_patch)
    patch = patch.replace('__CALL_SITE_PATCH__', call_site_patch)

    # Write out final file
    write_text_file(patch, args.output_file)


main()
