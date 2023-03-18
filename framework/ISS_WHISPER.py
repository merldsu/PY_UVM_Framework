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

import pandas as pd
import numpy as np
import csv
import os
import sys
import logging
import cocotb
import pyuvm
from pyuvm import *
#import csv file
class ISS_SIM(uvm_component):
	
	
	def extract_phase(self):
		self.run_iss_sim()
		
	def run_iss_sim(self):
	
		self.logger.info("**********ISS_SIM Execution**********")
		
		df = pd.read_csv('INSTR_RV32.csv')
		df_a = pd.read_csv('DATA_RV32.csv')
		
		INSTR_RV32= df['Instruction'].tolist()
		DATA_RV32= df_a['Data'].tolist()
		
		# To remove the instruction(ecall) from RV32_Instruction_list 
		
		INSTR_RV32.remove('0x00000073')
		
		INSTR_RV32.append('0xd05801b7')
		INSTR_RV32.append('0x0ff00293')
		INSTR_RV32.append('0x00518023')
		INSTR_RV32.append('0xfe000ae3')
		

		self.logger.info("Read CSV file from Sequencer (ISS_SIM)")
		
		# Store Instruction RV_32 in list only values not '0x'
		dlist_INSTR_RV32 =[]
		for i in INSTR_RV32:
			dlist_INSTR_RV32.append(i[2:])
			
		# for DATA_RV32 in list only values not '0x'	
		dlist_DATA_RV32 =[]
		for x in DATA_RV32:
			dlist_DATA_RV32.append(x[2:])
		
		# INSTRUCTION RV32 2-bit SWAPPING AND SPACING AFTER EVERY 2-bits 
		for i in range(len(dlist_INSTR_RV32)):
		    dlist_INSTR_RV32[i] = dlist_INSTR_RV32[i].upper()
		 
		program = []
		for q in range(0,len(dlist_INSTR_RV32)):
		  for j in range(0,8,2):
		    program.append((dlist_INSTR_RV32[q][6-j:8-j])) 
		
		
		# DATARV32 2-bit SWAPPING AND SPACING AFTER EVERY 2-bits
		
		for z in range(len(dlist_DATA_RV32)):
		    dlist_DATA_RV32[z] = dlist_DATA_RV32[z].upper()
		 
		program_1 = []
		for w in range(0,len(dlist_DATA_RV32)):
		  for e in range(0,8,2):
		    program_1.append((dlist_DATA_RV32[w][6-e:8-e]))
		   
		 
		# FROM HERE WE MAKE THE HEX FILE
		
		self.logger.info("Generate HEX file (ISS_SIM)")
		
		with open("program.hex", "w+") as f:
		  f.write('@00000000\n')  
		  f.write(str(program))    
		  f.write('\n@BFFFFC00\n')
		  f.write(str(program_1)) 
		    
		fin = open("program.hex", "rt")
		#read file contents to string
		data = fin.read()
		#replace all occurrences of the required string
		data = data.replace(',', '')
		data = data.replace('[', '')
		data = data.replace(']', '')
		data = data.replace("'", "")
		#close the input file
		fin.close()
		#open the input file in write mode
		fin = open("program.hex", "wt")
		#overrite the input file with the resulting data
		fin.write(data)
		#close the file
		fin.close()
		
		
		
		#HERE WE USE THE COMMAND TO RUN ISS(WHISPER)
		a = os.getcwd()
		self.logger.info("Sending HEX file to ISS (ISS_SIM)")
		os.system("whisper --isa im -x"+a+"/program.hex -s 0x00000000 --tohost 0xd0580000 -f ISS.txt")
		self.logger.info("Read HEX file from ISS (Results) ")
		os.system("python3 ISS_READ.py")
		self.logger.info("Convert HEX file into CSV")
		
