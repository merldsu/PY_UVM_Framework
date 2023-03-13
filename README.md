# License
Copyright [2023] [MERL-DSU]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


# Py_UVM_Framework
This repo contain the Py-UVM framework for RISC-V Single Cycle Core



# Prerequisite
1) Cocotb
2) pyuvm
3) Verilator v4.1O6
4) python 3.8 or high version
5) Pandas


# Setting up Environment
1) Configuration File:

     a) Open the configuration.py file.
     
     b) Enter the RISC-V Extension supported by your hardware.
     
     c) Enter the Excluded Instruction name as per your requirements.
   
   More details can be found in configuration.py file
   
   
2) Test.txt:

     a) Open the Test.txt file.
        
     b) Enter the Testname and number of iterations.
        
        
        For example:
        Test=riscv_random_test Iteration=100
     

# Supported Test
1) riscv_random_test
2) riscv_load_test
3) riscv_store_test
4) riscv_artihmetic_test
5) riscv_m_test
6) riscv_utype_test


# Running Framework 
         python3 Script.py

# Test Information
All the log files will be available in the log folder.


