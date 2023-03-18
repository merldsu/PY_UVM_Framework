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

class Generator(uvm_component):

	def build_phase(self):

		self.listins=[]
		self.hex_listins=[] #Instruction list
		self.listpc=[] #Instruction pc
		self.list_counter_=[] 
		self.listdata=[] #data list
		self.listcounter=[] #data pc
		self.opcode_l=[]
		self.i_ext_opcode=[0x3,0x23,0x13,0x37]
		self.m_ext_opcode=[0x33]
		
	def end_of_elaboration_phase(self):
		self.logger.info("**********Generator Execution**********")
		testname = os.getenv("Test","riscv_random_test")
		
		for x in extension:	
			if (x=='RV32I'):
				self.opcode_l.extend(self.i_ext_opcode)
			elif (x=='RV32M'):
				self.opcode_l.extend(self.m_ext_opcode)
			else:
				self.logger.info("The selected Extension is not supported by Instruction Generator")
				raise AssertionError("The selected Extension is not supported by Instruction Generator")
		count=0
		if (testname=='riscv_m_test'):
			for x in extension:
				if (x == 'RV32M'):
					count = count + 1
				else:
					count = count
		elif (testname=='riscv_load_test' or  testname=='riscv_store_test' or testname=='riscv_arithmetic_test' or testname=='riscv_utype_test' or testname=='riscv_branch_test'):
			for x in extension:
				if (x == 'RV32I'):
					count = count + 1
				else:
					count = count
		elif (testname == 'riscv_random_test'):
			count = count + 1
		else:
			count = count

		if (count > 0):
			self.logger.info("Found the given testname in the supported Extension list(***Generator***)") 
		else:
			self.logger.info("The Given Testname is not supported by the given Extension list(***Generator***)")
			raise AssertionError('The Given Testname is not supported by the given Extension list(***Generator***)')
			
	def start_of_simulation_phase(self):
		self.testname = os.getenv("Test","riscv_random_test")
		self.test_iteration = int(os.getenv("Iteration","10"))
		#self.test_it = int(test_iteration)
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
	def extract_phase(self):
		instruction_bank= pd.DataFrame({'PC':self.listpc,'Instruction':self.hex_listins})
		instruction_bank.to_csv('INSTR_RV32.csv',index=False)

		data_bank= pd.DataFrame({'PC_ Data':self.listcounter,'Data':self.listdata})
		data_bank.to_csv('DATA_RV32.csv',index=False)
	
	def boot_sequencer(self):
		self.listins.append("0b11000000000000000000000100110111")
		self.listins.append("0b00000000000000010000000100010011")
		
	def initialize_registers(self):
		for i in range(32):
			if (i!=2 and i!=0):
				self.OPCODE_LUI = bin(55)[2:].zfill(7)
				self.OPCODE_ADDI = bin(19)[2:].zfill(7)
				self.IMM_LUI = random.randint(0, 1048575)
				self.IMM_ADDI = random.randint(0, 4095)
				self.FUNCT3 = bin(0)[2:].zfill(3)
				self.RD = bin(i)[2:].zfill(5)
				self.RS1= bin(i)[2:].zfill(5)
				self.binary="0b"+bin(self.IMM_LUI)[2:].zfill(20)+self.RD+self.OPCODE_LUI
				self.LUI="0b"+bin(int(self.binary,2))[2:].zfill(32)
				self.binary1="0b"+bin(self.IMM_ADDI)[2:].zfill(12)+self.RS1+self.FUNCT3+self.RD+self.OPCODE_ADDI
				self.ADDI="0b"+bin(int(self.binary1,2))[2:].zfill(32)
				self.listins.append(self.LUI)
				self.listins.append(self.ADDI)
				
	def opcode_selector(self,testname,f_opcode):
	
		if (testname=="riscv_random_test"):
			self.OP_RV32=random.choice(f_opcode)
		elif (testname=="riscv_load_test"):
			self.OP_RV32=f_opcode[0]
		elif (testname=="riscv_store_test"):
			self.OP_RV32=f_opcode[1]
		elif (testname=="riscv_arithmetic_test"):
			self.OP_RV32=f_opcode[2]
		elif(testname=="riscv_utype_test"):
			self.OP_RV32=f_opcode[3]
		elif(testname=="riscv_m_test"):
			self.OP_RV32=f_opcode[4]
				
		return self.OP_RV32
		
	
	def instruction_select(self,opcode,testiteration):
		
		if (opcode==0x3):
			self.INSTRUCTION = (self.get_load())
			
		elif (opcode==0x23):
			self.INSTRUCTION = (self.get_store())
			
		elif (opcode==0x13):
			self.INSTRUCTION = self.get_arthimetic()
			
		elif (opcode==0x37):
			self.INSTRUCTION=self.u_type()
			
		elif (opcode==0x33):
			self.INSTRUCTION=self.M_extension()
			
		else:
			pass
			
		return self.INSTRUCTION
			
		
	
	def instruction_generator(self):
		self.logger.info("Execution of Instruction Generator")
		status=0
		counter=1
		
		if (self.testname=='riscv_branch_test'):
			self.branch_program=self.fixed_brancheq(self.test_iteration)
			self.listins.extend(self.branch_program)
		else:
			while (counter<=self.test_iteration):
				myopcode=self.opcode_selector(self.testname,self.opcode_l)
				
				instruct_generated=self.instruction_select(myopcode,self.test_iteration)
				
				
				for y in exclude_instructions:
					if (y=="auipc" and instruct_generated[27:34]=="0010111"):
						status=1
					if (y=="lb" and instruct_generated[19:22]=="000" and instruct_generated[27:34]=="0000011"):
						status=1
					if (y=="lh" and instruct_generated[19:22]=="001" and instruct_generated[27:34]=="0000011"):
						status=1
					if (y=="lw" and instruct_generated[19:22]=="010" and instruct_generated[27:34]=="0000011"):
						status=1
					if (y=="lbu" and instruct_generated[19:22]=="100" and instruct_generated[27:34]=="0000011"):
						status=1
					if (y=="lhu" and instruct_generated[19:22]=="101" and instruct_generated[27:34]=="0000011"):
						status=1
					if (y=="sb" and instruct_generated[19:22]=="000" and instruct_generated[27:34]=="0100011"):
						status=1
					if (y=="sh" and instruct_generated[19:22]=="001" and instruct_generated[27:34]=="0100011"):
						status=1
					if (y=="sw" and instruct_generated[19:22]=="010" and instruct_generated[27:34]=="0100011"):
						status=1
					if (y=="slti" and instruct_generated[19:22]=="010" and instruct_generated[27:34]=="0010011"):
						status=1
					if (y=="sltiu" and instruct_generated[19:22]=="011" and instruct_generated[27:34]=="0010011"):
						status=1
					if (y=="xori" and instruct_generated[19:22]=="100" and instruct_generated[27:34]=="0010011"):
						status=1
					if (y=="ori" and instruct_generated[19:22]=="110" and instruct_generated[27:34]=="0010011"):
						status=1
					if (y=="andi" and instruct_generated[19:22]=="111" and instruct_generated[27:34]=="0010011"):
						status=1
					if (y=="slli" and instruct_generated[19:22]=="001" and instruct_generated[27:34]=="0010011"):
						status=1
					if (y=="srli" and instruct_generated[19:22]=="101" and instruct_generated[27:34]=="0010011" and instruct_generated[2:9]=="0000000"):
						status=1
					if (y=="srai" and instruct_generated[19:22]=="101" and instruct_generated[27:34]=="0010011" and instruct_generated[2:9]=="0100000"):
						status=1
					if (y=="add" and instruct_generated[19:22]=="000" and instruct_generated[27:34]=="0110011" and instruct_generated[2:9]=="0000000"):
						status=1
					if (y=="sub" and instruct_generated[19:22]=="000" and instruct_generated[27:34]=="0110011" and instruct_generated[2:9]=="0100000"):
						status=1
					if (y=="sll" and instruct_generated[19:22]=="001" and instruct_generated[27:34]=="0110011"):
						status=1
					if (y=="slt" and instruct_generated[19:22]=="010" and instruct_generated[27:34]=="0110011"):
						status=1
					if (y=="sltu" and instruct_generated[19:22]=="011" and instruct_generated[27:34]=="0110011"):
						status=1
					if (y=="xor" and instruct_generated[19:22]=="100" and instruct_generated[27:34]=="0110011"):
						status=1
					if (y=="srl" and instruct_generated[19:22]=="101" and instruct_generated[27:34]=="0110011" and instruct_generated[2:9]=="0000000"):
						status=1
					if (y=="sra" and instruct_generated[19:22]=="101" and instruct_generated[27:34]=="0110011" and instruct_generated[2:9]=="0100000"):
						status=1
					if (y=="or" and instruct_generated[19:22]=="110" and instruct_generated[27:34]=="0110011"):
						status=1
					if (y=="and" and instruct_generated[19:22]=="111" and instruct_generated[27:34]=="0110011"):
						status=1
					if (y=="mul" and instruct_generated[19:22]=="000" and instruct_generated[27:34]=="0110011" and instruct_generated[2:9]=="0000001"):
						status = 1
					if (y=="mulh" and instruct_generated[19:22]=="001" and instruct_generated[27:34]=="0110011" and instruct_generated[2:9]=="0000001"):
						status = 1
					if (y=="mulhsu" and instruct_generated[19:22]=="010" and instruct_generated[27:34]=="0110011" and instruct_generated[2:9]=="0000001"):
						status = 1
					if (y=="mulhu" and instruct_generated[19:22]=="011" and instruct_generated[27:34]=="0110011" and instruct_generated[2:9]=="0000001"):
						status = 1
					if (y=="div" and instruct_generated[19:22]=="100" and instruct_generated[27:34]=="0110011" and instruct_generated[2:9]=="0000001"):
						status = 1
					if (y=="divu" and instruct_generated[19:22]=="101" and instruct_generated[27:34]=="0110011" and instruct_generated[2:9]=="0000001"):
						status = 1
					if (y=="rem" and instruct_generated[19:22]=="110" and instruct_generated[27:34]=="0110011" and instruct_generated[2:9]=="0000001"):
						status = 1
					if (y=="remu" and instruct_generated[19:22]=="111" and instruct_generated[27:34]=="0110011" and instruct_generated[2:9]=="0000001"):
						status = 1
						
				if(status == 0):
					self.listins.append(self.INSTRUCTION)
					
					counter = counter + 1
				else:
					counter = counter
					status = 0
			
		self.listpc=self.program_counter()		
		
	def instruction_terminator(self):

		self.listins.append("0b00000000000000000000000001110011")
		
		return self.listpc,self.listins
	
	def program_counter(self): #Program counter which generates values of multiplication of 4
		for x in range(len(self.listins)+1):
			self.counter=4*x
			self.hex_counter="0x"+(hex(self.counter)[2:].zfill(8))
			self.list_counter_.append(self.hex_counter)
		return self.list_counter_
	
	def data_generator(self): #This function generate data points and data counter and return both of them
		self.logger.info("Execution of Data Generator")
		for x in range(2048):
			self.counter=3221224448 + (x*4) 
			self.hex_counter="0x"+(hex(self.counter)[2:].zfill(8))
			self.listcounter.append(self.hex_counter)
			self.data_values=random.randint(0,4294967295) 
			self.hex_data="0x"+(hex(self.data_values)[2:].zfill(8))
			self.listdata.append(self.hex_data)	
			
		return self.listcounter,self.listdata
		
	def u_type(self):
			
		LISTOPCODE_UTYPE=[55,23] #One for LUI and another for AUIPC
		self.RD = random.randint(0,31)
		while self.RD==2:
			self.RD=random.randint(0,31)
		self.IMM = random.randint(0, 1048575)
		self.OPCODE_UTYPE=random.choice(LISTOPCODE_UTYPE)	
		self.binary="0b"+bin(self.IMM)[2:].zfill(20)+bin(self.RD)[2:].zfill(5)+bin(self.OPCODE_UTYPE)[2:].zfill(7)
		self.UTYPE="0b"+bin(int(self.binary,2))[2:].zfill(32)
		
		return self.UTYPE
		
	def get_load(self): #This function returns Load instruction

		LISTFUNC3_LD=[0,1,2,4,5]
		self.OP_RV32=bin(3)[2:].zfill(7)
		self.FUNCT3=random.choice(LISTFUNC3_LD)
		self.RS1=bin(2)[2:].zfill(5)
		self.RD = random.randint(0,31)
		while self.RD==2:
			self.RD=random.randint(0,31)
		self.IMM=random.randrange(0,1023,4)
		while (self.IMM+1073741824>4294967295 | self.IMM+1073741824<2147483648):
			self.IMM=random.randrange(0,1023,4)

		self.binary="0b"+bin(self.IMM)[2:].zfill(12)+self.RS1+bin(self.FUNCT3)[2:].zfill(3)+bin(self.RD)[2:].zfill(5)+self.OP_RV32
		self.LD="0b"+bin(int(self.binary,2))[2:].zfill(32)
				
		return self.LD
	
	def get_store(self): #This function returns all store instruction
	
		LISTFUNC3_ST=[0,1,2]
		self.OP_RV32=bin(35)[2:].zfill(7)
		self.FUNCT3=random.choice(LISTFUNC3_ST)
		self.RS1=bin(2)[2:].zfill(5)
		self.RS2=random.randint(0,31)
		self.IMM=random.randrange(0,1023,4)
		while (self.IMM+1073741824>4294967295 |self.IMM+1073741824<2147483648):
			self.IMM=random.randrange(0,1023,4)
		self.IMM1="0b"+(bin(self.IMM)[2:][7:])	
		self.IMM2="0b"+(bin(self.IMM)[2:][:7])
		self.binary="0b"+self.IMM2[2:].zfill(7)+bin(self.RS2)[2:].zfill(5)+self.RS1+bin(self.FUNCT3)[2:].zfill(3)+self.IMM1[2:].zfill(5)+self.OP_RV32
		self.ST="0b"+bin(int(self.binary,2))[2:].zfill(32)

		return self.ST
		
	def get_arthimetic(self): #This function return all immediate and rtype Instructions
	
		self.LIST=[19,51]
		self.LISTF7 = [0, 32]
		self.opcode = random.choice(self.LIST)
		self.FUNCT3 = random.randint(0,7)
		self.RS1 = random.randint(0, 31)
		self.RS2 = random.randint(0, 31)
		self.RD = random.randint(0, 31)
		self.shamt = random.randint(0, 31)
		self.IMM = random.randrange(0, 4095)
		while (self.RD == 2):
			self.RD = random.randint(0, 31)
		
		#In case of selection of Immidiate arthemetic instruction	
		if (self.opcode == 19):
			if(self.FUNCT3 == 5):
				self.FUNCT7 = random.choice(self.LISTF7)
				self.binary = "0b" + bin(self.FUNCT7)[2:].zfill(7) + bin(self.shamt)[2:].zfill(5) + bin(self.RS1)[2:].zfill(5) + bin(self.FUNCT3)[2:].zfill(3) + bin(self.RD)[2:].zfill(5) + bin(self.opcode)[2:].zfill(7)
			elif(self.FUNCT3 == 1):
				self.FUNCT7 = 0
				self.binary = "0b" + bin(self.FUNCT7)[2:].zfill(7) + bin(self.shamt)[2:].zfill(5) + bin(self.RS1)[2:].zfill(5) + bin(self.FUNCT3)[2:].zfill(3) + bin(self.RD)[2:].zfill(5) + bin(self.opcode)[2:].zfill(7)
			else:
				self.binary = "0b" + bin(self.IMM)[2:].zfill(12) + bin(self.RS1)[2:].zfill(5) + bin(self.FUNCT3)[2:].zfill(3) + bin(self.RD)[2:].zfill(5) + bin(self.opcode)[2:].zfill(7)
			self.ar_hex="0b"+bin(int(self.binary,2))[2:].zfill(32)
		
		#In case of selection of R-type arthemetic instruction	
		else:
			if(self.FUNCT3 == 0 or self.FUNCT3 == 5):
				self.FUNCT7 = random.choice(self.LISTF7)
			else:
				self.FUNCT7=0
			
			self.binary="0b"+bin(self.FUNCT7)[2:].zfill(7)+bin(self.RS2)[2:].zfill(5)+bin(self.RS1)[2:].zfill(5)+bin(self.FUNCT3)[2:].zfill(3)+bin(self.RD)[2:].zfill(5)+bin(self.opcode)[2:].zfill(7)
			self.ar_hex="0b"+bin(int(self.binary,2))[2:].zfill(32)
		
		return self.ar_hex
	
	def fixed_brancheq(self,num_list): #Fixed Branch Program
		program1=['0x00C000EF','0x00150513','0x00950C63','0x00400493','0x00300513','0xFE9518E3','0x00530313','0x0063C863','0x00300313','0x00700393','0xFE7348E3','0x00900E13']
		program2=["0x00800193","0x00100213","0x00100293","0x404181b3","0xfe304ce3"]
		program3=["0x09000293","0x00000313","0x00100393","0x00638433","0x00038313","0x00040393","0xfe539ae3"]
		program4=['0x00C000EF','0x00150513','0x00950863','0x00400493','0x00300513','0xFE9518E3','0x00300313']
		program5=['0x00000493','0x00000413','0x00A00313','0x00645863','0x008484B3','0x00140413','0xFF5FF06F']
		program6=['0x00000413','0x00000493','0x00A00E13','0x01C40863','0x008484B3','0x00140413','0xFF5FF06F']
		program7=['0x00400413','0x00100493','0x00249493','0x00940663','0x00148493','0x408484B3','0x008484B3']
		program8=['0x00400413','0x00100493','0x00249493','0x00941663','0x00148493','0x408484B3','0x008484B3']
		main_list=[]
		self.branch_pg=[]
		for i in range(num_list):
			program_choice=random.randrange(1,8)
			
			if program_choice==1:
				main_list.extend(program1)
			elif program_choice==2:
				main_list.extend(program2)
			elif program_choice==3:
				main_list.extend(program3)
			elif program_choice==4:
				main_list.extend(program4)
			elif program_choice==5:
				main_list.extend(program5)
			elif program_choice==6:
				main_list.extend(program6)
			elif program_choice==7:
				main_list.extend(program7)
			elif program_choice==8:
				main_list.extend(program8)
				
		for x in range(len(main_list)):
			self.branch_pg.append("0b"+(bin(int(main_list[x],16))[2:].zfill(32)))
		
		return self.branch_pg
	
	def M_extension(self):
	
		self.opcode=bin(51)[2:].zfill(7)
		self.RD=random.randint(0,31)
		while (self.RD == 2):
			self.RD = random.randint(0, 31)
		self.FUNCT3=random.randint(0,7)
		self.rs1=random.randint(0,31)
		self.rs2=random.randint(0,31)
		self.funct7=bin(1)[2:].zfill(7)
		self.binary = "0b" + self.funct7 + bin(self.rs2)[2:].zfill(5) + bin(self.rs1)[2:].zfill(5) + bin(self.FUNCT3)[2:].zfill(3) + bin(self.RD)[2:].zfill(5) + self.opcode
		self.hex="0b"+bin(int(self.binary,2))[2:].zfill(32)
		
		return self.hex

	
	
	
	
	
		
