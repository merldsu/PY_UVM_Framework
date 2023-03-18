// Copyright 2023 MERL-DSU

// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at

//    http://www.apache.org/licenses/LICENSE-2.0

// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.



module Instruction_Memory(A,WE,WD,RD,rst,clk);

input logic [31:0] A,WD;
input logic rst,clk;
input logic WE;
output logic [31:0] RD;

//declaration of memory 
 bit [31:0] Instr_Mem [bit[31:0]];

//reding in to the memory 
always @ (posedge clk)
 begin
    if (WE & (~rst))
     begin
     /* verilator lint_off WIDTH */
       Instr_Mem[A[31:2]] <= WD;
     end


 end




assign RD = (~rst) ? {32{1'b0}} :Instr_Mem[A[31:2]];
/* verilator lint_on WIDTH */

endmodule
