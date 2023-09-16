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

import cocotb
from cocotb.triggers import Timer
import random
import pandas as pd
import pyuvm
import logging
from pyuvm import *
import os
from configuration import *
from func_timeout import func_timeout, FunctionTimedOut
#IMPORT THE SYSTEM PATH TO LINK DIFFERENT PY FILE
from pathlib import Path
import sys
sys.path.insert(0, str(Path(".").resolve()))
import generator_rv32imf as rv32imf
import generator_csr_test as csr_test
import generator_exclude_instruction as exclude_instruction

class Generator(uvm_component):

	def build_phase(self): # This phase is used to build important arrays or lists.

		self.listins=[] # This list is used in this file to carry important instructions in binary
		self.hex_listins=[] #This list contains Instructions in Hex
		self.listpc=[] #This list contains Instructions PC in Hex
		self.listdata=[] #This list contains random data points in Hex
		self.listcounter=[] #This list contains random data points PC in Hex
		self.opcode_l=[] # This list is used to carry opcodes which are being selected by checking configuration file
		self.i_ext_opcode=[0x3,0x23,0x13] #This list contains Opcodes for I-extension RISC-V
		self.m_ext_opcode=[0x33] #This list contains Opcodes for M-extension RISC-V
		
	def end_of_elaboration_phase(self): # This phase is used to check the configuration file
		self.logger.info("**********Generator Execution**********")
		testname = os.getenv("Test","riscv_csr_test")
		count=0
		
		for x in extension: # This for loop is used to check extension list in configuration file
			if (x=='RV32I'):
				self.opcode_l.extend(self.i_ext_opcode)
			elif (x=='RV32M'):
				self.opcode_l.extend(self.m_ext_opcode)
			else:
				self.logger.info("The selected Extension is not supported by Instruction Generator")
				raise AssertionError("The selected Extension is not supported by Instruction Generator")
				
		if (testname=='riscv_m_test'):# This condition is used to verify whether the entered extension in configuration file supports the test name.
			for x in extension:
				if (x == 'RV32M'):
					count = count + 1
				else:
					count = count
					
		elif (testname=='riscv_load_test' or  testname=='riscv_store_test' or testname=='riscv_arithmetic_test' or testname=='riscv_csr_test' or testname=='riscv_branch_test'):
			for x in extension:
				if (x == 'RV32I'):
					count = count + 1
				else:
					count = count
					
		elif (testname == 'riscv_random_test'):
			count = count + 1
		
		else:
			count = count

		if (count > 0): # If the count is greater than 0, means the extension entered in configuration file supports testname
			self.logger.info("Found the given testname in the supported Extension list(***Generator***)") 
		else:
			self.logger.info("The Given Testname is not supported by the given Extension list(***Generator***)")
			raise AssertionError('The Given Testname is not supported by the given Extension list(***Generator***)')
			
	def start_of_simulation_phase(self): # This phase is used to execute different important functions
		self.testname = os.getenv("Test","riscv_csr_test")
		self.test_iteration = int(os.getenv("Iteration","10"))
		self.boot_sequencer()
		self.initialize_registers()
		
		try:
		
			func_timeout(300,self.instruction_generator)
		
		except FunctionTimedOut:
			self.logger.info("Instruction Generator reach Time Out")
			raise AssertionError("Instruction Generator reach Time Out")
			
		self.instruction_terminator()
		self.data_generator()
		for x in range(len(self.listins)):
			self.hex_listins.append("0x"+(hex(int(self.listins[x],2))[2:].zfill(8)))
			
	def extract_phase(self): # This phase is used generate CSV
		instruction_bank= pd.DataFrame({'PC':self.listpc,'Instruction':self.hex_listins})
		instruction_bank.to_csv('INSTR_RV32.csv',index=False)

		data_bank= pd.DataFrame({'PC_ Data':self.listcounter,'Data':self.listdata})
		data_bank.to_csv('DATA_RV32.csv',index=False)
	
	def boot_sequencer(self): # This function is used to generate boot sequence for DUT
		self.listins.append("0b11000000000000000000000100110111") # Instruction in hex=0xC0000137
		self.listins.append("0b00000000000000010000000100010011") # Instruction in hex=0x00010113
		
	def initialize_registers(self): # This function is used to generate register initialization sequence for DUT
		for i in range(32):
			if (i!=2 and i!=0):
				immediate = random.randint(0,2147483647)
				immediate=hex(immediate)
				immediate='0x'+(immediate[2:].zfill(8))
				Imm1 = immediate[2:7]
				Imm2 = immediate[7:10]
				dum1 = int(Imm2[0],16)
				
				if (dum1 >= 8):
					r1 = int(Imm1,16) + 1
					r21 = bin(r1)[2:]
				else:
					r1 = int(Imm1,16)
					r21 = bin(r1)[2:]
				s1 = bin(int(Imm2,16))[2:]
				
				
				OPCODE_LUI = bin(55)[2:].zfill(7)
				OPCODE_ADDI = bin(19)[2:].zfill(7)
				IMM_LUI = r21
				IMM_ADDI = s1
				FUNCT3 = bin(0)[2:].zfill(3)
				RD = bin(i)[2:].zfill(5)
				RS1= bin(i)[2:].zfill(5)
				LUI="0b"+IMM_LUI.zfill(20)+RD+OPCODE_LUI
				ADDI="0b"+IMM_ADDI.zfill(12)+RS1+FUNCT3+RD+OPCODE_ADDI
				self.listins.append(LUI)
				self.listins.append(ADDI)
				
	def opcode_selector(self,testname,f_opcode): # This function selects the specific opcode from opcodes list coming from the function instruction generator
	
		if (testname=="riscv_random_test"):
			self.OP_RV32=random.choice(f_opcode)
		elif (testname=="riscv_load_test"):
			self.OP_RV32=f_opcode[0]
		elif (testname=="riscv_store_test"):
			self.OP_RV32=f_opcode[1]
		elif (testname=="riscv_arithmetic_test"):
			self.OP_RV32=f_opcode[2]
		elif(testname=="riscv_m_test"):
			self.OP_RV32=f_opcode[3]
					
		return self.OP_RV32
		
	def instruction_terminator(self): # This function generates program termination instruction

		self.listins.append("0b00000000000000000000000001110011") # instruction in hex=0x00000073 (ecall)
		
		return self.listpc,self.listins
	
	def program_counter(self): # This function Program counter generates values of multiplication of 4
		self.list_counter_=[]
		for x in range(len(self.listins)+1):
			counter=4*x
			hex_counter="0x"+(hex(counter)[2:].zfill(8))
			self.list_counter_.append(hex_counter)
		return self.list_counter_
	
	def data_generator(self): #This function generate data points and data counter and return both of them
		self.logger.info("Execution of Data Generator")
		for x in range(2048):
			counter=3221224448 + (x*4)
			hex_counter="0x"+(hex(counter)[2:].zfill(8))
			self.listcounter.append(hex_counter)
			data_values=random.randint(0,4294967295) 
			hex_data="0x"+(hex(data_values)[2:].zfill(8))
			self.listdata.append(hex_data)	
			
		return self.listcounter,self.listdata
	
	def instruction_generator(self): # This function instruction generator is used to generate the instruction and exclude the instruction provided by the user
		
		self.logger.info("Execution of Instruction Generator")
		counter=1
		counter_csr=1
		
		if (self.testname=='riscv_branch_test'):
			self.branch_program=rv32imf.fixed_brancheq(self.test_iteration) #Getting fixed branch and jump instructions
			self.listins.extend(self.branch_program)
		
		elif (self.testname=='riscv_csr_test'):
			while(counter_csr<=self.test_iteration):
				self.csr_program=csr_test.csrtest(excluded_csr,implemented_csr,extension,privileged_mode) #Getting CSR instruction
				
				status_csr=exclude_instruction.csr_exclude(self.csr_program,exclude_instructions) # Getting exclude status, if the status is high means the user have decided to exclude the specific instruction.
				
				if(status_csr == 0): # If the status is greater than zero, the instruction is excluded
					self.listins.append(self.csr_program)
					counter_csr = counter_csr + 1
				else:
					counter_csr = counter_csr
					status_csr = 0
		
		else:
			while (counter<=self.test_iteration):
				myopcode=self.opcode_selector(self.testname,self.opcode_l) # Sending list opcodes and testname to the function opcode selector and getting the specific opcode from the function
				
				#Generating instruction depending on the basis of opcode
				if (myopcode==0x3):
					instruct_generated = (rv32imf.get_load())
				elif (myopcode==0x23):
					instruct_generated = (rv32imf.get_store())
				elif (myopcode==0x13):
					instruct_generated = rv32imf.get_arthimetic()
				elif (myopcode==0x33):
					instruct_generated=rv32imf.M_extension()
				
				status=exclude_instruction.rv32imf_exclude(instruct_generated,exclude_instructions) # Getting exclude status, if the status is high means the user have decided to exclude the specific instruction.	
				
				if(status == 0): # If the status is greater than zero, the instruction is excluded
					self.listins.append(instruct_generated)
					
					counter = counter + 1
				else:
					counter = counter
					status = 0
			
		self.listpc=self.program_counter()
