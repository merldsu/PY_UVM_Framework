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




// `include "Adder.v"
// `include "Program_Counter.v"
// `include "Instruction_Memory.v"
// `include "ALU_Decoder.v"
// `include "Main_Decoder.v"
// `include "Control_Unit.v"
// `include "Extension.v"
// `include "Result_Extension.v"
// `include "ALU.v"
// `include "Register_File.v"
// `include "Data_Memory.v"


module CORE(clk,rst,Instruction_Write_Enable,Instruction_Write,Instruction_Address,Data_write_Data,Data_write_Address,Finish_Prog,Instruction_cmnd_Monitor,Instruction_Address_cmd_Monitor,Instruction_result_Monitor,Instruction_Address_result_Monitor,Result_result_Monitor);

input clk,rst,Instruction_Write_Enable;
input [31:0] Instruction_Write,Instruction_Address,Data_write_Data,Data_write_Address;

output Finish_Prog;
output [31:0] Instruction_cmnd_Monitor,Instruction_Address_cmd_Monitor,Instruction_result_Monitor,Instruction_Address_result_Monitor,Result_result_Monitor;


wire [31:0] PC_Core,PC_Next_Routine,PC_Next,PC_Next_Branch,Input_B_Adder_Jump;
wire [31:0] Current_Instr,Instr_Memory_adrress_Input;
wire PCSrc_Core,MemWrite_Core,RegWrite_Core,Reg_Read_Enable_1_Core,Reg_Read_Enable_2_Core,Mem_Read_Enable_Core;
wire [1:0] ALUSrc_Core,ResultSrc_Core;
wire [2:0] ImmSrc_Core;
wire [3:0] ALUControl_Core;
wire [31:0] Extended_Imm_Core;
wire [31:0] Input_Result_Extension,Output_Result_Extension;
wire [31:0] Source_Register_1,Source_Register_2;
wire [31:0] Destination_Register;
wire [31:0] ALU_Result,ALU_Src_2,ALU_Src_1;
wire Zero_Flag_ALU,Negative_Flag_ALU,Overflow_Flag_ALU,Carry_Flag_ALU;
wire [31:0] ReadData_Core,Data_Memory_Write_Port,Data_Memory_Address_Port;

//Instantiation of Program Counter
assign PC_Next = (PCSrc_Core) ? PC_Next_Branch : PC_Next_Routine; 

Program_Counter Program_Counter(
                               .PC_Next(PC_Next),
                               .PC(PC_Core),
                               .clk(clk),
                               .rst(rst)
                               );

