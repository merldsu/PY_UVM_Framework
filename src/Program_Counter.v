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



module Program_Counter(PC_Next,PC,clk,rst);

input  [31:0] PC_Next;
input rst,clk;
output reg [31:0] PC;

always @ (posedge clk)
begin
  if (~rst)
     begin
      PC <= {32{1'b0}};
     end
  else 
     begin
      PC <= PC_Next;
     end   
end


endmodule
