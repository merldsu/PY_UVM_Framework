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
# Please enter your csr number name to get it exclude
# Please enter your csr number name to get it add
# Please try to avoid putting lui,branch,jumps and addi instruction in exclude instruction list as they are provided in boot sequence while at the start of the csv for smooth execution.

# The extension list is used for the desired architecture
extension=['RV32I','RV32M'] # eg. ['RV32I', 'RV32M']

# The exclude instruction list is used for the instructions which have to removed
exclude_instructions=[] # eg. ['lb', 'sw', 'srl', 'mul', 'div'] etc

# The csr number list is used to remove specific csr number
# The basic csr numbers included in generator are:
# minstret, mhpmcounter3, mhpmcounter4, mhpmcounter5, mhpmcounter6, mcycleh, minstreth, mhpmcounter3h, mhpmcounter4h, mhpmcounter5h, mhpmcounter6h, mstatus, mie, mtvec, mcountinhibit, mhpmevent3, mhpmevent4, mhpmevent5, mhpmevent6, mscratch, mepc, mcause, mtval, mip, tselect, tdata1 or mcontrol, tdata2, mcycle, misa, mvendorid, marchid, mimpid, mhartid
# If you select the extension F so three csr numbers fflags,frm,fcsr will be included in generator

excluded_csr=['mcycle'] # eg.["miccmet","mdccmect","mcgc","mfdc","mscause"]

# The csr number add list is used to add specific csr number
implemented_csr=[] # eg.["miccmet","mdccmect","mcgc","mfdc","mscause"]


# The csr privileged mode list
privileged_mode=[] # eg.["machine_mode","user_mode","supervisor_mode"]

