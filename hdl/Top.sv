// SPDX-License-Identifier: Apache-2.0
// Copyright 2019 Western Digital Corporation or its affiliates.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
module top
import el2_pkg::*;
 #(
parameter el2_param_t pt = 2271'h04840400010040000800000020908200002840004808220A0C848200060210C00000000000000000000000000000000000000000000000000000000000000000000000000000000003FFFFFFFC3FFFFFFFC3FFFFFFFC3FFFFFFFC3FFFFFFFC3FFFFFFFC3FFFFFFFC3FFFFFFFC104020401C213860103C3C01000000400820428042010840830C2010281840200081002108E0C0801004040800C01002100400606810104100C0810084300800E0EE00000001002101800000000000000000000000000000000000000000000000000000000000000000000000000000000007FFFFFFF87FFFFFFF87FFFFFFF87FFFFFFF87FFFFFFF87FFFFFFF87FFFFFFF87FFFFFFF8001080C080820080007806000003C043C04003E02008084021
)
(
   input logic                             clk,
   input logic                             rst_l,
   input logic                             dbg_rst_l,
   input logic                             nmi_int,
   input logic                             preload,


   output logic [31:0]                     trace_rv_i_insn_ip,
   output logic [31:0]                     trace_rv_i_address_ip,
   output logic                            trace_rv_i_valid_ip,
   output logic                            trace_rv_i_exception_ip,
   output logic [4:0]                      trace_rv_i_ecause_ip,
   output logic                            trace_rv_i_interrupt_ip,
   output logic [31:0]                     trace_rv_i_tval_ip,

   // Bus signals
   //-------------------------- LSU AXI signals--------------------------
   // AXI Write Channels
   input logic                             axi_awvalid,
   output  logic                           axi_awready,
   input logic [pt.LSU_BUS_TAG-1:0]        axi_awid,
   input logic [31:0]                      axi_awaddr,
   input logic [3:0]                       axi_awregion,
   input logic [7:0]                       axi_awlen,
   input logic [2:0]                       axi_awsize,
   input logic [1:0]                       axi_awburst,
   input logic                             axi_awlock,
   input logic [3:0]                       axi_awcache,
   input logic [2:0]                       axi_awprot,
   input logic [3:0]                       axi_awqos,

   input logic                             axi_wvalid,
   output  logic                           axi_wready,
   input logic [63:0]                      axi_wdata,
   input logic [7:0]                       axi_wstrb,
   input logic                             axi_wlast,

   output  logic                           axi_bvalid,
   input logic                             axi_bready,
   output  logic [1:0]                     axi_bresp,
   output  logic [2:0]                     axi_bid,

   // AXI Read Channels
   input logic                             axi_arvalid,
   output  logic                           axi_arready,
   input logic [2:0]                       axi_arid,
   input logic [31:0]                      axi_araddr,
   input logic [3:0]                       axi_arregion,
   input logic [7:0]                       axi_arlen,
   input logic [2:0]                       axi_arsize,
   input logic [1:0]                       axi_arburst,
   input logic                             axi_arlock,
   input logic [3:0]                       axi_arcache,
   input logic [2:0]                       axi_arprot,
   input logic [3:0]                       axi_arqos,

   output  logic                           axi_rvalid,
   input logic                             axi_rready,
   output  logic [2:0]                     axi_rid,
   output  logic [63:0]                    axi_rdata,
   output  logic [1:0]                     axi_rresp,
   output  logic                           axi_rlast
);

    logic        [31:0]         reset_vector;
    logic        [31:0]         nmi_vector;
    logic        [31:1]         jtag_id;

    logic        [31:0]         ic_haddr        ;
    logic        [2:0]          ic_hburst       ;
    logic                       ic_hmastlock    ;
    logic        [3:0]          ic_hprot        ;
    logic        [2:0]          ic_hsize        ;
    logic        [1:0]          ic_htrans       ;
    logic                       ic_hwrite       ;
    logic        [63:0]         ic_hrdata       ;
    logic                       ic_hready       ;
    logic                       ic_hresp        ;

    logic        [31:0]         lsu_haddr       ;
    logic        [2:0]          lsu_hburst      ;
    logic                       lsu_hmastlock   ;
    logic        [3:0]          lsu_hprot       ;
    logic        [2:0]          lsu_hsize       ;
    logic        [1:0]          lsu_htrans      ;
    logic                       lsu_hwrite      ;
    logic        [63:0]         lsu_hrdata      ;
    logic        [63:0]         lsu_hwdata      ;
    logic                       lsu_hready      ;
    logic                       lsu_hresp       ;

    logic        [31:0]         sb_haddr        ;
    logic        [2:0]          sb_hburst       ;
    logic                       sb_hmastlock    ;
    logic        [3:0]          sb_hprot        ;
    logic        [2:0]          sb_hsize        ;
    logic        [1:0]          sb_htrans       ;
    logic                       sb_hwrite       ;

    logic        [63:0]         sb_hrdata       ;
    logic        [63:0]         sb_hwdata       ;
    logic                       sb_hready       ;
    logic                       sb_hresp        ;


    logic                       o_debug_mode_status;


    logic                       jtag_tdo;
    logic                       o_cpu_halt_ack;
    logic                       o_cpu_halt_status;
    logic                       o_cpu_run_ack;

    logic                       mailbox_write;
    logic        [63:0]         dma_hrdata       ;
    logic        [63:0]         dma_hwdata       ;
    logic                       dma_hready       ;
    logic                       dma_hresp        ;

    logic                       mpc_debug_halt_req;
    logic                       mpc_debug_run_req;
    logic                       mpc_reset_run_req;
    logic                       mpc_debug_halt_ack;
    logic                       mpc_debug_run_ack;
    logic                       debug_brkpt_status;

    int                         cycleCnt;
    
    wire                        dma_hready_out;
    int                         commit_count;

    logic                       wb_valid;
    logic [4:0]                 wb_dest;
    logic [31:0]                wb_data,store_data;
    logic 			 st_comp;

