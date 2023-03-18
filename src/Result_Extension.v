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



module Result_Extender(Result_Un_Extended,Load_Instr,Store_Instr,Funct_3,Resukt_Extended);

input [31:0] Result_Un_Extended;
input Load_Instr,Store_Instr;
input [2:0] Funct_3;

output [31:0] Resukt_Extended;

assign Resukt_Extended =
/*Condition for Load Byte*/                               ((Load_Instr) & (Funct_3 == 3'b000)) ? {{24{Result_Un_Extended[7]}},Result_Un_Extended[7:0]} :                           
/*Condition for Load Half word*/                          ((Load_Instr) & (Funct_3 == 3'b001)) ? {{16{Result_Un_Extended[15]}},Result_Un_Extended[15:0]} :
/*Condition for Store Byte*/                              ((Store_Instr) & (Funct_3 == 3'b000)) ? {{24{1'b0}},Result_Un_Extended[7:0]} :                           
/*Condition for Store Haf word*/                          ((Store_Instr) & (Funct_3 == 3'b001)) ? {{16{1'b0}},Result_Un_Extended[15:0]} :                           
/*Condition for Load Byte Unsigned*/                      ((Load_Instr) & (Funct_3 == 3'b100)) ? {{24{1'b0}},Result_Un_Extended[7:0]}: 
/*Condition for Load Hal Word unsigned*/                  ((Load_Instr) & (Funct_3 == 3'b101)) ? {{16{1'b0}},Result_Un_Extended[15:0]}:
                                                          Result_Un_Extended;
                          
                        


endmodule
