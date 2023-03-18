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



module Control_Unit(Op,Zero,Negative,Overflow,Carry,Funct_3,Funct_7,Shift_Type,PCSrc,ResultSrc,MemWrite,ALUSrc,ImmSrc,RegWrite,Finish_Prog,ALUControl,Reg_Read_Enable_1,Reg_Read_Enable_2,Mem_Read_Enable);

input [6:0] Op;
input Zero,Negative,Overflow,Carry;
input [2:0] Funct_3;
input Funct_7,Shift_Type;

output PCSrc,MemWrite,RegWrite,Finish_Prog,Reg_Read_Enable_1,Reg_Read_Enable_2,Mem_Read_Enable;
output [1:0] ALUSrc,ResultSrc;
output [2:0] ImmSrc;
output [3:0] ALUControl;
//interim wires
wire [1:0] ALUOp;

//instantiation of Main decoder in The top module of Control Unit
main_decoder Main_Decoder(
                         .op(Op),
                         .Funct_3(Funct_3),
                         .zero(Zero),
                         .Negative(Negative),
                         .Overflow(Overflow),
                         .Carry(Carry),
                         .Shift_Type(Shift_Type),
                         .PCSrc(PCSrc),                         
                         .RegWrite(RegWrite),
                         .MemWrite(MemWrite),
                         .Mem_Read_Enable(Mem_Read_Enable),
                         .Reg_Read_Enable_1(Reg_Read_Enable_1),
                         .Reg_Read_Enable_2(Reg_Read_Enable_2),
                         .ResultSrc(ResultSrc),
                         .Finish_Prog(Finish_Prog), 
                         .ALUSrc(ALUSrc), 
                         .ImmSrc(ImmSrc), 
                         .ALUOp(ALUOp) 
                         );

//Insantiation of ALU Decoder in the Top module of Control Unit

alu_decoder ALU_Decoder(
                       .ALUOp(ALUOp),
                       .op5(Op[5]),
                       .funct3(Funct_3),
                       .Shift_Type(Shift_Type),
                       .funct7(Funct_7),
                       .ALUControl(ALUControl)                       
                       );




endmodule
