// SPDX-License-Identifier: Apache-2.0
// Copyright 2020 Western Digital Corporation or its affiliates.
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


module el2_exu_mul_ctl
import el2_pkg::*;
#(parameter el2_param_t pt = 2271'h04840400010040000800000020908200002840004808220A0C848200060210C00000000000000000000000000000000000000000000000000000000000000000000000000000000003FFFFFFFC3FFFFFFFC3FFFFFFFC3FFFFFFFC3FFFFFFFC3FFFFFFFC3FFFFFFFC3FFFFFFFC104020401C213860103C3C01000000400820428042010840830C2010281840200081002108E0C0801004040800C01002100400606810104100C0810084300800E0EE00000001002101800000000000000000000000000000000000000000000000000000000000000000000000000000000007FFFFFFF87FFFFFFF87FFFFFFF87FFFFFFF87FFFFFFF87FFFFFFF87FFFFFFF87FFFFFFF8001080C080820080007806000003C043C04003E02008084021
 )
  (
   input logic          clk,              // Top level clock
   input logic          rst_l,            // Reset
   input logic          scan_mode,        // Scan mode

   input el2_mul_pkt_t mul_p,            // {Valid, RS1 signed operand, RS2 signed operand, Select low 32-bits of result}

   input logic [31:0]   rs1_in,           // A operand
   input logic [31:0]   rs2_in,           // B operand


   output logic [31:0]  result_x          // Result
  );


   logic                mul_x_enable;
   logic                bit_x_enable;
   logic signed [32:0]  rs1_ext_in;
   logic signed [32:0]  rs2_ext_in;
   logic        [65:0]  prod_x;
   logic                low_x;



   // *** Start - BitManip ***

   logic                bitmanip_sel_d;
   logic                bitmanip_sel_x;
   logic        [31:0]  bitmanip_d;
   logic        [31:0]  bitmanip_x;



   // ZBE
   logic                ap_bext;
   logic                ap_bdep;

   // ZBC
   logic                ap_clmul;
   logic                ap_clmulh;
   logic                ap_clmulr;

   // ZBP
   logic                ap_grev;
   logic                ap_gorc;
   logic                ap_shfl;
   logic                ap_unshfl;

   // ZBR
   logic                ap_crc32_b;
   logic                ap_crc32_h;
   logic                ap_crc32_w;
   logic                ap_crc32c_b;
   logic                ap_crc32c_h;
   logic                ap_crc32c_w;

   // ZBF
   logic                ap_bfp;


   if (pt.BITMANIP_ZBE == 1)
     begin
       assign ap_bext         =  mul_p.bext;
       assign ap_bdep         =  mul_p.bdep;
     end
   else
     begin
       assign ap_bext         =  1'b0;
       assign ap_bdep         =  1'b0;
     end

   if (pt.BITMANIP_ZBC == 1)
     begin
       assign ap_clmul        =  mul_p.clmul;
       assign ap_clmulh       =  mul_p.clmulh;
       assign ap_clmulr       =  mul_p.clmulr;
     end
   else
     begin
       assign ap_clmul        =  1'b0;
       assign ap_clmulh       =  1'b0;
       assign ap_clmulr       =  1'b0;
     end

   if (pt.BITMANIP_ZBP == 1)
     begin
       assign ap_grev         =  mul_p.grev;
       assign ap_gorc         =  mul_p.gorc;
       assign ap_shfl         =  mul_p.shfl;
       assign ap_unshfl       =  mul_p.unshfl;
     end
   else
     begin
       assign ap_grev         =  1'b0;
       assign ap_gorc         =  1'b0;
       assign ap_shfl         =  1'b0;
       assign ap_unshfl       =  1'b0;
     end

   if (pt.BITMANIP_ZBR == 1)
     begin
       assign ap_crc32_b      =  mul_p.crc32_b;
       assign ap_crc32_h      =  mul_p.crc32_h;
       assign ap_crc32_w      =  mul_p.crc32_w;
       assign ap_crc32c_b     =  mul_p.crc32c_b;
       assign ap_crc32c_h     =  mul_p.crc32c_h;
       assign ap_crc32c_w     =  mul_p.crc32c_w;
     end
   else
     begin
       assign ap_crc32_b      =  1'b0;
       assign ap_crc32_h      =  1'b0;
       assign ap_crc32_w      =  1'b0;
       assign ap_crc32c_b     =  1'b0;
       assign ap_crc32c_h     =  1'b0;
       assign ap_crc32c_w     =  1'b0;
     end

   if (pt.BITMANIP_ZBF == 1)
     begin
       assign ap_bfp          =  mul_p.bfp;
     end
   else
     begin
       assign ap_bfp          =  1'b0;
     end


   // *** End   - BitManip ***



   assign mul_x_enable           =  mul_p.valid;
   assign bit_x_enable           =  mul_p.valid;

   assign rs1_ext_in[32]         =  mul_p.rs1_sign & rs1_in[31];
   assign rs2_ext_in[32]         =  mul_p.rs2_sign & rs2_in[31];

   assign rs1_ext_in[31:0]       =  rs1_in[31:0];
   assign rs2_ext_in[31:0]       =  rs2_in[31:0];



   // --------------------------- Multiply       ----------------------------------


   logic signed [32:0]  rs1_x;
   logic signed [32:0]  rs2_x;

   rvdffe #(34) i_a_x_ff         (.*, .clk(clk),  .din({mul_p.low,rs1_ext_in[32:0]}),        .dout({low_x,rs1_x[32:0]}),                 .en(mul_x_enable));
   rvdffe #(33) i_b_x_ff         (.*, .clk(clk),  .din(           rs2_ext_in[32:0] ),        .dout(       rs2_x[32:0] ),                 .en(mul_x_enable));


   assign prod_x[65:0]           =  rs1_x  *  rs2_x;


   // * * * * * * * * * * * * * * * * * *  BitManip  :  BEXT, BDEP   * * * * * * * * * * * * * * * * * *


   // *** BEXT == "gather"  ***

   logic        [31:0]    bext_d;
   logic                  bext_test_bit_d;
   integer                bext_i, bext_j;


   always_comb
     begin

       bext_j                    =      0;
       bext_test_bit_d           =   1'b0;
       bext_d[31:0]              =  32'b0;

       for (bext_i=0; bext_i<32; bext_i++)
         begin
             bext_test_bit_d     =  rs2_in[bext_i];
             if (bext_test_bit_d)
               begin
                  bext_d[bext_j] =  rs1_in[bext_i];
                  bext_j         =  bext_j + 1;
               end  // IF  bext_test_bit
         end        // FOR bext_i
     end            // ALWAYS_COMB



   // *** BDEP == "scatter" ***

   logic        [31:0]    bdep_d;
   logic                  bdep_test_bit_d;
   integer                bdep_i, bdep_j;


   always_comb
     begin

       bdep_j                    =      0;
       bdep_test_bit_d           =   1'b0;
       bdep_d[31:0]              =  32'b0;

       for (bdep_i=0; bdep_i<32; bdep_i++)
         begin
             bdep_test_bit_d     =  rs2_in[bdep_i];
             if (bdep_test_bit_d)
               begin
                  bdep_d[bdep_i] =  rs1_in[bdep_j];
                  bdep_j         =  bdep_j + 1;
               end  // IF  bdep_test_bit
         end        // FOR bdep_i
     end            // ALWAYS_COMB




   // * * * * * * * * * * * * * * * * * *  BitManip  :  CLMUL, CLMULH, CLMULR  * * * * * * * * * * * * *

   logic        [62:0]    clmul_raw_d;


   assign clmul_raw_d[62:0]      = ( {63{rs2_in[00]}} & {31'b0,rs1_in[31:0]      } ) ^
                                   ( {63{rs2_in[01]}} & {30'b0,rs1_in[31:0], 1'b0} ) ^
                                   ( {63{rs2_in[02]}} & {29'b0,rs1_in[31:0], 2'b0} ) ^
                                   ( {63{rs2_in[03]}} & {28'b0,rs1_in[31:0], 3'b0} ) ^
                                   ( {63{rs2_in[04]}} & {27'b0,rs1_in[31:0], 4'b0} ) ^
                                   ( {63{rs2_in[05]}} & {26'b0,rs1_in[31:0], 5'b0} ) ^
                                   ( {63{rs2_in[06]}} & {25'b0,rs1_in[31:0], 6'b0} ) ^
                                   ( {63{rs2_in[07]}} & {24'b0,rs1_in[31:0], 7'b0} ) ^
                                   ( {63{rs2_in[08]}} & {23'b0,rs1_in[31:0], 8'b0} ) ^
                                   ( {63{rs2_in[09]}} & {22'b0,rs1_in[31:0], 9'b0} ) ^
                                   ( {63{rs2_in[10]}} & {21'b0,rs1_in[31:0],10'b0} ) ^
                                   ( {63{rs2_in[11]}} & {20'b0,rs1_in[31:0],11'b0} ) ^
                                   ( {63{rs2_in[12]}} & {19'b0,rs1_in[31:0],12'b0} ) ^
                                   ( {63{rs2_in[13]}} & {18'b0,rs1_in[31:0],13'b0} ) ^
                                   ( {63{rs2_in[14]}} & {17'b0,rs1_in[31:0],14'b0} ) ^
                                   ( {63{rs2_in[15]}} & {16'b0,rs1_in[31:0],15'b0} ) ^
                                   ( {63{rs2_in[16]}} & {15'b0,rs1_in[31:0],16'b0} ) ^
                                   ( {63{rs2_in[17]}} & {14'b0,rs1_in[31:0],17'b0} ) ^
                                   ( {63{rs2_in[18]}} & {13'b0,rs1_in[31:0],18'b0} ) ^
                                   ( {63{rs2_in[19]}} & {12'b0,rs1_in[31:0],19'b0} ) ^
                                   ( {63{rs2_in[20]}} & {11'b0,rs1_in[31:0],20'b0} ) ^
                                   ( {63{rs2_in[21]}} & {10'b0,rs1_in[31:0],21'b0} ) ^
                                   ( {63{rs2_in[22]}} & { 9'b0,rs1_in[31:0],22'b0} ) ^
                                   ( {63{rs2_in[23]}} & { 8'b0,rs1_in[31:0],23'b0} ) ^
                                   ( {63{rs2_in[24]}} & { 7'b0,rs1_in[31:0],24'b0} ) ^
                                   ( {63{rs2_in[25]}} & { 6'b0,rs1_in[31:0],25'b0} ) ^
                                   ( {63{rs2_in[26]}} & { 5'b0,rs1_in[31:0],26'b0} ) ^
                                   ( {63{rs2_in[27]}} & { 4'b0,rs1_in[31:0],27'b0} ) ^
                                   ( {63{rs2_in[28]}} & { 3'b0,rs1_in[31:0],28'b0} ) ^
                                   ( {63{rs2_in[29]}} & { 2'b0,rs1_in[31:0],29'b0} ) ^
                                   ( {63{rs2_in[30]}} & { 1'b0,rs1_in[31:0],30'b0} ) ^
                                   ( {63{rs2_in[31]}} & {      rs1_in[31:0],31'b0} );




   // * * * * * * * * * * * * * * * * * *  BitManip  :  GREV         * * * * * * * * * * * * * * * * * *

   // uint32_t grev32(uint32_t rs1, uint32_t rs2)
   // {
   //     uint32_t x = rs1;
   //     int shamt = rs2 & 31;
   //
   //     if (shamt &  1)  x = ( (x & 0x55555555) <<  1) | ( (x & 0xAAAAAAAA) >>  1);
   //     if (shamt &  2)  x = ( (x & 0x33333333) <<  2) | ( (x & 0xCCCCCCCC) >>  2);
   //     if (shamt &  4)  x = ( (x & 0x0F0F0F0F) <<  4) | ( (x & 0xF0F0F0F0) >>  4);
   //     if (shamt &  8)  x = ( (x & 0x00FF00FF) <<  8) | ( (x & 0xFF00FF00) >>  8);
   //     if (shamt & 16)  x = ( (x & 0x0000FFFF) << 16) | ( (x & 0xFFFF0000) >> 16);
   //
   //     return x;
   //  }


   logic        [31:0]    grev1_d;
   logic        [31:0]    grev2_d;
   logic        [31:0]    grev4_d;
   logic        [31:0]    grev8_d;
   logic        [31:0]    grev_d;


   assign grev1_d[31:0]       = (rs2_in[0])  ?  {rs1_in[30],rs1_in[31],rs1_in[28],rs1_in[29],rs1_in[26],rs1_in[27],rs1_in[24],rs1_in[25],
                                                 rs1_in[22],rs1_in[23],rs1_in[20],rs1_in[21],rs1_in[18],rs1_in[19],rs1_in[16],rs1_in[17],
                                                 rs1_in[14],rs1_in[15],rs1_in[12],rs1_in[13],rs1_in[10],rs1_in[11],rs1_in[08],rs1_in[09],
                                                 rs1_in[06],rs1_in[07],rs1_in[04],rs1_in[05],rs1_in[02],rs1_in[03],rs1_in[00],rs1_in[01]}  :  rs1_in[31:0];

   assign grev2_d[31:0]       = (rs2_in[1])  ?  {grev1_d[29:28],grev1_d[31:30],grev1_d[25:24],grev1_d[27:26],
                                                 grev1_d[21:20],grev1_d[23:22],grev1_d[17:16],grev1_d[19:18],
                                                 grev1_d[13:12],grev1_d[15:14],grev1_d[09:08],grev1_d[11:10],
                                                 grev1_d[05:04],grev1_d[07:06],grev1_d[01:00],grev1_d[03:02]}  :  grev1_d[31:0];

   assign grev4_d[31:0]       = (rs2_in[2])  ?  {grev2_d[27:24],grev2_d[31:28],grev2_d[19:16],grev2_d[23:20],
                                                 grev2_d[11:08],grev2_d[15:12],grev2_d[03:00],grev2_d[07:04]}  :  grev2_d[31:0];

   assign grev8_d[31:0]       = (rs2_in[3])  ?  {grev4_d[23:16],grev4_d[31:24],grev4_d[07:00],grev4_d[15:08]}  :  grev4_d[31:0];

   assign grev_d[31:0]        = (rs2_in[4])  ?  {grev8_d[15:00],grev8_d[31:16]}  :  grev8_d[31:0];




   // * * * * * * * * * * * * * * * * * *  BitManip  :  GORC         * * * * * * * * * * * * * * * * * *

   // uint32_t gorc32(uint32_t rs1, uint32_t rs2)
   // {
   //     uint32_t x = rs1;
   //     int shamt = rs2 & 31;
   //
   //     if (shamt &  1)  x |= ( (x & 0x55555555) <<  1) | ( (x & 0xAAAAAAAA) >>  1);
   //     if (shamt &  2)  x |= ( (x & 0x33333333) <<  2) | ( (x & 0xCCCCCCCC) >>  2);
   //     if (shamt &  4)  x |= ( (x & 0x0F0F0F0F) <<  4) | ( (x & 0xF0F0F0F0) >>  4);
   //     if (shamt &  8)  x |= ( (x & 0x00FF00FF) <<  8) | ( (x & 0xFF00FF00) >>  8);
   //     if (shamt & 16)  x |= ( (x & 0x0000FFFF) << 16) | ( (x & 0xFFFF0000) >> 16);
   //
   //     return x;
   //  }


   logic        [31:0]    gorc1_d;
   logic        [31:0]    gorc2_d;
   logic        [31:0]    gorc4_d;
   logic        [31:0]    gorc8_d;
   logic        [31:0]    gorc_d;


   assign gorc1_d[31:0]       = ( {32{rs2_in[0]}} & {rs1_in[30],rs1_in[31],rs1_in[28],rs1_in[29],rs1_in[26],rs1_in[27],rs1_in[24],rs1_in[25],
                                                     rs1_in[22],rs1_in[23],rs1_in[20],rs1_in[21],rs1_in[18],rs1_in[19],rs1_in[16],rs1_in[17],
                                                     rs1_in[14],rs1_in[15],rs1_in[12],rs1_in[13],rs1_in[10],rs1_in[11],rs1_in[08],rs1_in[09],
                                                     rs1_in[06],rs1_in[07],rs1_in[04],rs1_in[05],rs1_in[02],rs1_in[03],rs1_in[00],rs1_in[01]} ) | rs1_in[31:0];

   assign gorc2_d[31:0]       = ( {32{rs2_in[1]}} & {gorc1_d[29:28],gorc1_d[31:30],gorc1_d[25:24],gorc1_d[27:26],
                                                     gorc1_d[21:20],gorc1_d[23:22],gorc1_d[17:16],gorc1_d[19:18],
                                                     gorc1_d[13:12],gorc1_d[15:14],gorc1_d[09:08],gorc1_d[11:10],
                                                     gorc1_d[05:04],gorc1_d[07:06],gorc1_d[01:00],gorc1_d[03:02]} ) | gorc1_d[31:0];

   assign gorc4_d[31:0]       = ( {32{rs2_in[2]}} & {gorc2_d[27:24],gorc2_d[31:28],gorc2_d[19:16],gorc2_d[23:20],
                                                     gorc2_d[11:08],gorc2_d[15:12],gorc2_d[03:00],gorc2_d[07:04]} ) | gorc2_d[31:0];

   assign gorc8_d[31:0]       = ( {32{rs2_in[3]}} & {gorc4_d[23:16],gorc4_d[31:24],gorc4_d[07:00],gorc4_d[15:08]} ) | gorc4_d[31:0];

   assign gorc_d[31:0]        = ( {32{rs2_in[4]}} & {gorc8_d[15:00],gorc8_d[31:16]} ) | gorc8_d[31:0];




   // * * * * * * * * * * * * * * * * * *  BitManip  :  SHFL, UNSHLF * * * * * * * * * * * * * * * * * *

   // uint32_t shuffle32_stage (uint32_t src, uint32_t maskL, uint32_t maskR, int N)
   // {
   //     uint32_t x  = src & ~(maskL | maskR);
   //     x          |= ((src << N) & maskL) | ((src >> N) & maskR);
   //     return x;
   // }
   //
   //
   //
   // uint32_t shfl32(uint32_t rs1, uint32_t rs2)
   // {
   //     uint32_t x = rs1;
   //     int shamt = rs2 & 15
   //
   //     if (shamt & 8)  x = shuffle32_stage(x, 0x00ff0000, 0x0000ff00, 8);
   //     if (shamt & 4)  x = shuffle32_stage(x, 0x0f000f00, 0x00f000f0, 4);
   //     if (shamt & 2)  x = shuffle32_stage(x, 0x30303030, 0xc0c0c0c0, 2);
   //     if (shamt & 1)  x = shuffle32_stage(x, 0x44444444, 0x22222222, 1);
   //
   //     return x;
   // }


   logic        [31:0]    shfl8_d;
   logic        [31:0]    shfl4_d;
   logic        [31:0]    shfl2_d;
   logic        [31:0]    shfl_d;



   assign shfl8_d[31:0]       = (rs2_in[3])  ?  {rs1_in[31:24],rs1_in[15:08],rs1_in[23:16],rs1_in[07:00]}      :  rs1_in[31:0];

   assign shfl4_d[31:0]       = (rs2_in[2])  ?  {shfl8_d[31:28],shfl8_d[23:20],shfl8_d[27:24],shfl8_d[19:16],
                                                 shfl8_d[15:12],shfl8_d[07:04],shfl8_d[11:08],shfl8_d[03:00]}  :  shfl8_d[31:0];

   assign shfl2_d[31:0]       = (rs2_in[1])  ?  {shfl4_d[31:30],shfl4_d[27:26],shfl4_d[29:28],shfl4_d[25:24],
                                                 shfl4_d[23:22],shfl4_d[19:18],shfl4_d[21:20],shfl4_d[17:16],
                                                 shfl4_d[15:14],shfl4_d[11:10],shfl4_d[13:12],shfl4_d[09:08],
                                                 shfl4_d[07:06],shfl4_d[03:02],shfl4_d[05:04],shfl4_d[01:00]}  :  shfl4_d[31:0];

   assign shfl_d[31:0]        = (rs2_in[0])  ?  {shfl2_d[31],shfl2_d[29],shfl2_d[30],shfl2_d[28],shfl2_d[27],shfl2_d[25],shfl2_d[26],shfl2_d[24],
                                                 shfl2_d[23],shfl2_d[21],shfl2_d[22],shfl2_d[20],shfl2_d[19],shfl2_d[17],shfl2_d[18],shfl2_d[16],
                                                 shfl2_d[15],shfl2_d[13],shfl2_d[14],shfl2_d[12],shfl2_d[11],shfl2_d[09],shfl2_d[10],shfl2_d[08],
                                                 shfl2_d[07],shfl2_d[05],shfl2_d[06],shfl2_d[04],shfl2_d[03],shfl2_d[01],shfl2_d[02],shfl2_d[00]}  :  shfl2_d[31:0];




   // uint32_t unshfl32(uint32_t rs1, uint32_t rs2)
   // {
   //     uint32_t x = rs1;
   //     int shamt = rs2 & 15
   //
   //     if (shamt & 1)  x = shuffle32_stage(x, 0x44444444, 0x22222222, 1);
   //     if (shamt & 2)  x = shuffle32_stage(x, 0x30303030, 0xc0c0c0c0, 2);
   //     if (shamt & 4)  x = shuffle32_stage(x, 0x0f000f00, 0x00f000f0, 4);
   //     if (shamt & 8)  x = shuffle32_stage(x, 0x00ff0000, 0x0000ff00, 8);
   //
   //     return x;
   // }


   logic        [31:0]    unshfl1_d;
   logic        [31:0]    unshfl2_d;
   logic        [31:0]    unshfl4_d;
   logic        [31:0]    unshfl_d;


   assign unshfl1_d[31:0]     = (rs2_in[0])  ?  {rs1_in[31],rs1_in[29],rs1_in[30],rs1_in[28],rs1_in[27],rs1_in[25],rs1_in[26],rs1_in[24],
                                                 rs1_in[23],rs1_in[21],rs1_in[22],rs1_in[20],rs1_in[19],rs1_in[17],rs1_in[18],rs1_in[16],
                                                 rs1_in[15],rs1_in[13],rs1_in[14],rs1_in[12],rs1_in[11],rs1_in[09],rs1_in[10],rs1_in[08],
                                                 rs1_in[07],rs1_in[05],rs1_in[06],rs1_in[04],rs1_in[03],rs1_in[01],rs1_in[02],rs1_in[00]}  :  rs1_in[31:0];

   assign unshfl2_d[31:0]     = (rs2_in[1])  ?  {unshfl1_d[31:30],unshfl1_d[27:26],unshfl1_d[29:28],unshfl1_d[25:24],
                                                 unshfl1_d[23:22],unshfl1_d[19:18],unshfl1_d[21:20],unshfl1_d[17:16],
                                                 unshfl1_d[15:14],unshfl1_d[11:10],unshfl1_d[13:12],unshfl1_d[09:08],
                                                 unshfl1_d[07:06],unshfl1_d[03:02],unshfl1_d[05:04],unshfl1_d[01:00]}  :  unshfl1_d[31:0];

   assign unshfl4_d[31:0]     = (rs2_in[2])  ?  {unshfl2_d[31:28],unshfl2_d[23:20],unshfl2_d[27:24],unshfl2_d[19:16],
                                                 unshfl2_d[15:12],unshfl2_d[07:04],unshfl2_d[11:08],unshfl2_d[03:00]}  :  unshfl2_d[31:0];

   assign unshfl_d[31:0]      = (rs2_in[3])  ?  {unshfl4_d[31:24],unshfl4_d[15:08],unshfl4_d[23:16],unshfl4_d[07:00]}  :  unshfl4_d[31:0];




   // * * * * * * * * * * * * * * * * * *  BitManip  :  CRC32, CRC32c  * * * * * * * * * * * * * * * * *

   // ***  computed from   https: //crccalc.com  ***
   //
   // "a" is 8'h61 = 8'b0110_0001    (8'h61 ^ 8'hff = 8'h9e)
   //
   // Input must first be XORed with 32'hffff_ffff
   //
   //
   // CRC32
   //
   // Input    Output        Input      Output
   // -----   --------      --------   --------
   // "a"     e8b7be43      ffffff9e   174841bc
   // "aa"    078a19d7      ffff9e9e   f875e628
   // "aaaa"  ad98e545      9e9e9e9e   5267a1ba
   //
   //
   //
   // CRC32c
   //
   // Input    Output        Input      Output
   // -----   --------      --------   --------
   // "a"     c1d04330      ffffff9e   3e2fbccf
   // "aa"    f1f2dac2      ffff9e9e   0e0d253d
   // "aaaa"  6a52eeb0      9e9e9e9e   95ad114f


   logic                  crc32_all;
   logic        [31:0]    crc32_poly_rev;
   logic        [31:0]    crc32c_poly_rev;
   integer                crc32_bi, crc32_hi, crc32_wi, crc32c_bi, crc32c_hi, crc32c_wi;
   logic        [31:0]    crc32_bd, crc32_hd, crc32_wd, crc32c_bd, crc32c_hd, crc32c_wd;


   assign crc32_all              =  ap_crc32_b  | ap_crc32_h  | ap_crc32_w | ap_crc32c_b | ap_crc32c_h | ap_crc32c_w;

   assign crc32_poly_rev[31:0]   =  32'hEDB88320;    // bit reverse of 32'h04C11DB7
   assign crc32c_poly_rev[31:0]  =  32'h82F63B78;    // bit reverse of 32'h1EDC6F41


   always_comb
     begin
       crc32_bd[31:0]            =  rs1_in[31:0];

       for (crc32_bi=0; crc32_bi<8; crc32_bi++)
         begin
            crc32_bd[31:0] = (crc32_bd[31:0] >> 1) ^ (crc32_poly_rev[31:0] & {32{crc32_bd[0]}});
         end      // FOR    crc32_bi
     end          // ALWAYS_COMB


   always_comb
     begin
       crc32_hd[31:0]            =  rs1_in[31:0];

       for (crc32_hi=0; crc32_hi<16; crc32_hi++)
         begin
            crc32_hd[31:0] = (crc32_hd[31:0] >> 1) ^ (crc32_poly_rev[31:0] & {32{crc32_hd[0]}});
         end      // FOR    crc32_hi
     end          // ALWAYS_COMB


   always_comb
     begin
       crc32_wd[31:0]            =  rs1_in[31:0];

       for (crc32_wi=0; crc32_wi<32; crc32_wi++)
         begin
            crc32_wd[31:0] = (crc32_wd[31:0] >> 1) ^ (crc32_poly_rev[31:0] & {32{crc32_wd[0]}});
         end      // FOR    crc32_wi
     end          // ALWAYS_COMB




   always_comb
     begin
       crc32c_bd[31:0]           =  rs1_in[31:0];

       for (crc32c_bi=0; crc32c_bi<8; crc32c_bi++)
         begin
            crc32c_bd[31:0] = (crc32c_bd[31:0] >> 1) ^ (crc32c_poly_rev[31:0] & {32{crc32c_bd[0]}});
         end      // FOR    crc32c_bi
     end          // ALWAYS_COMB


   always_comb
     begin
       crc32c_hd[31:0]           =  rs1_in[31:0];

       for (crc32c_hi=0; crc32c_hi<16; crc32c_hi++)
         begin
            crc32c_hd[31:0] = (crc32c_hd[31:0] >> 1) ^ (crc32c_poly_rev[31:0] & {32{crc32c_hd[0]}});
         end      // FOR    crc32c_hi
     end          // ALWAYS_COMB


   always_comb
     begin
       crc32c_wd[31:0]           =  rs1_in[31:0];

       for (crc32c_wi=0; crc32c_wi<32; crc32c_wi++)
         begin
            crc32c_wd[31:0] = (crc32c_wd[31:0] >> 1) ^ (crc32c_poly_rev[31:0] & {32{crc32c_wd[0]}});
         end      // FOR    crc32c_wi
     end          // ALWAYS_COMB





   // * * * * * * * * * * * * * * * * * *  BitManip  :  BFP          * * * * * * * * * * * * * * * * * *

   logic        [4:0]     bfp_len;
   logic        [4:0]     bfp_off;
   logic        [31:0]    bfp_len_mask_;
   logic        [15:0]    bfp_preshift_data;
   logic        [63:0]    bfp_shift_data;
   logic        [63:0]    bfp_shift_mask;
   logic        [31:0]    bfp_result_d;


   assign bfp_len[3:0]           =  rs2_in[27:24];
   assign bfp_len[4]             = (bfp_len[3:0] == 4'b0);   // If LEN field is zero, then LEN=16
   assign bfp_off[4:0]           =  rs2_in[20:16];

   assign bfp_len_mask_[31:0]    =  32'hffff_ffff  <<  bfp_len[4:0];
   assign bfp_preshift_data[15:0]=  rs2_in[15:0] & ~bfp_len_mask_[15:0];

   assign bfp_shift_data[63:0]   = {16'b0,bfp_preshift_data[15:0], 16'b0,bfp_preshift_data[15:0]}  <<  bfp_off[4:0];
   assign bfp_shift_mask[63:0]   = {bfp_len_mask_[31:0],           bfp_len_mask_[31:0]}            <<  bfp_off[4:0];

   assign bfp_result_d[31:0]     = bfp_shift_data[63:32] | (rs1_in[31:0] & bfp_shift_mask[63:32]);





   // * * * * * * * * * * * * * * * * * *  BitManip  :  Common logic * * * * * * * * * * * * * * * * * *


   assign bitmanip_sel_d         =  ap_bext | ap_bdep | ap_clmul | ap_clmulh | ap_clmulr | ap_grev | ap_gorc | ap_shfl | ap_unshfl | crc32_all | ap_bfp;

   assign bitmanip_d[31:0]       = ( {32{ap_bext}}     &       bext_d[31:0]        ) |
                                   ( {32{ap_bdep}}     &       bdep_d[31:0]        ) |
                                   ( {32{ap_clmul}}    &       clmul_raw_d[31:0]   ) |
                                   ( {32{ap_clmulh}}   & {1'b0,clmul_raw_d[62:32]} ) |
                                   ( {32{ap_clmulr}}   &       clmul_raw_d[62:31]  ) |
                                   ( {32{ap_grev}}     &       grev_d[31:0]        ) |
                                   ( {32{ap_gorc}}     &       gorc_d[31:0]        ) |
                                   ( {32{ap_shfl}}     &       shfl_d[31:0]        ) |
                                   ( {32{ap_unshfl}}   &       unshfl_d[31:0]      ) |
                                   ( {32{ap_crc32_b}}  &       crc32_bd[31:0]      ) |
                                   ( {32{ap_crc32_h}}  &       crc32_hd[31:0]      ) |
                                   ( {32{ap_crc32_w}}  &       crc32_wd[31:0]      ) |
                                   ( {32{ap_crc32c_b}} &       crc32c_bd[31:0]     ) |
                                   ( {32{ap_crc32c_h}} &       crc32c_hd[31:0]     ) |
                                   ( {32{ap_crc32c_w}} &       crc32c_wd[31:0]     ) |
                                   ( {32{ap_bfp}}      &       bfp_result_d[31:0]  );



   rvdffe #(33) i_bitmanip_ff    (.*, .clk(clk),  .din({bitmanip_sel_d,bitmanip_d[31:0]}),   .dout({bitmanip_sel_x,bitmanip_x[31:0]}),   .en(bit_x_enable));




   assign result_x[31:0]         =  ( {32{~bitmanip_sel_x & ~low_x}} & prod_x[63:32]    ) |
                                    ( {32{~bitmanip_sel_x &  low_x}} & prod_x[31:0]     ) |
                                                                       bitmanip_x[31:0];



endmodule  // el2_exu_mul_ctl
