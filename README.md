# GZIControlStickPatchGen

A small script for generating GZI patch files for use with [gzinject](https://github.com/krimtonz/gzinject) that replace the default control stick mapping in the Wii VC versions of Ocarina of Time with one that more closely matches the feel of the N64 version of the game. 

Please note that this is completely illegal for all speed runs and is intended for either new speedrunners who are learning and don't yet have access to an ESS adapter or for randomizer players who want to play on VC in glorious 480p without having annoying control issues.

## Usage

For most users the only important part of this repository is the `generate.py` script. It has a number of options as detailed below, but at its most basic it simply needs to be given the region of the WAD it is patching. For example `./generate.py -r na` will generate a GZI patch file that works with the North American WAD version (NACE), while `./generate.py -r jp` will generate a patch that works with the Japanese WAD (NACJ).

```
usage: generate.py [-h] -r {na,jp,eu} [-d DEADZONE] [-e EXTENTS]
                   [-o OUTPUT_FILE]

required arguments:
  -r {na,jp,eu}, --region {na,jp,eu}
                        Region of the targeted WAD

optional arguments:
  -d DEADZONE, --deadzone DEADZONE
                        Radius of the control stick deadzone (default: 0)
  -e EXTENTS, --extents EXTENTS
                        Maximum control stick value in each direction.Specify
                        1 value to set all directions together or 4 values
                        (right, left, up, down) separated by commas to set
                        each direction individually (default: 106)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        Name of the output patch file (default: stick-
                        patch.gzi)
```

### Additional Examples

`./generate.py -r na --deadzone 4`  
`./generate.py -r jp --deadzone 2 --extents 110`  
`./generate.py -r eu --deadzone 2 --extents 110,114,109,106`  
`./generate.py -r na --output patch-for-na-wad.gzi`

## Additional Information

The remainder of the files in this repository either are files used by `generate.py` for creating the patches or are helper infrastructure for developing the actual mapping functions that is injected by generate.

### Patches Directory

Contains the base patches for each of the three base WAD types as well as the prebuilt raw binary files that contain the actual machine code to be injected by the patches.

### Docker Directory

Contains some scripts used in to help with creating and using a docker image which contains the necessary tools for assembling the `asm` files in the `assembly` directory. `build-image.sh` will build the initial Docker image and update it if changes are made to `image-files\Dockerfile.templ`. `bash.sh` will open a bash prompt in a container of the image. `make-asm.sh` will run `make` in the `assembly` directory within the container. An obvious prerequisite is that Docker needs to be installed and usable by the current user.

### Assembly Directory

Contains the `asm` files for the patch to the stick mapping call site and the actual mapping function. These are the files that the prebuilt binaries in `patches/binaries` are generated from.

### Scripts Directory

Contains the python script `gc-n64.py` which is an example implementation in python of the stick mapping function which can be used to test changes before writing them in assembly.