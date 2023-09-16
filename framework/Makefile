TOPLEVEL_LANG ?= verilog
PWD=$(shell pwd)
SIM ?= verilator


EXTRA_ARGS += --trace-fst --trace-structs
WARNING_ARGS += -Wno-TIMESCALEMOD -Wno-WIDTH -Wno-UNOPT
	

ifeq ($(TOPLEVEL_LANG),verilog)
	VERILOG_SOURCES = $(PWD)/../hdl/el2_def.sv
	VERILOG_SOURCES += $(PWD)/../hdl/el2_pdef.vh
	VERILOG_SOURCES += $(PWD)/../hdl/ahb_sif.sv
	VERILOG_SOURCES += $(PWD)/../hdl/ahb_to_axi4.sv
	VERILOG_SOURCES += $(PWD)/../hdl/axi4_to_ahb.sv
	VERILOG_SOURCES += $(PWD)/../hdl/beh_lib.sv
	VERILOG_SOURCES += $(PWD)/../hdl/common_defines.vh
	VERILOG_SOURCES += $(PWD)/../hdl/el2_dbg.sv
	VERILOG_SOURCES += $(PWD)/../hdl/el2_dec.sv
	VERILOG_SOURCES += $(PWD)/../hdl/el2_dec_decode_ctl.sv
	VERILOG_SOURCES += $(PWD)/../hdl/el2_dec_gpr_ctl.sv
	VERILOG_SOURCES += $(PWD)/../hdl/el2_dec_ib_ctl.sv
	VERILOG_SOURCES += $(PWD)/../hdl/el2_dec_tlu_ctl.sv    
	VERILOG_SOURCES += $(PWD)/../hdl/el2_dec_trigger.sv
	VERILOG_SOURCES += $(PWD)/../hdl/el2_dma_ctrl.sv
	VERILOG_SOURCES += $(PWD)/../hdl/el2_exu.sv
	VERILOG_SOURCES += $(PWD)/../hdl/el2_exu_alu_ctl.sv
	VERILOG_SOURCES += $(PWD)/../hdl/el2_exu_div_ctl.sv
	VERILOG_SOURCES += $(PWD)/../hdl/el2_exu_mul_ctl.sv
	VERILOG_SOURCES += $(PWD)/../hdl/el2_ifu.sv
	VERILOG_SOURCES += $(PWD)/../hdl/el2_ifu_aln_ctl.sv
	VERILOG_SOURCES += $(PWD)/../hdl/el2_ifu_bp_ctl.sv
	VERILOG_SOURCES += $(PWD)/../hdl/el2_ifu_compress_ctl.sv
	VERILOG_SOURCES += $(PWD)/../hdl/el2_ifu_iccm_mem.sv
	VERILOG_SOURCES += $(PWD)/../hdl/el2_ifu_ic_mem.sv
	VERILOG_SOURCES += $(PWD)/../hdl/el2_ifu_ifc_ctl.sv
	VERILOG_SOURCES += $(PWD)/../hdl/el2_ifu_mem_ctl.sv
	VERILOG_SOURCES += $(PWD)/../hdl/el2_lib.sv
	VERILOG_SOURCES += $(PWD)/../hdl/el2_lsu.sv
	VERILOG_SOURCES += $(PWD)/../hdl/el2_lsu_addrcheck.sv
	VERILOG_SOURCES += $(PWD)/../hdl/el2_lsu_bus_buffer.sv
	VERILOG_SOURCES += $(PWD)/../hdl/el2_lsu_bus_intf.sv
	VERILOG_SOURCES += $(PWD)/../hdl/el2_lsu_clkdomain.sv
	VERILOG_SOURCES += $(PWD)/../hdl/el2_lsu_dccm_ctl.sv
	VERILOG_SOURCES += $(PWD)/../hdl/el2_lsu_dccm_mem.sv
	VERILOG_SOURCES += $(PWD)/../hdl/el2_lsu_ecc.sv
	VERILOG_SOURCES += $(PWD)/../hdl/el2_lsu_lsc_ctl.sv
	VERILOG_SOURCES += $(PWD)/../hdl/el2_lsu_stbuf.sv
	VERILOG_SOURCES += $(PWD)/../hdl/el2_lsu_trigger.sv
	VERILOG_SOURCES += $(PWD)/../hdl/el2_mem.sv
	VERILOG_SOURCES += $(PWD)/../hdl/el2_pic_ctrl.sv
	VERILOG_SOURCES += $(PWD)/../hdl/el2_swerv.sv
	VERILOG_SOURCES += $(PWD)/../hdl/el2_swerv_wrapper.sv
	VERILOG_SOURCES += $(PWD)/../hdl/mem_lib.sv
	VERILOG_SOURCES += $(PWD)/../hdl/Top.sv
else
    $(error A valid value (verilog or vhdl) was not provided for TOPLEVEL_LANG=$(TOPLEVEL_LANG))
endif

TOPLEVEL := top
MODULE   := TOP

include $(shell cocotb-config --makefiles)/Makefile.sim
