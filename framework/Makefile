TOPLEVEL_LANG ?= verilog
PWD=$(shell pwd)
SIM ?= verilator

ifeq ($(TOPLEVEL_LANG),verilog)
    VERILOG_SOURCES = $(PWD)/../src/CORE_I_Extension.v
    VERILOG_SOURCES += $(PWD)/../src/Program_Counter.v
    VERILOG_SOURCES += $(PWD)/../src/ALU.v
    VERILOG_SOURCES += $(PWD)/../src/ALU_Decoder.v
    VERILOG_SOURCES += $(PWD)/../src/Adder.v
    VERILOG_SOURCES += $(PWD)/../src/Control_Unit.v
    VERILOG_SOURCES += $(PWD)/../src/Data_Memory.sv
    VERILOG_SOURCES += $(PWD)/../src/Extension.v
    VERILOG_SOURCES += $(PWD)/../src/Instruction_Memory.sv
    VERILOG_SOURCES += $(PWD)/../src/Main_Decoder.v
    VERILOG_SOURCES += $(PWD)/../src/Result_Extension.v
    VERILOG_SOURCES += $(PWD)/../src/Register_File.v

else
    $(error A valid value (verilog or vhdl) was not provided for TOPLEVEL_LANG=$(TOPLEVEL_LANG))
endif

TOPLEVEL := CORE
MODULE   := TOP

include $(shell cocotb-config --makefiles)/Makefile.sim
