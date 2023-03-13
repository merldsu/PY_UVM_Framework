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




module Data_Memory(A,WD,WE,RD,Mem_Read_Enable,clk,rst);

input logic [31:0] A,WD;
input logic clk,WE,rst;
input logic Mem_Read_Enable;
output logic [31:0] RD;


 bit [31:0] Data_Mem [bit[31:0]];
integer Addr;


assign RD  = ((~rst) | (WE)) ? {32{1'b0}} : ((Mem_Read_Enable) ? Data_Mem[A] : {32{1'b0}});



always @ (posedge clk)
 begin 
   if (WE)
     begin
       Data_Mem[A] <= WD;
     end 
 end


endmodule
