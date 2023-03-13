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


module Register_File(A1,RD1,Reg_Read_Enable_1,A2,RD2,Reg_Read_Enable_2,A3,WD3,WE3,clk,rst);

input [4:0] A1,A2,A3;
input Reg_Read_Enable_1,Reg_Read_Enable_2;
input [31:0] WD3;
input WE3,clk,rst;

output [31:0] RD1,RD2;

reg [31:0] Register_File_MEM [31:0];

//reading from register File
assign RD1 = ((~rst) | (~Reg_Read_Enable_1)) ? {32{1'b0}} : Register_File_MEM[A1];
assign RD2 = ((~rst) | (~Reg_Read_Enable_2)) ? {32{1'b0}} : Register_File_MEM[A2]; 

//writing on the register File
always @ (posedge clk)
 begin

  /*In case of deactivated global reste the register file stores the data coming on to WD3 port in the address given on A3 address port.
    if the desired write addres is Zero the data is not saved in the register file*/  
  if (rst)
     begin
      if (WE3 & (~(&(~A3))) )
         begin
          Register_File_MEM[A3] <= WD3;
         end
     end

  //Reseting the reg file on the occurance of gobal reset
  else
     begin
          Register_File_MEM[0] <= {32{1'b0}};
          Register_File_MEM[1] <= {32{1'b0}}; 
          Register_File_MEM[2] <= {32{1'b0}}; 
          Register_File_MEM[3] <= {32{1'b0}}; 
          Register_File_MEM[4] <= {32{1'b0}}; 
          Register_File_MEM[5] <= {32{1'b0}}; 
          Register_File_MEM[6] <= {32{1'b0}};           
          Register_File_MEM[7] <= {32{1'b0}}; 
          Register_File_MEM[8] <= {32{1'b0}};           
          Register_File_MEM[9] <= {32{1'b0}}; 
          Register_File_MEM[10] <= {32{1'b0}};           
          Register_File_MEM[11] <= {32{1'b0}}; 
          Register_File_MEM[12] <= {32{1'b0}}; 
          Register_File_MEM[13] <= {32{1'b0}}; 
          Register_File_MEM[14] <= {32{1'b0}}; 
          Register_File_MEM[15] <= {32{1'b0}}; 
          Register_File_MEM[16] <= {32{1'b0}}; 
          Register_File_MEM[17] <= {32{1'b0}}; 
          Register_File_MEM[18] <= {32{1'b0}}; 
          Register_File_MEM[19] <= {32{1'b0}}; 
          Register_File_MEM[20] <= {32{1'b0}}; 
          Register_File_MEM[21] <= {32{1'b0}}; 
          Register_File_MEM[22] <= {32{1'b0}}; 
          Register_File_MEM[23] <= {32{1'b0}}; 
          Register_File_MEM[24] <= {32{1'b0}}; 
          Register_File_MEM[25] <= {32{1'b0}}; 
          Register_File_MEM[26] <= {32{1'b0}}; 
          Register_File_MEM[27] <= {32{1'b0}}; 
          Register_File_MEM[28] <= {32{1'b0}}; 
          Register_File_MEM[29] <= {32{1'b0}}; 
          Register_File_MEM[30] <= {32{1'b0}}; 
          Register_File_MEM[31] <= {32{1'b0}}; 
     end    
 end

endmodule

