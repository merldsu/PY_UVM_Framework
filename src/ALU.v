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


module alu(A,B,ALUControl,Result,Z,N,V,C);
    // declaring inputs
    input [31:0] A,B;
    input [3:0] ALUControl;
    
    // Declaring outputs
    output [31:0] Result;
    output Z, N, V, C;

    // declaring interim wires
    wire [31:0] a_and_b;
    wire [31:0] a_or_b;
    wire [31:0] not_b;
    wire [31:0] a_xor_b;
    wire [31:0] a_slli_b;
    wire [31:0] a_sRli_b;
    wire [31:0] a_sRAi_b;

    wire [31:0] mux_1;

    wire [31:0] sum;

    wire [31:0] mux_2;
 
     wire [31:0] slt;

    wire cout;
    wire Z_w,N_w,V_w,C_w;
    wire subtraction_check,Less_Than_Check;

    // Logic design

    // AND Operation
    assign a_and_b = A & B;

    // OR Operation
    assign a_or_b = A | B;

    //Xor of A and B
    assign a_xor_b = A^B; 

    // NOT Operation on B
    assign not_b = ~B;
    assign mux_1 = ALUControl[0] ? not_b : B;

    // Addition / subtraction Operation
    assign {cout,sum} = A + mux_1 +  {{31{1'b0}},ALUControl[0]} ;
     

    // Zero Extension
    assign Less_Than_Check = (ALUControl == 4'b0101) ? (N_w ^ V_w) : (ALUControl == 4'b0111) ? (~C_w):1'b0;
    assign slt = {31'b0000000000000000000000000000000,Less_Than_Check};
        
    //shifting operations
    assign a_slli_b = A << B[4:0] ;
    assign a_sRli_b = A >> B[4:0];
    assign a_sRAi_b = $signed(A) >>> B[4:0];

    // Designing 4by1 Mux
    assign mux_2 = (ALUControl == 4'b0000) ? sum : 
                   (ALUControl == 4'b0001) ? sum : 
                   (ALUControl == 4'b0010) ? a_and_b :  
                   (ALUControl == 4'b0011) ? a_or_b :
                   (ALUControl == 4'b0100) ? a_xor_b:
                   ((ALUControl == 4'b0101) | (ALUControl == 4'b0111) ) ? slt: 
                   (ALUControl == 4'b0110) ? a_slli_b:
                   (ALUControl == 4'b1000) ? a_sRli_b:
                   (ALUControl == 4'b1001) ? a_sRAi_b:
                   32'h00000000;  //Alu Control 111 is for SLTiU, and 101 for SLTi.

    assign Result = mux_2;

    // Flags temporary wire Assignment
    assign Z_w = &(~Result); // Zero flag

    assign N_w = sum[31]; // Negative Flag

    assign C_w = cout /*& (~ALUControl[1])*/; // Carry Flag

    assign V_w = (~ALUControl[1]) & (A[31] ^ sum[31]) & (~(A[31] ^ B[31] ^ ALUControl[0])); // Overflow Flag
   
    // Flag Assigments
    assign Z = Z_w;
    assign N = N_w;
    assign C = C_w;
    assign V = V_w;

endmodule
