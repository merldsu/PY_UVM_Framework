// Copyright [2023] [MERL-DSU]

// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at

//    http://www.apache.org/licenses/LICENSE-2.0

// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.



module Extender(Imm,ImmSrc,Imm_Extended);

input [24:0] Imm;
input [2:0] ImmSrc;

output [31:0] Imm_Extended;


//extracting the immidiate source from the incoming instruction based in the immsrc sighal
/*
ImmSrc = 001 for S-type(SW to be specific) immidiate Extension of 12 bits.
ImmSrc = 000 for I-type(LW to be specific) immidiate Extension of 12 bits.
ImmSrc = 010 for I-type(Conditional branch instructions to be specific) immidiate Extension of 13 bits.
ImmSrc = 011 for I-type(LUI and AUIPC) immidiate Extension of 20 bits,12 bits ar addeed on LSB side.
ImmSrc = 100 for I-type(JAL) immidiate Extension of 21 bits, sign extended to 32 bits.
*/


assign Imm_Extended = (ImmSrc == 3'b001) ? {{20{Imm[24]}},Imm[24:18],Imm[4:0]} : (ImmSrc == 3'b000) ?  {{20{Imm[24]}},Imm[24:13]} : (ImmSrc == 3'b010) ? {{19{Imm[24]}},Imm[24],Imm[0],Imm[23:18],Imm[4:1],1'b0} : (ImmSrc == 3'b011) ? ({Imm[24:5],{12{1'b0}}}) : (ImmSrc == 3'b100) ?  {{11{Imm[24]}},Imm[24],Imm[12:5],Imm[13],Imm[23:14],1'b0} : (ImmSrc == 3'b101) ? {{27{1'b0}},Imm[17:13]}:  {32{1'b0}};

endmodule
