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




module Adder(Input_A,Input_B,ImmSrc,Output_A);

input [31:0] Input_A,Input_B;
input [2:0] ImmSrc;
output [31:0] Output_A;

wire [31:0] Output_A_wire;

assign Output_A_wire = Input_A + Input_B;

assign Output_A = (ImmSrc ==3'b000) ? {Output_A_wire[31:1],1'b0} : Output_A_wire;

endmodule
