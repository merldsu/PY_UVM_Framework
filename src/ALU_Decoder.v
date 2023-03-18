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


module alu_decoder(ALUOp,op5,Shift_Type,funct3,funct7,ALUControl);
    input op5, funct7,Shift_Type;
    input [2:0] funct3;
    input [1:0] ALUOp;
    output [3:0] ALUControl;

    // interim wire
    wire [1:0] concatenation;

    assign concatenation = {op5, funct7};

    assign ALUControl = (ALUOp == 2'b00) ? 4'b0000 :
                        (ALUOp == 2'b01) ? 4'b0001 :
/*Opc_SLT*/             ((ALUOp == 2'b10) & (funct3 == 3'b010)) ? 4'b0101 :
/*Opc_OR*/              ((ALUOp == 2'b10) & (funct3 == 3'b110)) ? 4'b0011 :
/*Opc_AND*/             ((ALUOp == 2'b10) & (funct3 == 3'b111)) ? 4'b0010 :
/*Opc_SUB*/             ((ALUOp == 2'b10) & (funct3 == 3'b000) & (concatenation == 2'b11)) ? 4'b0001 :
/*Opc_ADD*/            ((ALUOp == 2'b10) & (funct3 == 3'b000) & (concatenation == 2'b10)) ? 4'b0000 :
/*Opc_SLL*/             ((ALUOp == 2'b10) & (funct3 == 3'b001)) ? 4'b0110:
/*Opc_SLTU*/            ((ALUOp == 2'b10) & (funct3 == 3'b011)) ? 4'b0111:
/*Opc_XOR*/             ((ALUOp == 2'b10) & (funct3 == 3'b100)) ? 4'b0100:
/*Opc_SRL*/             ((ALUOp == 2'b10) & (funct3 == 3'b101) & (~funct7)) ? 4'b1000:
/*Opc_SRA*/             ((ALUOp == 2'b10) & (funct3 == 3'b101) & (funct7)) ? 4'b1001:
/*Opc_Addi*/            ((ALUOp == 2'b11) & (funct3 == 3'b000)) ? 4'b0000: 
/*Opc_SLTI*/            ((ALUOp == 2'b11) & (funct3 == 3'b010)) ? 4'b0101:
/*Opc_SLTIU*/           ((ALUOp == 2'b11) & (funct3 == 3'b011)) ? 4'b0111:                        
/*Opc_XORI*/            ((ALUOp == 2'b11) & (funct3 == 3'b100)) ? 4'b0100:
/*Opc_ORI*/             ((ALUOp == 2'b11) & (funct3 == 3'b110)) ? 4'b0011:
/*Opc_ANDI*/            ((ALUOp == 2'b11) & (funct3 == 3'b111)) ? 4'b0010:
/*Ooc_SLLI*/             ((ALUOp == 2'b11) & (funct3 == 3'b001)) ? 4'b0110:  
/*Ooc_SRLI*/             ((ALUOp == 2'b11) & (funct3 == 3'b101) & (~Shift_Type)) ? 4'b1000:  
/*Ooc_SRAI*/             ((ALUOp == 2'b11) & (funct3 == 3'b101) & (Shift_Type)) ? 4'b1001:  
                        4'b0000;


endmodule