//Instantiation of Adder Module for routine PC + 4
Adder Adder_PC_Routine (
                        .Input_A(PC_Core),
                        .Input_B({{28{1'b0}},4'b0100}),
                        .ImmSrc (),
                        .Output_A(PC_Next_Routine)
                       );

//Instantiation of Adder Module for Jump Pc + imm, this is the same module ofr all instructions involving jumps. weather conditional or unconditional.

assign Input_B_Adder_Jump = (ImmSrc_Core == 3'b000) ? ALU_Result : Extended_Imm_Core;

Adder Adder_PC_Core_Jump (
                      .Input_A(PC_Core),
                      .Input_B (Input_B_Adder_Jump),
                      .ImmSrc(ImmSrc_Core),
                      .Output_A(PC_Next_Branch)
);

//instatiation of Instruction memory
assign Instr_Memory_adrress_Input = (Instruction_Write_Enable) ? Instruction_Address : PC_Core ;
Instruction_Memory Inst_Memory(
                               .A(Instr_Memory_adrress_Input),                               
                               .WE(Instruction_Write_Enable),
                               .WD(Instruction_Write),
                               .rst(rst),
                               .clk(clk),
                               .RD(Current_Instr)
                               );
                               

//instantiation of Control Unit 

Control_Unit Control_Unit(
              .Op(Current_Instr[6:0]),
              .Zero(Zero_Flag_ALU),
              .Negative(Negative_Flag_ALU),
              .Overflow(Overflow_Flag_ALU),
              .Carry(Carry_Flag_ALU),
              .Funct_3(Current_Instr[14:12]),
              .Funct_7(Current_Instr[30]),
              .Shift_Type(Current_Instr[30]),
              .Reg_Read_Enable_1(Reg_Read_Enable_1_Core),
              .Reg_Read_Enable_2(Reg_Read_Enable_2_Core),
              .Mem_Read_Enable(Mem_Read_Enable_Core),
              .PCSrc(PCSrc_Core),
              .ResultSrc(ResultSrc_Core),
              .MemWrite(MemWrite_Core),
              .ALUSrc(ALUSrc_Core),
              .ImmSrc(ImmSrc_Core),
              .RegWrite(RegWrite_Core),
              .ALUControl(ALUControl_Core),
              .Finish_Prog(Finish_Prog)
              );

//instantiation of Extender Block

Extender Extender_Block(
                        .Imm (Current_Instr[31:7]), //Sending the whole current instruction except for opcode feild to the extender block 
                        .ImmSrc(ImmSrc_Core),       //The immidiate source from the instruction would be determined via IMMSrc contor signal 
                        .Imm_Extended(Extended_Imm_Core) //The xtended output for ALU operations.
                        );



//instantiating Register File 

// assign Destination_Register = (ResultSrc_Core == 2'b01) ? ReadData_Core : (ResultSrc_Core == 2'b10) ? PC_Next_Routine : ALU_Result ;
assign Destination_Register = Output_Result_Extension;

Register_File Register_File(
                            .A1(Current_Instr[19:15]),
                            .RD1(Source_Register_1),
                            .Reg_Read_Enable_1(Reg_Read_Enable_1_Core),
                            .A2(Current_Instr[24:20]),
                            .RD2(Source_Register_2),
                            .Reg_Read_Enable_2(Reg_Read_Enable_2_Core),
                            .A3(Current_Instr[11:7]),
                            .WD3(Destination_Register),
                            .WE3(RegWrite_Core),
                            .clk(clk),
                            .rst(rst)
                            );

//instantiaintg Extender Bloxk. This extender block is used to incorprate the desired extension in LB,LH,SB,SH instructions. 
//If the incoming instruction is not one of these then the this block acts like a buffer. In architcture the extender block is placed after the ResultSRC mux.
// The output of the extender goes to the Register file's write data port.                            

assign Input_Result_Extension = (MemWrite_Core) ? Source_Register_2 : ((ResultSrc_Core == 2'b01) ? ReadData_Core : (ResultSrc_Core == 2'b10) ? PC_Next_Routine : ALU_Result) ; 
Result_Extender Result_Extension_Block (
                                        .Result_Un_Extended(Input_Result_Extension),
                                        .Load_Instr(Mem_Read_Enable_Core),
                                        .Store_Instr(MemWrite_Core),
                                        .Funct_3(Current_Instr[14:12]),
                                        .Resukt_Extended(Output_Result_Extension)
);


//Inhstantiating ALU 

assign ALU_Src_1 = (ALUSrc_Core[0]) ? PC_Core : Source_Register_1 ;
assign ALU_Src_2 = (ALUSrc_Core[1]) ? Extended_Imm_Core : Source_Register_2 ;

alu Arthemetic_Logic_Unit(
                          .A(ALU_Src_1),
                          .B(ALU_Src_2),
                          .ALUControl(ALUControl_Core),
                          .Result(ALU_Result),
                          .Z(Zero_Flag_ALU),
                          .N(Negative_Flag_ALU),
                          .V(Overflow_Flag_ALU),
                          .C(Carry_Flag_ALU)
                          );

//instantiaating Data Memory
assign Data_Memory_Write_Port = (rst) ? Output_Result_Extension : Data_write_Data ;
assign Data_Memory_Address_Port = (rst) ? ALU_Result : Data_write_Address;

Data_Memory Data_MEM (
                      .A(Data_Memory_Address_Port),
                      .WD(Data_Memory_Write_Port),
                      .Mem_Read_Enable(Mem_Read_Enable_Core),
                      .WE(MemWrite_Core | (~rst) ),
                      .RD(ReadData_Core),
                      .clk(clk),
                      .rst(rst)
                      );

assign Instruction_cmnd_Monitor = Instruction_Write;
assign Instruction_Address_cmd_Monitor = Instruction_Address ;

assign Instruction_result_Monitor = Current_Instr;
assign Instruction_Address_result_Monitor = PC_Core ;
assign Result_result_Monitor = ((Current_Instr[11:7] == 5'h00) & (RegWrite_Core == 1'b1)) ? 32'h00000000 : Destination_Register;




endmodule
