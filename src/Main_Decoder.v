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




module main_decoder(op,zero,Negative,Overflow,Carry,Shift_Type,Funct_3,Reg_Read_Enable_1,Reg_Read_Enable_2,Mem_Read_Enable,RegWrite,MemWrite,ResultSrc, ALUSrc,Finish_Prog, ImmSrc, ALUOp, PCSrc);

    // Inputs / Outputs declaration
    input zero,Negative,Overflow,Carry,Shift_Type;
    input [6:0] op;
    input [2:0] Funct_3;
    output Reg_Read_Enable_1,Reg_Read_Enable_2;
    output Mem_Read_Enable;
    output RegWrite, MemWrite, PCSrc;
    output Finish_Prog;
    output [1:0]  ALUOp,ALUSrc,ResultSrc;
    output [2:0] ImmSrc;

    // interim wire
    wire branch;
    
    assign Finish_Prog = (op == 7'b1110011) ? 1'b1 :1'b0;

    assign RegWrite = ((op == 7'b0000011) | (op == 7'b0110011) | (op == 7'b0110111) | (op== 7'b0010111) | (op == 7'b1101111) | (op == 7'b1100111) | (op==7'b0010011) ) ? 1'b1 : 1'b0;

    assign MemWrite = (op == 7'b0100011) ? 1'b1 : 1'b0;

    assign ResultSrc = (op == 7'b0000011) ? 2'b01 : ((op == 7'b1101111) | (op == 7'b1100111) ) ? 2'b10 : 2'b00;

    assign Reg_Read_Enable_1 = ( (op == 7'b0110011) | (op == 7'b0010011) | (op == 7'b1100011) | (op == 7'b0000011 ) | (op == 7'b0100011) | (op == 7'b1100111)) ;
    
    assign Reg_Read_Enable_2 = ((op == 7'b0100011) | (op == 7'b1100011) | (op == 7'b0110011) ) ;

    assign Mem_Read_Enable =  (op ==7'b0000011) ;
     
    assign ALUSrc[1] = ((op == 7'b0000011) | (op == 7'b0100011) | (op == 7'b0010011) | (op == 7'b0110111) | (op == 7'b0010111) | (op == 7'b1100111) ) ? 1'b1 : 1'b0;
    
    assign ALUSrc[0] = (op== 7'b0010111);


    assign branch = (op == 7'b1100011) & ( ( zero & (Funct_3 ==3'b000)) | ( (~zero) & (Funct_3 ==3'b001)) | ( (Negative ^ Overflow) & (Funct_3 ==3'b100)) | ( (~((Negative) ^ (Overflow))) & (Funct_3 ==3'b101) ) | ( (~Carry) & (Funct_3 == 3'b110) ) | ( (Carry) & (Funct_3 == 3'b111) )  ) ;

    assign ImmSrc = (op == 7'b0100011) ? 3'b001 : (op == 7'b1100011) ? 3'b010 : ((op == 7'b0110111) | (op== 7'b0010111) ) ? 3'b011 : (op == 7'b1101111 ) ? 3'b100 : ( (op == 7'b0010011) & (Funct_3 == 3'b101) & (Shift_Type) ) ? 3'b101 : 3'b000;
    
    assign ALUOp = (op == 7'b0110011) ? 2'b10 : (op == 7'b1100011) ? 2'b01 : (op == 7'b0010011) ? 2'b11 : 2'b00;

    assign PCSrc = (branch) | (op == 7'b1101111) | (op==7'b1100111);

    
endmodule
