# Copyright 2023 MERL-DSU

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Welcome to the Configuration File
# Please enter your desired architecture
# Please enter your desired excluded instructions
# Please try to avoid putting lui,branch,jumps and addi instruction in exclude instruction list as they are provided in boot sequence while at the start of the csv for smooth execution.

extension=['RV32I'] # eg. 'RV32I', 'RV32M'
exclude_instructions=[] # eg. ['lb', 'sw', 'srl', 'mul', 'div'] etc





