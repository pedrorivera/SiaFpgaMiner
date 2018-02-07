import os

from vunit import VUnit

# Create VUnit instance by parsing command line arguments
vu = VUnit.from_argv()

# Create library 'lib'
lib = vu.add_library("lib")

# Add all files ending in .vhd in the following directories
# dirs = [".", "Example", "Testbench"]
dirs = [".", "Testbench"]
script_path = os.path.dirname(__file__)
dirs = [os.path.realpath(
    os.path.join(script_path, "..", d, "*.vhd")) for d in dirs]
for d in dirs:
    lib.add_source_files(d)

# Run vunit function
vu.main()
