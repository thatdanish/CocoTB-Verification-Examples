# Setup 

SIM = icarus
TOPLEVEL_LANG = verilog

# Source file

VERILOG_SOURCES = $(shell pwd)/../src/simple_adder.sv

# COCO TB

COCOTB_TOPLEVEL = simple_adder

COCOTB_TEST_MODULES = test_simple_adder

# WAVES

WAVES = 1

# Housekeeping (necessary)
include $(shell cocotb-config --makefiles)/Makefile.sim

# Run GTkWave
wave: 
	gtkwave $(shell pwd)/sim_build/simple_adder.fst