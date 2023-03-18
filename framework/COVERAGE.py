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


import csv
import pandas as pd
import os
import cocotb, pyuvm
from pyuvm import *
from collections import Counter
from operator import add
import logging
from cocotb.triggers import ClockCycles
from pyuvm import utility_classes
from cocotb.triggers import Timer, FallingEdge, RisingEdge
import random
import sys
from pathlib import Path
parent_path = Path("..").resolve()
sys.path.insert(0, str(parent_path))

def directory():
	dir_path = 'log/Coverage'
	if not os.path.exists(dir_path):
		os.mkdir(dir_path)
	cvg_file = os.path.join(dir_path, 'Coverage.csv')
	return cvg_file

class Coverage(uvm_component):

	def build_phase(self):
		self.logger.info("********* Execution of Coverage Build Phase*********")
		self.dlist = []
		self.xyz_list =[]
		self.percentage_list = []
		self.count_list = []
		self.instr_list = []
		self.new_percentage_list = []
		self.values = []
		self.instruction_names = [ 'LUI', 'AUIPC','JAL', 'JALR', 'BEQ', 'BNE', 'BLT', 'BGE','BLTU', 'BGEU','LB', 'LH', 'LW', 'LBU', 'LHU',  'SB' , 'SH', 'SW', 'ADDI', 'SLTI', 'SLTIU', 'XORi', 'ORi', 'ANDI', 'SLLI', 'SRLI', 'SRAI', 'ADD', 'SUB', 'SLL', 'SLT', 'SLTU', 'XOR', 'SRL', 'SRA', 'OR', 'AND', 'MUL', 'MULH', 'MULHSU', 'MULHU', 'DIV', 'DIVU', 'REM', 'REMU', 'ECALL']
		
		
		self.reg_rd = []
		self.reg_rs1 = []
		self.reg_rs2 = []
		self.names_of_registers = ['zero', 'ra', 'sp', 'gp', 'tp', 't0', 't1','t2' , 's0', 's1', 'a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 's2', 's3', 's4',  's5', 's6', 's7', 's8', 's9', 's10' ,'s11', 't3', 't4', 't5', 't6', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED' , 'RESERVED' , 'RESERVED' , 'RESERVED' , 'RESERVED' , 'RESERVED' , 'RESERVED' , 'RESERVED' , 'RESERVED', 'RESERVED']
		
		self.list_rd = []
		self.list_rs1 = []
		self.list_rs2 = []
		

		self.imm_read = []
		self.imm_value = []
		self.list_imm = ['imm_pos', 'imm_neg', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED','RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED' , 'RESERVED' , 'RESERVED' , 'RESERVED' , 'RESERVED' , 'RESERVED' , 'RESERVED' , 'RESERVED' , 'RESERVED', 'RESERVED']


	def report_phase(self):
		
		self.COVERAGE_RV32()
		self.COVERAGE_WORKING_RV32()
		self.logger.info("*********Generate the Coverage Report*********")
	
	def COVERAGE_RV32(self):

		self.cvg = set()

		self.dfA = pd.read_csv('ISS.csv')		
		self.dfA.columns
		
		self.specific_column = self.dfA["INSTRUCTION"] 
		self.main_column = self.specific_column
		self.main_column[2:]


		filename = "coverage.csv"
		self.covg = directory()
		if os.path.isfile(self.covg):
			self.covg = directory()
			dfC = pd.read_csv(self.covg)
			column_names = dfC.columns.tolist()
			new_variable = dfC['TOTAL_TIMES_INSTRUCTIONS_PERFORMED']
			self.total_count = new_variable [0]
			self.total_count = self.total_count + (len(self.main_column))

			instr = dfC['INSTRUCTION_COUNT']
			self.list_rd = dfC['RD']
			self.list_rs1 = dfC['RS_1']
			self.list_rs2 = dfC['RS_2']
			self.imm_read = dfC['VALUES']

			
			for i in range(len(self.instruction_names)):
				self.values.append(0)
				self.reg_rd.append(0)
				self.reg_rs1.append(0)
				self.reg_rs2.append(0)
				self.imm_value.append(0)
				
			for i in range(len(self.instruction_names)):
				
				self.values[i] = instr[i]
				self.reg_rd[i] = self.list_rd[i]
				self.reg_rs1[i] = self.list_rs1[i]
				self.reg_rs2[i] = self.list_rs2[i]
				self.imm_value[i] = self.imm_read[i] 

		else:
			self.total_count = (len(self.main_column))
			for i in range(len(self.instruction_names)):
				self.values.append(0)
				self.reg_rd.append(0)
				self.reg_rs1.append(0)
				self.reg_rs2.append(0)
				self.imm_value.append(0)
		
	def COVERAGE_WORKING_RV32(self):

		for we in self.main_column:
			self.dlist.append(we[2:].zfill(8))
			self.xyz_list.append(bin(int(we[2:].zfill(8),16))[2:].zfill(32))

		for i in range(len(self.xyz_list)):
			if (self.xyz_list[i][25:32] == '0110111' or self.xyz_list[i][25:32] == '0010111' or self.xyz_list[i][25:32] == '1101111' or self.xyz_list[i][25:32] == '1100111' or self.xyz_list[i][25:32] == '0000011' or self.xyz_list[i][25:32] == '0100011' or self.xyz_list[i][25:32] == '0010011'):
				if(self.xyz_list[0] == 1):
					self.imm_value[1] = self.imm_value[1] + 1

				else:
					self.imm_value[0] = self.imm_value[0] + 1
					
			if (self.xyz_list[i][25:32] == '0110111'):
				self.values[0] = self.values[0] + 1
				rd = self.xyz_list[i][20:25]
				self.reg_rd[(int(rd, 2))] = self.reg_rd[int(rd, 2)] + 1
				

			elif (self.xyz_list[i][25:32] == '0010111'):
				self.values[1] = self.values[1] + 1
				
				rd = self.xyz_list[i][20:25]
				rd_h = int(rd,2)
				self.reg_rd[rd_h] = self.reg_rd[rd_h] + 1
				
			elif ((self.xyz_list[i][25:32] == '1101111')):
				self.values[2] = self.values[2] + 1
				
				rd = self.xyz_list[i][20:25]
				self.reg_rd[(int(rd, 2))] = self.reg_rd[int(rd, 2)] + 1				
				
			elif ((self.xyz_list[i][25:32] == '1100111') and (self.xyz_list[i][17:20] == '000')):
				self.values[3] = self.values[3] + 1
				
				rd = self.xyz_list[i][20:25]
				self.reg_rd[(int(rd, 2))] = self.reg_rd[int(rd, 2)] + 1
				
				rs1 = self.xyz_list[i][12:17]
				self.reg_rs1[int(rs1, 2)] = self.reg_rs1[int(rs1, 2)] + 1		
				
			elif ((self.xyz_list[i][25:32] == '1100011')):
							
				rs1 = self.xyz_list[i][12:17]
				self.reg_rs1[int(rs1, 2)] = self.reg_rs1[int(rs1, 2)] + 1
				
				rs2 = self.xyz_list[i][7:12]
				self.reg_rs2[int(rs2, 2)] = self.reg_rs2[int(rs2, 2)] + 1
				
				if ((self.xyz_list[i][17:20] == '000')):
					self.values[4] = self.values[4] + 1
					
				elif ((self.xyz_list[i][17:20] == '001')):
					self.values[5] = self.values[5] + 1
					
				elif ((self.xyz_list[i][17:20] == '100')):
					self.values[6] = self.values[6] + 1
					
				elif ((self.xyz_list[i][17:20] == '101')):
					self.values[7] = self.values[7] + 1
					
				elif ((self.xyz_list[i][17:20] == '110')):
					self.values[8] = self.values[8] + 1
					
				else:
					self.values[9] = self.values[9] + 1
					
					
			elif ((self.xyz_list[i][25:32] == '0000011')):
				rd = self.xyz_list[i][20:25]
				self.reg_rd[(int(rd, 2))] = self.reg_rd[int(rd, 2)]+1			
				
				rs1 = self.xyz_list[i][12:17]
				self.reg_rs1[int(rs1, 2)] = self.reg_rs1[int(rs1, 2)] + 1
				
				if ((self.xyz_list[i][17:20] == '000')):
					self.values[10] = self.values[10] + 1
					
				elif ((self.xyz_list[i][17:20] == '001')):
					self.values[11] = self.values[11] + 1
					
				elif ((self.xyz_list[i][17:20] == '010')):
					self.values[12] = self.values[12] + 1
					
				elif ((self.xyz_list[i][17:20] == '100')):
					self.values[13] = self.values[13] + 1

				else:
					self.values[14] = self.values[14] + 1
					
			elif ((self.xyz_list[i][25:32] == '0100011')):		
				
				rs1 = self.xyz_list[i][12:17]
				self.reg_rs1[int(rs1, 2)] = self.reg_rs1[int(rs1, 2)] + 1
				
				rs2 = self.xyz_list[i][7:12]
				self.reg_rs2[int(rs2, 2)] = self.reg_rs2[int(rs2, 2)] + 1
				
				if ((self.xyz_list[i][17:20] == '000')):
					self.values[15] = self.values[15] + 1
					
				elif ((self.xyz_list[i][17:20] == '001')):
					self.values[16] = self.values[16] + 1

				else:
					self.values[17] = self.values[17] + 1
					
			elif ((self.xyz_list[i][25:32] == '0010011')):
				rd = self.xyz_list[i][20:25]
				self.reg_rd[(int(rd, 2))] = self.reg_rd[int(rd, 2)] + 1			
				
				rs1 = self.xyz_list[i][12:17]
				self.reg_rs1[int(rs1, 2)] = self.reg_rs1[int(rs1, 2)] + 1
				
				if ((self.xyz_list[i][17:20] == '000')):
					self.values[18] = self.values[18] + 1
					
				elif ((self.xyz_list[i][17:20] == '010')):
					self.values[19] = self.values[19] + 1
					
				elif ((self.xyz_list[i][17:20] == '011')):
					self.values[20] = self.values[20] + 1
					
				elif ((self.xyz_list[i][17:20] == '100')):
					self.values[21] = self.values[21] + 1
					
				elif ((self.xyz_list[i][17:20] == '110')):
					self.values[22] = self.values[22] + 1

				elif ((self.xyz_list[i][17:20] == '111')):
					self.values[23] = self.values[23] + 1
					
				elif (((self.xyz_list[i][17:20] == '001')) and ((self.xyz_list[i][0:7] == '0000000'))):
					self.values[24] = self.values[24] + 1
				
				elif (((self.xyz_list[i][17:20] == '101')) and ((self.xyz_list[i][0:7] == '0000000'))):
					self.values[25] = self.values[25] + 1

				elif (((self.xyz_list[i][17:20] == '101')) and ((self.xyz_list[i][0:7] == '0100000'))):
					self.values[26] = self.values[26] + 1
				
				else:
					print("DEFAULT")
					
			elif ((self.xyz_list[i][25:32] == '0110011')):
				rd = self.xyz_list[i][20:25]
				self.reg_rd[(int(rd, 2))] = self.reg_rd[int(rd, 2)] + 1			
				
				rs1 = self.xyz_list[i][12:17]
				self.reg_rs1[int(rs1, 2)] = self.reg_rs1[int(rs1, 2)] + 1
				
				rs2 = self.xyz_list[i][7:12]
				self.reg_rs2[int(rs2, 2)] = self.reg_rs2[int(rs2, 2)] + 1
				
				if((self.xyz_list[i][17:20] == '000') and (self.xyz_list[i][0:7] == '0000000')):
					self.values[27] = self.values[27] + 1
				
				elif ((self.xyz_list[i][17:20] == '000') and (self.xyz_list[i][0:7] == '0100000')):
					self.values[28] = self.values[28] + 1
					
				elif((self.xyz_list[i][17:20] == '001')) and ((self.xyz_list[i][0:7] == '0000000')):
					self.values[29] = self.values[29] + 1
					
				elif((self.xyz_list[i][17:20] == '010')) and ((self.xyz_list[i][0:7] == '0000000')):
					self.values[30] = self.values[30] + 1
				
				elif((self.xyz_list[i][17:20] == '011')) and ((self.xyz_list[i][0:7] == '0000000')):
					self.values[31] = self.values[31] + 1
					
				elif((self.xyz_list[i][17:20] == '100')) and ((self.xyz_list[i][0:7] == '0000000')):
					self.values[32] = self.values[32] + 1
					
				elif((self.xyz_list[i][17:20] == '101')) and ((self.xyz_list[i][0:7] == '0000000')):
					self.values[33] = self.values[33] + 1
				
				elif((self.xyz_list[i][17:20] == '101')) and ((self.xyz_list[i][0:7] == '0100000')):
					self.values[34] = self.values[34] + 1
				
				elif((self.xyz_list[i][17:20] == '110')) and ((self.xyz_list[i][0:7] == '0000000')):
					self.values[35] = self.values[35] + 1

				else:
					self.values[36] = self.values[36] + 1
					
							
			elif ((self.xyz_list[i][25:32] == '0110011') and (self.xyz_list[i][0:7] == '0000001')):
				rd = self.xyz_list[i][20:25]
				self.reg_rd[int(rd, 2)] = self.reg_rd[int(rd, 2)] + 1
				
				rs1 = self.xyz_list[i][12:17]
				self.reg_rs1[int(rs1, 2)] = self.reg_rs1[int(rs1, 2)] + 1
				
				rs2 = self.xyz_list[i][7:12]
				self.reg_rs2[int(rs2, 2)] = self.reg_rs2[int(rs2, 2)] + 1
				
				if (self.xyz_list[i][17:20] == '000'):
					self.values[37] = self.values[37] + 1
					
				elif (self.xyz_list[i][17:20] == '001'):
					self.values[38] = self.values[38] + 1
					
				elif (self.xyz_list[i][17:20] == '010'):
					self.values[39] = self.values[39] + 1
					
				elif (self.xyz_list[i][17:20] == '011'):
					self.values[40] = self.values[40] + 1
				
				elif (self.xyz_list[i][17:20] == '100'):
					self.values[41] = self.values[41] + 1
					
				elif (self.xyz_list[i][17:20] == '101'):
					self.values[42] = self.values[42] + 1
					
				elif (self.xyz_list[i][17:20] == '110'):
					self.values[43] = self.values[43] + 1
					
				else:
					self.values[44] = self.values[44] + 1

		
				
			elif ((self.xyz_list[i][25:32] == '1110011') and (self.xyz_list[i][17:20] == '000')and (self.xyz_list[i][0:7] == '0000000')):
				self.values[45] = self.values[45] + 1
	
			else:
				print("INVALID")

		my_series = pd.Series(self.values)
		for i in range (len(self.values)):
			self.final_percentage = (self.values[i] /  self.total_count) * 100;
			self.percentage_list.append(self.final_percentage)
			self.count_list.append(self.total_count)

		DICT = {'NAMES_OF_INSTR': self.instruction_names , 'INSTRUCTION_COUNT': self.values , 'TOTAL_TIMES_INSTRUCTIONS_PERFORMED': self.count_list, 'TOTAL_INSTRUCTIONS_IN_PERCENTAGE' : self.percentage_list, 'REGISTER_NAMES': self.names_of_registers, 'RD': self.reg_rd, 'RS_1': self.reg_rs1, 'RS_2': self.reg_rs2, 'MISSCELENOUS': self.list_imm, 'VALUES' : self.imm_value}
		self.dfb = pd.DataFrame.from_dict(DICT) 
		self.covg = directory() 
		self.dfb.to_csv(self.covg)
		