`ifdef RV_BUILD_AXI4
   //-------------------------- LSU AXI signals--------------------------
   // AXI Write Channels
    wire                        lsu_axi_awvalid;
    wire                        lsu_axi_awready;
    wire [`RV_LSU_BUS_TAG-1:0]  lsu_axi_awid;
    wire [31:0]                 lsu_axi_awaddr;
    wire [3:0]                  lsu_axi_awregion;
    wire [7:0]                  lsu_axi_awlen;
    wire [2:0]                  lsu_axi_awsize;
    wire [1:0]                  lsu_axi_awburst;
    wire                        lsu_axi_awlock;
    wire [3:0]                  lsu_axi_awcache;
    wire [2:0]                  lsu_axi_awprot;
    wire [3:0]                  lsu_axi_awqos;

    wire                        lsu_axi_wvalid;
    wire                        lsu_axi_wready;
    wire [63:0]                 lsu_axi_wdata;
    wire [7:0]                  lsu_axi_wstrb;
    wire                        lsu_axi_wlast;

    wire                        lsu_axi_bvalid;
    wire                        lsu_axi_bready;
    wire [1:0]                  lsu_axi_bresp;
    wire [`RV_LSU_BUS_TAG-1:0]  lsu_axi_bid;

    // AXI Read Channels
    wire                        lsu_axi_arvalid;
    wire                        lsu_axi_arready;
    wire [`RV_LSU_BUS_TAG-1:0]  lsu_axi_arid;
    wire [31:0]                 lsu_axi_araddr;
    wire [3:0]                  lsu_axi_arregion;
    wire [7:0]                  lsu_axi_arlen;
    wire [2:0]                  lsu_axi_arsize;
    wire [1:0]                  lsu_axi_arburst;
    wire                        lsu_axi_arlock;
    wire [3:0]                  lsu_axi_arcache;
    wire [2:0]                  lsu_axi_arprot;
    wire [3:0]                  lsu_axi_arqos;

    wire                        lsu_axi_rvalid;
    wire                        lsu_axi_rready;
    wire [`RV_LSU_BUS_TAG-1:0]  lsu_axi_rid;
    wire [63:0]                 lsu_axi_rdata;
    wire [1:0]                  lsu_axi_rresp;
    wire                        lsu_axi_rlast;

    //-------------------------- IFU AXI signals--------------------------
    // AXI Write Channels
    wire                        ifu_axi_awvalid;
    wire                        ifu_axi_awready;
    wire [`RV_IFU_BUS_TAG-1:0]  ifu_axi_awid;
    wire [31:0]                 ifu_axi_awaddr;
    wire [3:0]                  ifu_axi_awregion;
    wire [7:0]                  ifu_axi_awlen;
    wire [2:0]                  ifu_axi_awsize;
    wire [1:0]                  ifu_axi_awburst;
    wire                        ifu_axi_awlock;
    wire [3:0]                  ifu_axi_awcache;
    wire [2:0]                  ifu_axi_awprot;
    wire [3:0]                  ifu_axi_awqos;

    wire                        ifu_axi_wvalid;
    wire                        ifu_axi_wready;
    wire [63:0]                 ifu_axi_wdata;
    wire [7:0]                  ifu_axi_wstrb;
    wire                        ifu_axi_wlast;

    wire                        ifu_axi_bvalid;
    wire                        ifu_axi_bready;
    wire [1:0]                  ifu_axi_bresp;
    wire [`RV_IFU_BUS_TAG-1:0]  ifu_axi_bid;

    // AXI Read Channels
    wire                        ifu_axi_arvalid;
    wire                        ifu_axi_arready;
    wire [`RV_IFU_BUS_TAG-1:0]  ifu_axi_arid;
    wire [31:0]                 ifu_axi_araddr;
    wire [3:0]                  ifu_axi_arregion;
    wire [7:0]                  ifu_axi_arlen;
    wire [2:0]                  ifu_axi_arsize;
    wire [1:0]                  ifu_axi_arburst;
    wire                        ifu_axi_arlock;
    wire [3:0]                  ifu_axi_arcache;
    wire [2:0]                  ifu_axi_arprot;
    wire [3:0]                  ifu_axi_arqos;

    wire                        ifu_axi_rvalid;
    wire                        ifu_axi_rready;
    wire [`RV_IFU_BUS_TAG-1:0]  ifu_axi_rid;
    wire [63:0]                 ifu_axi_rdata;
    wire [1:0]                  ifu_axi_rresp;
    wire                        ifu_axi_rlast;

    //-------------------------- SB AXI signals--------------------------
    // AXI Write Channels
    wire                        sb_axi_awvalid;
    wire                        sb_axi_awready;
    wire [`RV_SB_BUS_TAG-1:0]   sb_axi_awid;
    wire [31:0]                 sb_axi_awaddr;
    wire [3:0]                  sb_axi_awregion;
    wire [7:0]                  sb_axi_awlen;
    wire [2:0]                  sb_axi_awsize;
    wire [1:0]                  sb_axi_awburst;
    wire                        sb_axi_awlock;
    wire [3:0]                  sb_axi_awcache;
    wire [2:0]                  sb_axi_awprot;
    wire [3:0]                  sb_axi_awqos;

    wire                        sb_axi_wvalid;
    wire                        sb_axi_wready;
    wire [63:0]                 sb_axi_wdata;
    wire [7:0]                  sb_axi_wstrb;
    wire                        sb_axi_wlast;

    wire                        sb_axi_bvalid;
    wire                        sb_axi_bready;
    wire [1:0]                  sb_axi_bresp;
    wire [`RV_SB_BUS_TAG-1:0]   sb_axi_bid;

    // AXI Read Channels
    wire                        sb_axi_arvalid;
    wire                        sb_axi_arready;
    wire [`RV_SB_BUS_TAG-1:0]   sb_axi_arid;
    wire [31:0]                 sb_axi_araddr;
    wire [3:0]                  sb_axi_arregion;
    wire [7:0]                  sb_axi_arlen;
    wire [2:0]                  sb_axi_arsize;
    wire [1:0]                  sb_axi_arburst;
    wire                        sb_axi_arlock;
    wire [3:0]                  sb_axi_arcache;
    wire [2:0]                  sb_axi_arprot;
    wire [3:0]                  sb_axi_arqos;

    wire                        sb_axi_rvalid;
    wire                        sb_axi_rready;
    wire [`RV_SB_BUS_TAG-1:0]   sb_axi_rid;
    wire [63:0]                 sb_axi_rdata;
    wire [1:0]                  sb_axi_rresp;
    wire                        sb_axi_rlast;

   //-------------------------- DMA AXI signals--------------------------
   // AXI Write Channels
    wire                        dma_axi_awvalid;
    wire                        dma_axi_awready;
    wire [`RV_DMA_BUS_TAG-1:0]  dma_axi_awid;
    wire [31:0]                 dma_axi_awaddr;
    wire [2:0]                  dma_axi_awsize;
    wire [2:0]                  dma_axi_awprot;
    wire [7:0]                  dma_axi_awlen;
    wire [1:0]                  dma_axi_awburst;


    wire                        dma_axi_wvalid;
    wire                        dma_axi_wready;
    wire [63:0]                 dma_axi_wdata;
    wire [7:0]                  dma_axi_wstrb;
    wire                        dma_axi_wlast;

    wire                        dma_axi_bvalid;
    wire                        dma_axi_bready;
    wire [1:0]                  dma_axi_bresp;
    wire [`RV_DMA_BUS_TAG-1:0]  dma_axi_bid;

    // AXI Read Channels
    wire                        dma_axi_arvalid;
    wire                        dma_axi_arready;
    wire [`RV_DMA_BUS_TAG-1:0]  dma_axi_arid;
    wire [31:0]                 dma_axi_araddr;
    wire [2:0]                  dma_axi_arsize;
    wire [2:0]                  dma_axi_arprot;
    wire [7:0]                  dma_axi_arlen;
    wire [1:0]                  dma_axi_arburst;

    wire                        dma_axi_rvalid;
    wire                        dma_axi_rready;
    wire [`RV_DMA_BUS_TAG-1:0]  dma_axi_rid;
    wire [63:0]                 dma_axi_rdata;
    wire [1:0]                  dma_axi_rresp;
    wire                        dma_axi_rlast;

    wire                        lmem_axi_arvalid;
    wire                        lmem_axi_arready;

    wire                        lmem_axi_rvalid;
    wire [`RV_LSU_BUS_TAG-1:0]  lmem_axi_rid;
    wire [1:0]                  lmem_axi_rresp;
    wire [63:0]                 lmem_axi_rdata;
    wire                        lmem_axi_rlast;
    wire                        lmem_axi_rready;

    wire                        lmem_axi_awvalid;
    wire                        lmem_axi_awready;

    wire                        lmem_axi_wvalid;
    wire                        lmem_axi_wready;

    wire [1:0]                  lmem_axi_bresp;
    wire                        lmem_axi_bvalid;
    wire [`RV_LSU_BUS_TAG-1:0]  lmem_axi_bid;
    wire                        lmem_axi_bready;

`endif

    string                      abi_reg[32]; // ABI register names
    reg finish_ecall;
    integer el;
    reg [31:0] terminate_count = 0;

    always @(negedge clk) begin
        cycleCnt <= cycleCnt+1;
        
        if(finish_ecall == 1'b1 & terminate_count < 32'h00000005) begin
        	terminate_count <= terminate_count + 1'b1;
        end
        else if (terminate_count == 32'h00000005) begin
        	terminate_count <= 32'h00000000;
        	finish_ecall <= 1'b0;
        	$fclose(el);
        end
        else begin
        	terminate_count <= terminate_count;
        end
	
        // End Of test monitor
        if(trace_rv_i_valid_ip) begin
            if(trace_rv_i_insn_ip == 32'h00000073) begin
            	$display("TEST Finish");
            	$display("\nFinished : minstret = %0d, mcycle = %0d", rvtop.swerv.dec.tlu.minstretl[31:0],rvtop.swerv.dec.tlu.mcyclel[31:0]);
               finish_ecall <= 1'b1;
               //$fclose(el);
            end
        end
    end


    // trace monitor
    always @(posedge clk) begin
        wb_valid  <= rvtop.swerv.dec.dec_i0_wen_r;
        wb_dest   <= rvtop.swerv.dec.dec_i0_waddr_r;
        wb_data   <= rvtop.swerv.dec.dec_i0_wdata_r;
        st_comp   <= rvtop.swerv.lsu.lsu_commit_r;
        store_data <= rvtop.swerv.lsu.store_data_lo_r;
        
        if (trace_rv_i_valid_ip) begin
           commit_count++;
           $fwrite (el, "%10d : %8s 0 %h %h%15s ; %s\n", cycleCnt, $sformatf("#%0d",commit_count),
                        trace_rv_i_address_ip, trace_rv_i_insn_ip,
                        (wb_dest !=0 && wb_valid)?  $sformatf("%s=%h", abi_reg[wb_dest], wb_data) : 
                        (rvtop.swerv.lsu.dccm_wren) ? $sformatf("%s=%h","st", rvtop.swerv.lsu.dccm_wr_data_lo[31:0]) : 
                        ((trace_rv_i_insn_ip[11:7] == 5'h00 & trace_rv_i_insn_ip[6:0] != 7'h23 & trace_rv_i_insn_ip[6:0] != 7'h73 & (((trace_rv_i_insn_ip[6:0] == 7'h33 & trace_rv_i_insn_ip[31:25] == 7'b0000001 & trace_rv_i_insn_ip[14] != 1'b1) | trace_rv_i_insn_ip[6:0] == 7'h37 | trace_rv_i_insn_ip[6:0] == 7'h17 | trace_rv_i_insn_ip[6:0] == 7'h13 | (trace_rv_i_insn_ip[6:0] == 7'h33 & (trace_rv_i_insn_ip[31:25] == 7'b0100000 | trace_rv_i_insn_ip[31:25] == 7'b0000000)))) /* trace_rv_i_insn_ip[6:0] != 7'h03*/ & (/*rvtop.brqrv.lsu.lsu_active != 1'b1 |*/ rvtop.swerv.dec.dec_div_cancel != 1'b1))) /*| (trace_rv_i_insn_ip[11:7] == 5'h00 & trace_rv_i_insn_ip[6:0] != 7'h73)*/? $sformatf("%s=%h", abi_reg[wb_dest], 32'h00000000) : 
                        (trace_rv_i_insn_ip[11:7] == 5'h00 & trace_rv_i_insn_ip[6:0] == 7'h03 & rvtop.swerv.lsu.lsu_active == 1'b1 /*& rvtop.brqrv.dec.dec_div_cancel == 1'b1*/) ? $sformatf("%s=%h", abi_reg[wb_dest], 32'h00000000) : "             ", 
                        "");
        end
        if(rvtop.swerv.dec.dec_nonblock_load_wen)
           $fwrite (el, "%10d : %32s=%h ; nbL\n", cycleCnt, abi_reg[rvtop.swerv.dec.dec_nonblock_load_waddr], rvtop.swerv.dec.lsu_nonblock_load_data);
        if(rvtop.swerv.dec.decode.lsu_nonblock_load_data_valid & (~rvtop.swerv.dec.dec_nonblock_load_wen))
           $fwrite (el, "%10d : %32s=%h ; nbL+1\n", cycleCnt, abi_reg[rvtop.swerv.dec.dec_nonblock_load_waddr], rvtop.swerv.dec.lsu_nonblock_load_data);
        if(rvtop.swerv.dec.exu_div_wren | (rvtop.swerv.dec.dec_div_cancel))
           $fwrite (el, "%10d : %32s=%h ; nbD+%h\n", cycleCnt, abi_reg[rvtop.swerv.dec.div_waddr_wb], rvtop.swerv.dec.exu_div_result, rvtop.swerv.dec.dec_div_cancel);
        //if(rvtop.swerv.lsu.lsu_active & rvtop.swerv.lsu.lsu_axi_wvalid)
         //$fwrite (el, "%10d : %33s=%h ; nbS\n", cycleCnt, " st", (|rvtop.swerv.lsu.lsu_axi_wstrb[3:0]) ? rvtop.swerv.lsu.lsu_axi_wdata[31:0] : rvtop.swerv.lsu.lsu_axi_wdata[63:32]);
        if(st_comp & trace_rv_i_insn_ip[6:0] == 7'h23)
         $fwrite (el, "%10d : %33s=%h ; nbS\n", cycleCnt, " st", store_data);
        if(trace_rv_i_valid_ip & trace_rv_i_insn_ip[11:7] == 5'h00 & trace_rv_i_insn_ip[6:0] == 7'h73)
         $fwrite (el, "%10d : %33s=%h ; csr\n", cycleCnt, " rm", 32'h00000000);
           
    end
    


    initial begin
        abi_reg[0] = "zero";
        abi_reg[1] = "ra";
        abi_reg[2] = "sp";
        abi_reg[3] = "gp";
        abi_reg[4] = "tp";
        abi_reg[5] = "t0";
        abi_reg[6] = "t1";
        abi_reg[7] = "t2";
        abi_reg[8] = "s0";
        abi_reg[9] = "s1";
        abi_reg[10] = "a0";
        abi_reg[11] = "a1";
        abi_reg[12] = "a2";
        abi_reg[13] = "a3";
        abi_reg[14] = "a4";
        abi_reg[15] = "a5";
        abi_reg[16] = "a6";
        abi_reg[17] = "a7";
        abi_reg[18] = "s2";
        abi_reg[19] = "s3";
        abi_reg[20] = "s4";
        abi_reg[21] = "s5";
        abi_reg[22] = "s6";
        abi_reg[23] = "s7";
        abi_reg[24] = "s8";
        abi_reg[25] = "s9";
        abi_reg[26] = "s10";
        abi_reg[27] = "s11";
        abi_reg[28] = "t3";
        abi_reg[29] = "t4";
        abi_reg[30] = "t5";
        abi_reg[31] = "t6";
    // tie offs
        jtag_id[31:28] = 4'b1;
        jtag_id[27:12] = '0;
        jtag_id[11:1]  = 11'h45;
        reset_vector = `RV_RESET_VEC;
        nmi_vector   = 32'hee000000;

        el = $fopen("exec.log","w");
        $fwrite (el, "//   Cycle : #inst    0    pc    opcode    reg=value   ; mnemonic\n");
        commit_count = 0;
    end
	



   //=========================================================================-
   // RTL instance
   //=========================================================================-
el2_swerv_wrapper rvtop (
    .rst_l                  ( rst_l         ),
    .dbg_rst_l              ( dbg_rst_l       ),
    .clk                    ( clk           ),
    .rst_vec                ( reset_vector[31:1]),
    .nmi_int                ( nmi_int       ),
    .nmi_vec                ( nmi_vector[31:1]),
    .jtag_id                ( jtag_id[31:1]),

`ifdef RV_BUILD_AHB_LITE
    .haddr                  ( ic_haddr      ),
    .hburst                 ( ic_hburst     ),
    .hmastlock              ( ic_hmastlock  ),
    .hprot                  ( ic_hprot      ),
    .hsize                  ( ic_hsize      ),
    .htrans                 ( ic_htrans     ),
    .hwrite                 ( ic_hwrite     ),

    .hrdata                 ( ic_hrdata[63:0]),
    .hready                 ( ic_hready     ),
    .hresp                  ( ic_hresp      ),

    //---------------------------------------------------------------
    // Debug AHB Master
    //---------------------------------------------------------------
    .sb_haddr               ( sb_haddr      ),
    .sb_hburst              ( sb_hburst     ),
    .sb_hmastlock           ( sb_hmastlock  ),
    .sb_hprot               ( sb_hprot      ),
    .sb_hsize               ( sb_hsize      ),
    .sb_htrans              ( sb_htrans     ),
    .sb_hwrite              ( sb_hwrite     ),
    .sb_hwdata              ( sb_hwdata     ),

    .sb_hrdata              ( sb_hrdata     ),
    .sb_hready              ( sb_hready     ),
    .sb_hresp               ( sb_hresp      ),

    //---------------------------------------------------------------
    // LSU AHB Master
    //---------------------------------------------------------------
    .lsu_haddr              ( lsu_haddr       ),
    .lsu_hburst             ( lsu_hburst      ),
    .lsu_hmastlock          ( lsu_hmastlock   ),
    .lsu_hprot              ( lsu_hprot       ),
    .lsu_hsize              ( lsu_hsize       ),
    .lsu_htrans             ( lsu_htrans      ),
    .lsu_hwrite             ( lsu_hwrite      ),
    .lsu_hwdata             ( lsu_hwdata      ),

    .lsu_hrdata             ( lsu_hrdata[63:0]),
    .lsu_hready             ( lsu_hready      ),
    .lsu_hresp              ( lsu_hresp       ),

    //---------------------------------------------------------------
    // DMA Slave
    //---------------------------------------------------------------
    .dma_haddr              ( '0 ),
    .dma_hburst             ( '0 ),
    .dma_hmastlock          ( '0 ),
    .dma_hprot              ( '0 ),
    .dma_hsize              ( '0 ),
    .dma_htrans             ( '0 ),
    .dma_hwrite             ( '0 ),
    .dma_hwdata             ( '0 ),

    .dma_hrdata             ( dma_hrdata    ),
    .dma_hresp              ( dma_hresp     ),
    .dma_hsel               ( 1'b1            ),
    .dma_hreadyin           ( dma_hready_out  ),
    .dma_hreadyout          ( dma_hready_out  ),
`endif
`ifdef RV_BUILD_AXI4
    //-------------------------- LSU AXI signals--------------------------
    // AXI Write Channels
    .lsu_axi_awvalid        (lsu_axi_awvalid),
    .lsu_axi_awready        (lsu_axi_awready),
    .lsu_axi_awid           (lsu_axi_awid),
    .lsu_axi_awaddr         (lsu_axi_awaddr),
    .lsu_axi_awregion       (lsu_axi_awregion),
    .lsu_axi_awlen          (lsu_axi_awlen),
    .lsu_axi_awsize         (lsu_axi_awsize),
    .lsu_axi_awburst        (lsu_axi_awburst),
    .lsu_axi_awlock         (lsu_axi_awlock),
    .lsu_axi_awcache        (lsu_axi_awcache),
    .lsu_axi_awprot         (lsu_axi_awprot),
    .lsu_axi_awqos          (lsu_axi_awqos),

    .lsu_axi_wvalid         (lsu_axi_wvalid),
    .lsu_axi_wready         (lsu_axi_wready),
    .lsu_axi_wdata          (lsu_axi_wdata),
    .lsu_axi_wstrb          (lsu_axi_wstrb),
    .lsu_axi_wlast          (lsu_axi_wlast),

    .lsu_axi_bvalid         (lsu_axi_bvalid),
    .lsu_axi_bready         (lsu_axi_bready),
    .lsu_axi_bresp          (lsu_axi_bresp),
    .lsu_axi_bid            (lsu_axi_bid),


    .lsu_axi_arvalid        (lsu_axi_arvalid),
    .lsu_axi_arready        (lsu_axi_arready),
    .lsu_axi_arid           (lsu_axi_arid),
    .lsu_axi_araddr         (lsu_axi_araddr),
    .lsu_axi_arregion       (lsu_axi_arregion),
    .lsu_axi_arlen          (lsu_axi_arlen),
    .lsu_axi_arsize         (lsu_axi_arsize),
    .lsu_axi_arburst        (lsu_axi_arburst),
    .lsu_axi_arlock         (lsu_axi_arlock),
    .lsu_axi_arcache        (lsu_axi_arcache),
    .lsu_axi_arprot         (lsu_axi_arprot),
    .lsu_axi_arqos          (lsu_axi_arqos),

    .lsu_axi_rvalid         (lsu_axi_rvalid),
    .lsu_axi_rready         (lsu_axi_rready),
    .lsu_axi_rid            (lsu_axi_rid),
    .lsu_axi_rdata          (lsu_axi_rdata),
    .lsu_axi_rresp          (lsu_axi_rresp),
    .lsu_axi_rlast          (lsu_axi_rlast),

    //-------------------------- IFU AXI signals--------------------------
    // AXI Write Channels
    .ifu_axi_awvalid        (ifu_axi_awvalid),
    .ifu_axi_awready        (ifu_axi_awready),
    .ifu_axi_awid           (ifu_axi_awid),
    .ifu_axi_awaddr         (ifu_axi_awaddr),
    .ifu_axi_awregion       (ifu_axi_awregion),
    .ifu_axi_awlen          (ifu_axi_awlen),
    .ifu_axi_awsize         (ifu_axi_awsize),
    .ifu_axi_awburst        (ifu_axi_awburst),
    .ifu_axi_awlock         (ifu_axi_awlock),
    .ifu_axi_awcache        (ifu_axi_awcache),
    .ifu_axi_awprot         (ifu_axi_awprot),
    .ifu_axi_awqos          (ifu_axi_awqos),

    .ifu_axi_wvalid         (ifu_axi_wvalid),
    .ifu_axi_wready         (ifu_axi_wready),
    .ifu_axi_wdata          (ifu_axi_wdata),
    .ifu_axi_wstrb          (ifu_axi_wstrb),
    .ifu_axi_wlast          (ifu_axi_wlast),

    .ifu_axi_bvalid         (ifu_axi_bvalid),
    .ifu_axi_bready         (ifu_axi_bready),
    .ifu_axi_bresp          (ifu_axi_bresp),
    .ifu_axi_bid            (ifu_axi_bid),

    .ifu_axi_arvalid        (ifu_axi_arvalid),
    .ifu_axi_arready        (ifu_axi_arready),
    .ifu_axi_arid           (ifu_axi_arid),
    .ifu_axi_araddr         (ifu_axi_araddr),
    .ifu_axi_arregion       (ifu_axi_arregion),
    .ifu_axi_arlen          (ifu_axi_arlen),
    .ifu_axi_arsize         (ifu_axi_arsize),
    .ifu_axi_arburst        (ifu_axi_arburst),
    .ifu_axi_arlock         (ifu_axi_arlock),
    .ifu_axi_arcache        (ifu_axi_arcache),
    .ifu_axi_arprot         (ifu_axi_arprot),
    .ifu_axi_arqos          (ifu_axi_arqos),

    .ifu_axi_rvalid         (ifu_axi_rvalid),
    .ifu_axi_rready         (ifu_axi_rready),
    .ifu_axi_rid            (ifu_axi_rid),
    .ifu_axi_rdata          (ifu_axi_rdata),
    .ifu_axi_rresp          (ifu_axi_rresp),
    .ifu_axi_rlast          (ifu_axi_rlast),

    //-------------------------- SB AXI signals--------------------------
    // AXI Write Channels
    .sb_axi_awvalid         (sb_axi_awvalid),
    .sb_axi_awready         (sb_axi_awready),
    .sb_axi_awid            (sb_axi_awid),
    .sb_axi_awaddr          (sb_axi_awaddr),
    .sb_axi_awregion        (sb_axi_awregion),
    .sb_axi_awlen           (sb_axi_awlen),
    .sb_axi_awsize          (sb_axi_awsize),
    .sb_axi_awburst         (sb_axi_awburst),
    .sb_axi_awlock          (sb_axi_awlock),
    .sb_axi_awcache         (sb_axi_awcache),
    .sb_axi_awprot          (sb_axi_awprot),
    .sb_axi_awqos           (sb_axi_awqos),

    .sb_axi_wvalid          (sb_axi_wvalid),
    .sb_axi_wready          (sb_axi_wready),
    .sb_axi_wdata           (sb_axi_wdata),
    .sb_axi_wstrb           (sb_axi_wstrb),
    .sb_axi_wlast           (sb_axi_wlast),

    .sb_axi_bvalid          (sb_axi_bvalid),
    .sb_axi_bready          (sb_axi_bready),
    .sb_axi_bresp           (sb_axi_bresp),
    .sb_axi_bid             (sb_axi_bid),


    .sb_axi_arvalid         (sb_axi_arvalid),
    .sb_axi_arready         (sb_axi_arready),
    .sb_axi_arid            (sb_axi_arid),
    .sb_axi_araddr          (sb_axi_araddr),
    .sb_axi_arregion        (sb_axi_arregion),
    .sb_axi_arlen           (sb_axi_arlen),
    .sb_axi_arsize          (sb_axi_arsize),
    .sb_axi_arburst         (sb_axi_arburst),
    .sb_axi_arlock          (sb_axi_arlock),
    .sb_axi_arcache         (sb_axi_arcache),
    .sb_axi_arprot          (sb_axi_arprot),
    .sb_axi_arqos           (sb_axi_arqos),

    .sb_axi_rvalid          (sb_axi_rvalid),
    .sb_axi_rready          (sb_axi_rready),
    .sb_axi_rid             (sb_axi_rid),
    .sb_axi_rdata           (sb_axi_rdata),
    .sb_axi_rresp           (sb_axi_rresp),
    .sb_axi_rlast           (sb_axi_rlast),

    //-------------------------- DMA AXI signals--------------------------
    // AXI Write Channels
    .dma_axi_awvalid        (dma_axi_awvalid),
    .dma_axi_awready        (dma_axi_awready),
    .dma_axi_awid           ('0),
    .dma_axi_awaddr         (lsu_axi_awaddr),
    .dma_axi_awsize         (lsu_axi_awsize),
    .dma_axi_awprot         (lsu_axi_awprot),
    .dma_axi_awlen          (lsu_axi_awlen),
    .dma_axi_awburst        (lsu_axi_awburst),


    .dma_axi_wvalid         (dma_axi_wvalid),
    .dma_axi_wready         (dma_axi_wready),
    .dma_axi_wdata          (lsu_axi_wdata),
    .dma_axi_wstrb          (lsu_axi_wstrb),
    .dma_axi_wlast          (lsu_axi_wlast),

    .dma_axi_bvalid         (dma_axi_bvalid),
    .dma_axi_bready         (dma_axi_bready),
    .dma_axi_bresp          (dma_axi_bresp),
    .dma_axi_bid            (),


    .dma_axi_arvalid        (dma_axi_arvalid),
    .dma_axi_arready        (dma_axi_arready),
    .dma_axi_arid           ('0),
    .dma_axi_araddr         (lsu_axi_araddr),
    .dma_axi_arsize         (lsu_axi_arsize),
    .dma_axi_arprot         (lsu_axi_arprot),
    .dma_axi_arlen          (lsu_axi_arlen),
    .dma_axi_arburst        (lsu_axi_arburst),

    .dma_axi_rvalid         (dma_axi_rvalid),
    .dma_axi_rready         (dma_axi_rready),
    .dma_axi_rid            (),
    .dma_axi_rdata          (dma_axi_rdata),
    .dma_axi_rresp          (dma_axi_rresp),
    .dma_axi_rlast          (dma_axi_rlast),
`endif
    .timer_int              ( 1'b0     ),
    .extintsrc_req          ( '0  ),

    .lsu_bus_clk_en         ( 1'b1  ),// Clock ratio b/w cpu core clk & AHB master interface
    .ifu_bus_clk_en         ( 1'b1  ),// Clock ratio b/w cpu core clk & AHB master interface
    .dbg_bus_clk_en         ( 1'b1  ),// Clock ratio b/w cpu core clk & AHB Debug master interface
    .dma_bus_clk_en         ( 1'b1  ),// Clock ratio b/w cpu core clk & AHB slave interface

    .trace_rv_i_insn_ip     (trace_rv_i_insn_ip),
    .trace_rv_i_address_ip  (trace_rv_i_address_ip),
    .trace_rv_i_valid_ip    (trace_rv_i_valid_ip),
    .trace_rv_i_exception_ip(trace_rv_i_exception_ip),
    .trace_rv_i_ecause_ip   (trace_rv_i_ecause_ip),
    .trace_rv_i_interrupt_ip(trace_rv_i_interrupt_ip),
    .trace_rv_i_tval_ip     (trace_rv_i_tval_ip),

    .jtag_tck               ( 1'b0  ),
    .jtag_tms               ( 1'b0  ),
    .jtag_tdi               ( 1'b0  ),
    .jtag_trst_n            ( 1'b0  ),
    .jtag_tdo               ( jtag_tdo ),

    .mpc_debug_halt_ack     ( mpc_debug_halt_ack),
    .mpc_debug_halt_req     ( 1'b0),
    .mpc_debug_run_ack      ( mpc_debug_run_ack),
    .mpc_debug_run_req      ( 1'b1),
    .mpc_reset_run_req      ( 1'b1),             // Start running after reset
     .debug_brkpt_status    (debug_brkpt_status),

    .i_cpu_halt_req         ( 1'b0  ),    // Async halt req to CPU
    .o_cpu_halt_ack         ( o_cpu_halt_ack ),    // core response to halt
    .o_cpu_halt_status      ( o_cpu_halt_status ), // 1'b1 indicates core is halted
    .i_cpu_run_req          ( 1'b0  ),     // Async restart req to CPU
    .o_debug_mode_status    (o_debug_mode_status),
    .o_cpu_run_ack          ( o_cpu_run_ack ),     // Core response to run req

    .dec_tlu_perfcnt0       (),
    .dec_tlu_perfcnt1       (),
    .dec_tlu_perfcnt2       (),
    .dec_tlu_perfcnt3       (),

// remove mems DFT pins for opensource
    .dccm_ext_in_pkt        ('0),
    .iccm_ext_in_pkt        ('0),
    .ic_data_ext_in_pkt     ('0),
    .ic_tag_ext_in_pkt      ('0),

    .soft_int               ('0),
    .core_id                ('0),
    .scan_mode              ( 1'b0 ),         // To enable scan mode
    .mbist_mode             ( 1'b0 )        // to enable mbist

);

// Output assignment
assign axi_arready = (preload & axi_araddr <= 32'h80000000) ? ifu_axi_arready : (preload & axi_araddr > 32'h80000000) ? lsu_axi_arready : '0;
assign axi_rvalid =  (preload & axi_araddr <= 32'h80000000) ? ifu_axi_rvalid  : (preload & axi_araddr > 32'h80000000) ? lsu_axi_rvalid  : '0;
assign axi_rdata =   (preload & axi_araddr <= 32'h80000000) ? ifu_axi_rdata   : (preload & axi_araddr > 32'h80000000) ? lsu_axi_rdata   : '0;
assign axi_rresp =   (preload & axi_araddr <= 32'h80000000) ? ifu_axi_rresp   : (preload & axi_araddr > 32'h80000000) ? lsu_axi_rresp   : '0;
assign axi_rid   =   (preload & axi_araddr <= 32'h80000000) ? ifu_axi_rid     : (preload & axi_araddr > 32'h80000000) ? lsu_axi_rid     : '0;
assign axi_rlast =   (preload & axi_araddr <= 32'h80000000) ? ifu_axi_rlast   : (preload & axi_araddr > 32'h80000000) ? lsu_axi_rlast   : '0;
assign axi_awready = (preload & axi_awaddr <= 32'h80000000) ? ifu_axi_awready : (preload & axi_awaddr > 32'h80000000) ? lsu_axi_awready : '0;
assign axi_wready =  (preload & axi_awaddr <= 32'h80000000) ? ifu_axi_wready  : (preload & axi_awaddr > 32'h80000000) ? lsu_axi_wready  : '0;
assign axi_bvalid =  (preload & axi_awaddr <= 32'h80000000) ? ifu_axi_bvalid  : (preload & axi_awaddr > 32'h80000000) ? lsu_axi_bvalid  : '0;
assign axi_bresp =   (preload & axi_awaddr <= 32'h80000000) ? ifu_axi_bresp   : (preload & axi_awaddr > 32'h80000000) ? lsu_axi_bresp   : '0;
assign axi_bid   =   (preload & axi_awaddr <= 32'h80000000) ? ifu_axi_bid     : (preload & axi_awaddr > 32'h80000000) ? lsu_axi_bid     : '0;

// External Memories
axi_slv #(.TAGW(`RV_IFU_BUS_TAG)) imem(
    .aclk(clk),
    .rst_l(dbg_rst_l),
    .arvalid((preload) ? axi_arvalid : ifu_axi_arvalid),
    .arready(ifu_axi_arready),
    .araddr((preload) ? axi_araddr : ifu_axi_araddr),
    .arid((preload) ? axi_arid : ifu_axi_arid),
    .arlen((preload) ? axi_arlen : ifu_axi_arlen),
    .arburst((preload) ? axi_arburst : ifu_axi_arburst),
    .arsize((preload) ? axi_arsize : ifu_axi_arsize),

    .rvalid(ifu_axi_rvalid),
    .rready((preload) ? axi_rready : ifu_axi_rready),
    .rdata(ifu_axi_rdata),
    .rresp(ifu_axi_rresp),
    .rid(ifu_axi_rid),
    .rlast(ifu_axi_rlast),

    .awvalid((preload) ? axi_awvalid : ifu_axi_awvalid),
    .awready(ifu_axi_awready),
    .awaddr((preload) ? axi_awaddr : ifu_axi_awaddr),
    .awid((preload) ? axi_awid : ifu_axi_awid),
    .awlen((preload) ? axi_awlen : ifu_axi_awlen),
    .awburst((preload) ? axi_awburst : ifu_axi_awburst),
    .awsize((preload) ? axi_awsize : ifu_axi_awsize),

    .wdata((preload) ? axi_wdata : ifu_axi_wdata),
    .wstrb((preload) ? axi_wstrb : ifu_axi_wstrb),
    .wvalid((preload) ? axi_wvalid : ifu_axi_wvalid),
    .wready(ifu_axi_wready),

    .bvalid(ifu_axi_bvalid),
    .bready((preload) ? axi_bready : ifu_axi_bready),
    .bresp(ifu_axi_bresp),
    .bid(ifu_axi_bid)
);

defparam lmem.TAGW =`RV_LSU_BUS_TAG;

axi_slv  lmem(
    .aclk(clk),
    .rst_l(dbg_rst_l),
    .arvalid((preload) ? axi_arvalid : lsu_axi_arvalid),
    .arready(lsu_axi_arready),
    .araddr((preload) ? axi_araddr : lsu_axi_araddr),
    .arid((preload) ? axi_arid : lsu_axi_arid),
    .arlen((preload) ? axi_arlen : lsu_axi_arlen),
    .arburst((preload) ? axi_arburst : lsu_axi_arburst),
    .arsize((preload) ? axi_arsize : lsu_axi_arsize),

    .rvalid(lsu_axi_rvalid),
    .rready((preload) ? axi_rready : lsu_axi_rready),
    .rdata(lsu_axi_rdata),
    .rresp(lsu_axi_rresp),
    .rid(lsu_axi_rid),
    .rlast(lsu_axi_rlast),

    .awvalid((preload) ? axi_awvalid : lsu_axi_awvalid),
    .awready(lsu_axi_awready),
    .awaddr((preload) ? axi_awaddr : lsu_axi_awaddr),
    .awid((preload) ? axi_awid : lsu_axi_awid),
    .awlen((preload) ? axi_awlen : lsu_axi_awlen),
    .awburst((preload) ? axi_awburst : lsu_axi_awburst),
    .awsize((preload) ? axi_awsize : lsu_axi_awsize),

    .wdata((preload) ? axi_wdata : lsu_axi_wdata),
    .wstrb((preload) ? axi_wstrb : lsu_axi_wstrb),
    .wvalid((preload) ? axi_wvalid : lsu_axi_wvalid),
    .wready(lsu_axi_wready),

    .bvalid(lsu_axi_bvalid),
    .bready((preload) ? axi_bready : lsu_axi_bready),
    .bresp(lsu_axi_bresp),
    .bid(lsu_axi_bid)
);

/*axi_lsu_dma_bridge # (`RV_LSU_BUS_TAG,`RV_LSU_BUS_TAG ) bridge(
    .clk(core_clk),
    .reset_l(dbg_rst_l),

    .m_arvalid(lsu_axi_arvalid),
    .m_arid(lsu_axi_arid),
    .m_araddr(lsu_axi_araddr),
    .m_arready(lsu_axi_arready),

    .m_rvalid(lsu_axi_rvalid),
    .m_rready(lsu_axi_rready),
    .m_rdata(lsu_axi_rdata),
    .m_rid(lsu_axi_rid),
    .m_rresp(lsu_axi_rresp),
    .m_rlast(lsu_axi_rlast),

    .m_awvalid(lsu_axi_awvalid),
    .m_awid(lsu_axi_awid),
    .m_awaddr(lsu_axi_awaddr),
    .m_awready(lsu_axi_awready),

    .m_wvalid(lsu_axi_wvalid),
    .m_wready(lsu_axi_wready),

    .m_bresp(lsu_axi_bresp),
    .m_bvalid(lsu_axi_bvalid),
    .m_bid(lsu_axi_bid),
    .m_bready(lsu_axi_bready),

    .s0_arvalid(lmem_axi_arvalid),
    .s0_arready(lmem_axi_arready),

    .s0_rvalid(lmem_axi_rvalid),
    .s0_rid(lmem_axi_rid),
    .s0_rresp(lmem_axi_rresp),
    .s0_rdata(lmem_axi_rdata),
    .s0_rlast(lmem_axi_rlast),
    .s0_rready(lmem_axi_rready),

    .s0_awvalid(lmem_axi_awvalid),
    .s0_awready(lmem_axi_awready),

    .s0_wvalid(lmem_axi_wvalid),
    .s0_wready(lmem_axi_wready),

    .s0_bresp(lmem_axi_bresp),
    .s0_bvalid(lmem_axi_bvalid),
    .s0_bid(lmem_axi_bid),
    .s0_bready(lmem_axi_bready),


    .s1_arvalid(dma_axi_arvalid),
    .s1_arready(dma_axi_arready),

    .s1_rvalid(dma_axi_rvalid),
    .s1_rresp(dma_axi_rresp),
    .s1_rdata(dma_axi_rdata),
    .s1_rlast(dma_axi_rlast),
    .s1_rready(dma_axi_rready),

    .s1_awvalid(dma_axi_awvalid),
    .s1_awready(dma_axi_awready),

    .s1_wvalid(dma_axi_wvalid),
    .s1_wready(dma_axi_wready),

    .s1_bresp(dma_axi_bresp),
    .s1_bvalid(dma_axi_bvalid),
    .s1_bready(dma_axi_bready)
);
*/

/*
`include "dasm.svi"
*/
endmodule