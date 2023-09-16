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

# current work directory file access
from pathlib import Path
parent_path = Path(".").resolve()
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
		self.instruction_names = [ 'LUI', 'AUIPC','JAL', 'JALR', 'BEQ', 'BNE', 'BLT', 'BGE','BLTU', 'BGEU','LB', 'LH', 'LW', 'LBU', 'LHU',  'SB' , 'SH', 'SW', 'ADDI', 'SLTI', 'SLTIU', 'XORi', 'ORi', 'ANDI', 'SLLI', 'SRLI', 'SRAI', 'ADD', 'SUB', 'SLL', 'SLT', 'SLTU', 'XOR', 'SRL', 'SRA', 'OR', 'AND', 'MUL', 'MULH', 'MULHSU', 'MULHU', 'DIV', 'DIVU', 'REM', 'REMU','FLW', 'FSW', 'FMADD.S', 'FMSUB.S', 'FNMSUB.S', 'FNMADD.S', 'FADD.S', 'FSUB.S', 'FMUL.S', 'FDIV.S', 'FSQRT.S','FSGNJ.S', 'FSGNJN.S',
		'FSGNJX.S','FMIN.S', 'FMAX.S', 'FCVT.W.S', 'FCVT.WU.S', 'FMV.X.W', 'FEQ.S', 'FLT.S', 'FLE.S', 'FCLASS.S', 
		'FCVT.S.W', 'FCVT.S.WU', 'FMV.W.X', 'CSRRW', 'CSRRS', 'CSRRC', 'CSRRWI', 'CSRRSI', 'CSRRCI',  'ECALL']
		
		
		self.reg_rd = []
		self.reg_rs1 = []
		self.reg_rs2 = []
		self.names_of_registers = ['zero', 'ra', 'sp', 'gp', 'tp', 't0', 't1','t2' , 's0', 's1', 'a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 's2', 's3', 's4',  's5', 's6', 's7', 's8', 's9', 's10' ,'s11', 't3', 't4', 't5', 't6', 'ft0', 'ft1', 'ft2', 'ft3', 'ft4', 'ft5', 'ft6', 'ft7',
		'fs0', 'fs1', 'fa0', 'fa1', 'fa2', 'fa3', 'fa4', 'fa5', 'fa6', 'fa7', 'fs2', 'fs3', 'fs4', 'fs5', 'fs6', 'fs7',
		'fs8', 'fs9', 'fs10', 'fs11', 'ft8', 'ft9', 'ft10', 'ft11','RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED' , 'RESERVED' , 'RESERVED' , 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED']
		
		self.list_rd = []
		self.list_rs1 = []
		self.list_rs2 = []
		self.INSTR_iter = []
		

		self.imm_read = []
		self.imm_value = []
		self.list_imm = ['imm_pos', 'imm_neg', 'RNE', 'RTZ', 'RDN', 'RUP', 'DYN', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED','RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED' , 'RESERVED' , 'RESERVED' , 'RESERVED' , 'RESERVED' , 'RESERVED' , 'RESERVED' , 'RESERVED' , 'RESERVED', 'RESERVED' , 'RESERVED' , 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED']
		
		self.list_INSTR = ["minstret" , "mhpmcounter3","mhpmcounter4","mhpmcounter5" ,
              "mhpmcounter6", "mcycleh", "minstreth", "mhpmcounter3h", "mhpmcounter4h", "mhpmcounter5h", "mhpmcounter6h", "mstatus" ,
              "mie" ,"mtvec", "mcountinhibit", "mhpmevent3", "mhpmevent4", "mhpmevent5", "mhpmevent6", "mscratch", "mepc" ,"mcause",  "mtval",
              "mip" ,"tselect" ,"tdata1", "tdata2", "mcycle", "misa", "mvendorid", "marchid", "mimpid", "mhartid" , 'fflags', 'frm', 'fcsr', 'RESERVED' , 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED', 'RESERVED']
              
	def report_phase(self):
		
		self.logger.info("*********Generate the Coverage Report*********")
		self.COVERAGE_RV32()
		self.coverage_summary()
		
	
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


			self.instr = dfC['INSTRUCTION_COUNT']
			self.list_rd = dfC['RD']
			self.list_rs1 = dfC['RS_1']
			self.list_rs2 = dfC['RS_2']
			self.imm_read = dfC['VALUES']
			self.INSTR_iteration = dfC['CSR_COUNT']
			

			
			for i in range(len(self.instruction_names)):
				self.values.append(0)
				self.reg_rd.append(0)
				self.reg_rs1.append(0)
				self.reg_rs2.append(0)
				self.imm_value.append(0)
				self.INSTR_iter.append(0)
				
			for i in range(len(self.instruction_names)):
				
				self.values[i] = self.instr[i]
				self.reg_rd[i] = self.list_rd[i]
				self.reg_rs1[i] = self.list_rs1[i]
				self.reg_rs2[i] = self.list_rs2[i]
				self.imm_value[i] = self.imm_read[i]
				self.INSTR_iter[i] = self.INSTR_iteration[i]
		else:
			
			for i in range(len(self.instruction_names)):
				self.values.append(0)
				self.reg_rd.append(0)
				self.reg_rs1.append(0)
				self.reg_rs2.append(0)
				self.imm_value.append(0)
				self.INSTR_iter.append(0)
		
	def COVERAGE_WORKING_RV32(self):

		for we in self.main_column:
			self.dlist.append(we[2:].zfill(8))
			self.xyz_list.append(bin(int(we[2:].zfill(8),16))[2:].zfill(32))

		for i in range(len(self.xyz_list)):
			if (self.xyz_list[i][25:32] == '0110111' or self.xyz_list[i][25:32] == '0010111' or self.xyz_list[i][25:32] == '1101111' or self.xyz_list[i][25:32] == '1100111' or self.xyz_list[i][25:32] == '0000011' or self.xyz_list[i][25:32] == '0100011' or self.xyz_list[i][25:32] == '0010011'):
				if(self.xyz_list[i][0] == '1'):
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
				self.reg_rd[(int(rd, 2))] = self.reg_rd[int(rd, 2)] + 1
				
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

				elif(((self.xyz_list[i][17:20] == '111')) and ((self.xyz_list[i][0:7] == '0000000'))):
					self.values[36] = self.values[36] + 1
									
				elif ((self.xyz_list[i][17:20] == '000') and (self.xyz_list[i][0:7] == '0000001')):
					self.values[37] = self.values[37] + 1
					
					
				elif ((self.xyz_list[i][17:20] == '001')and (self.xyz_list[i][0:7] == '0000001')):
					self.values[38] = self.values[38] + 1
					
					
				elif ((self.xyz_list[i][17:20] == '010') and (self.xyz_list[i][0:7] == '0000001')):
					self.values[39] = self.values[39] + 1
					
					
				elif ((self.xyz_list[i][17:20] == '011') and (self.xyz_list[i][0:7] == '0000001')):
					self.values[40] = self.values[40] + 1
					
				
				elif ((self.xyz_list[i][17:20] == '100') and (self.xyz_list[i][0:7] == '0000001')):
					self.values[41] = self.values[41] + 1
					
					
				elif ((self.xyz_list[i][17:20] == '101') and (self.xyz_list[i][0:7] == '0000001')):
					self.values[42] = self.values[42] + 1
					
					
				elif ((self.xyz_list[i][17:20] == '110') and (self.xyz_list[i][0:7] == '0000001')):
					self.values[43] = self.values[43] + 1
					
					
				else:
					self.values[44] = self.values[44] + 1

			elif ((self.xyz_list[i][25:32] == '1000011')): #FM ADD
				rd = self.xyz_list[i][20:25]
				self.reg_rd[(int(rd, 2))] = self.reg_rd[int(rd, 2)] + 1
				
				rs1 = self.xyz_list[i][12:17]
				self.reg_rs1[int(rs1, 2)] = self.reg_rs1[int(rs1, 2)] + 1
				
				rs2 = self.xyz_list[i][7:12]
				self.reg_rs2[int(rs2, 2)] = self.reg_rs2[int(rs2, 2)] + 1
				
				self.values[47] = self.values[47] + 1
				
				#add RS3 and RM
				
			elif ((self.xyz_list[i][25:32] == '1000111')): #FM SUB
				self.values[48] = self.values[48] + 1
				
				rd = self.xyz_list[i][20:25]
				self.reg_rd[(int(rd, 2))] = self.reg_rd[int(rd, 2)] + 1
				
				rs1 = self.xyz_list[i][12:17]
				self.reg_rs1[int(rs1, 2)] = self.reg_rs1[int(rs1, 2)] + 1
				
				rs2 = self.xyz_list[i][7:12]
				self.reg_rs2[int(rs2, 2)] = self.reg_rs2[int(rs2, 2)] + 1
				
				#add RS3 and RM
				
			elif ((self.xyz_list[i][25:32] == '1001011')): #FNM SUB
				self.values[49] = self.values[49] + 1
				
				rd = self.xyz_list[i][20:25]
				self.reg_rd[(int(rd, 2))] = self.reg_rd[int(rd, 2)] + 1
				
				rs1 = self.xyz_list[i][12:17]
				self.reg_rs1[int(rs1, 2)] = self.reg_rs1[int(rs1, 2)] + 1
				
				rs2 = self.xyz_list[i][7:12]
				self.reg_rs2[int(rs2, 2)] = self.reg_rs2[int(rs2, 2)] + 1
				
				#add RS3 and RM
				
			elif ((self.xyz_list[i][25:32] == '1001111')): #FNM ADD 
				self.values[50] = self.values[50] + 1
				
				rd = self.xyz_list[i][20:25]
				self.reg_rd[(int(rd, 2))] = self.reg_rd[int(rd, 2)] + 1
				
				rs1 = self.xyz_list[i][12:17]
				self.reg_rs1[int(rs1, 2)] = self.reg_rs1[int(rs1, 2)] + 1
				
				rs2 = self.xyz_list[i][7:12]
				self.reg_rs2[int(rs2, 2)] = self.reg_rs2[int(rs2, 2)] + 1
				
			elif ((self.xyz_list[i][25:32] == '1010011')): #F ADD till FMV.W.X 
			
				if(self.xyz_list[17:20] == '000'):
					self.imm_value[2] = self.imm_value[2] + 1
				elif(self.xyz_list[17:20] == '001'):
					self.imm_value[3] = self.imm_value[3] + 1
				elif(self.xyz_list[17:20] == '010'):
					self.imm_value[4] = self.imm_value[4] + 1
				elif(self.xyz_list[17:20] == '011'):
					self.imm_value[5] = self.imm_value[5] + 1
				elif(self.xyz_list[17:20] == '100'):
					self.imm_value[6] = self.imm_value[6] + 1
				else:
					self.imm_value[7] = self.imm_value[7] + 1
					
				if(self.xyz_list[i][0:7] == '0000000'): #FADD
					
				
					self.values[51] = self.values[51] + 1 
				
					rd = self.xyz_list[i][20:25]
					self.reg_rd[(int(rd, 2))] = self.reg_rd[int(rd, 2)] + 1
					
					rs1 = self.xyz_list[i][12:17]
					self.reg_rs1[int(rs1, 2)] = self.reg_rs1[int(rs1, 2)] + 1
					
					rs2 = self.xyz_list[i][7:12]
					self.reg_rs2[int(rs2, 2)] = self.reg_rs2[int(rs2, 2)] + 1
				
				
				elif(self.xyz_list[i][0:7] == '0000100'): #FSUB
				
					
					self.values[52] = self.values[52] + 1
				
					rd = self.xyz_list[i][20:25]
					self.reg_rd[(int(rd, 2))] = self.reg_rd[int(rd, 2)] + 1
					
					rs1 = self.xyz_list[i][12:17]
					self.reg_rs1[int(rs1, 2)] = self.reg_rs1[int(rs1, 2)] + 1
					
					rs2 = self.xyz_list[i][7:12]
					self.reg_rs2[int(rs2, 2)] = self.reg_rs2[int(rs2, 2)] + 1
					
				elif(self.xyz_list[i][0:7] == '0001000'): #FMUL
				
					self.values[53] = self.values[53] + 1
					
				
					rd = self.xyz_list[i][20:25]
					self.reg_rd[(int(rd, 2))] = self.reg_rd[int(rd, 2)] + 1
					
					rs1 = self.xyz_list[i][12:17]
					self.reg_rs1[int(rs1, 2)] = self.reg_rs1[int(rs1, 2)] + 1
					
					rs2 = self.xyz_list[i][7:12]
					self.reg_rs2[int(rs2, 2)] = self.reg_rs2[int(rs2, 2)] + 1
					
				elif(self.xyz_list[i][0:7] == '0001100'): #FDIV
				
					self.values[54] = self.values[54] + 1
					
				
					rd = self.xyz_list[i][20:25]
					self.reg_rd[(int(rd, 2))] = self.reg_rd[int(rd, 2)] + 1
					
					rs1 = self.xyz_list[i][12:17]
					self.reg_rs1[int(rs1, 2)] = self.reg_rs1[int(rs1, 2)] + 1
					
					rs2 = self.xyz_list[i][7:12] 
					self.reg_rs2[int(rs2, 2)] = self.reg_rs2[int(rs2, 2)] + 1
					
				elif(self.xyz_list[i][0:7] == '0101100'): #FSQRT and #condition for rs2
				
					self.values[55] = self.values[55] + 1
					
				
					rd = self.xyz_list[i][20:25]
					self.reg_rd[(int(rd, 2))] = self.reg_rd[int(rd, 2)] + 1
					
					rs1 = self.xyz_list[i][12:17]
					self.reg_rs1[int(rs1, 2)] = self.reg_rs1[int(rs1, 2)] + 1		
					
				elif((self.xyz_list[i][0:7] == '0010000') and (self.xyz_list[i][17:20] == '000')): #FSGNJ
				
					self.values[56] = self.values[56] + 1
					
				
					rd = self.xyz_list[i][20:25]
					self.reg_rd[(int(rd, 2))] = self.reg_rd[int(rd, 2)] + 1
					
					rs1 = self.xyz_list[i][12:17]
					self.reg_rs1[int(rs1, 2)] = self.reg_rs1[int(rs1, 2)] + 1
					
					rs2 = self.xyz_list[i][7:12]
					self.reg_rs2[int(rs2, 2)] = self.reg_rs2[int(rs2, 2)] + 1
					
				elif((self.xyz_list[i][0:7] == '0010000') and (self.xyz_list[i][17:20] == '001')): #FSGNJN
				
					self.values[57] = self.values[57] + 1
					
				
					rd = self.xyz_list[i][20:25]
					self.reg_rd[(int(rd, 2))] = self.reg_rd[int(rd, 2)] + 1
					
					rs1 = self.xyz_list[i][12:17]
					self.reg_rs1[int(rs1, 2)] = self.reg_rs1[int(rs1, 2)] + 1
					
					rs2 = self.xyz_list[i][7:12]
					self.reg_rs2[int(rs2, 2)] = self.reg_rs2[int(rs2, 2)] + 1
					
				elif((self.xyz_list[i][0:7] == '0010000') and (self.xyz_list[i][17:20] == '010')): #FSGNJX
				
					self.values[58] = self.values[58] + 1
					
				
					rd = self.xyz_list[i][20:25]
					self.reg_rd[(int(rd, 2))] = self.reg_rd[int(rd, 2)] + 1
					
					rs1 = self.xyz_list[i][12:17]
					self.reg_rs1[int(rs1, 2)] = self.reg_rs1[int(rs1, 2)] + 1
					
					rs2 = self.xyz_list[i][7:12]
					self.reg_rs2[int(rs2, 2)] = self.reg_rs2[int(rs2, 2)] + 1
					
				elif((self.xyz_list[i][0:7] == '0010100') and (self.xyz_list[i][17:20] == '000')): #FMIN
				
					self.values[59] = self.values[59] + 1
					
				
					rd = self.xyz_list[i][20:25]
					self.reg_rd[(int(rd, 2))] = self.reg_rd[int(rd, 2)] + 1
					
					rs1 = self.xyz_list[i][12:17]
					self.reg_rs1[int(rs1, 2)] = self.reg_rs1[int(rs1, 2)] + 1
					
					rs2 = self.xyz_list[i][7:12]
					self.reg_rs2[int(rs2, 2)] = self.reg_rs2[int(rs2, 2)] + 1
					
				elif((self.xyz_list[i][0:7] == '0010100') and (self.xyz_list[i][17:20] == '001')): #FMAX
				
					self.values[60] = self.values[60] + 1
					
				
					rd = self.xyz_list[i][20:25]
					self.reg_rd[(int(rd, 2))] = self.reg_rd[int(rd, 2)] + 1
					
					rs1 = self.xyz_list[i][12:17]
					self.reg_rs1[int(rs1, 2)] = self.reg_rs1[int(rs1, 2)] + 1
					
					rs2 = self.xyz_list[i][7:12]
					self.reg_rs2[int(rs2, 2)] = self.reg_rs2[int(rs2, 2)] + 1
					
				elif(self.xyz_list[i][0:7] == '1100000'): #FCVT
				
					if (self.xyz_list[i][7:12] == '00000'):
						

						rd = self.xyz_list[i][20:25]
						self.reg_rd[(int(rd, 2))] = self.reg_rd[int(rd, 2)] + 1
						
						rs1 = self.xyz_list[i][12:17]
						self.reg_rs1[int(rs1, 2)] = self.reg_rs1[int(rs1, 2)] + 1
						
						rs2 = self.xyz_list[i][7:12]
						self.reg_rs2[int(rs2, 2)] = self.reg_rs2[int(rs2, 2)] + 1
						
						self.values[61] = self.values[61] + 1
					else:
						pass
					
				elif((self.xyz_list[i][0:7] == '1100000')): #FCVT WU S
					
					
					if (self.xyz_list[i][7:12] == '00001'):

						rd = self.xyz_list[i][20:25]
						self.reg_rd[(int(rd, 2))] = self.reg_rd[int(rd, 2)] + 1
						
						rs1 = self.xyz_list[i][12:17]
						self.reg_rs1[int(rs1, 2)] = self.reg_rs1[int(rs1, 2)] + 1
						
						rs2 = self.xyz_list[i][7:12]
						self.reg_rs2[int(rs2, 2)] = self.reg_rs2[int(rs2, 2)] + 1
						
						self.values[62] = self.values[62] + 1
					else:
						pass
						
						
				elif((self.xyz_list[i][0:7] == '1110000')): #FMV X W
					
					
					if ((self.xyz_list[i][7:12] == '00001') and (self.xyz_list[i][17:20] == '000')):

						rd = self.xyz_list[i][20:25]
						self.reg_rd[(int(rd, 2))] = self.reg_rd[int(rd, 2)] + 1
						
						rs1 = self.xyz_list[i][12:17]
						self.reg_rs1[int(rs1, 2)] = self.reg_rs1[int(rs1, 2)] + 1
						
						rs2 = self.xyz_list[i][7:12]
						self.reg_rs2[int(rs2, 2)] = self.reg_rs2[int(rs2, 2)] + 1
						
						self.values[63] = self.values[63] + 1
					else:
						pass
						
				elif((self.xyz_list[i][0:7] == '1010000')): #FEQ , FLT, FLE
						rd = self.xyz_list[i][20:25]
						self.reg_rd[(int(rd, 2))] = self.reg_rd[int(rd, 2)] + 1
						
						rs1 = self.xyz_list[i][12:17]
						self.reg_rs1[int(rs1, 2)] = self.reg_rs1[int(rs1, 2)] + 1
						
						rs2 = self.xyz_list[i][7:12]
						self.reg_rs2[int(rs2, 2)] = self.reg_rs2[int(rs2, 2)] + 1
						
						
						if (self.xyz_list[i][17:20] == '010'): #FEQ
							self.values[64] = self.values[64] + 1
						
						elif (self.xyz_list[i][17:20] == '001'): #FLT
							self.values[65] = self.values[65] + 1
						
						elif (self.xyz_list[i][17:20] == '000'): #FLE
							self.values[66] = self.values[66] + 1
						else:
							pass
		
				elif((self.xyz_list[i][0:7] == '1110000')):
					
					
					if ((self.xyz_list[i][7:12] == '00000') and (self.xyz_list[i][17:20] == '001')): #FCLASS

						rd = self.xyz_list[i][20:25]
						self.reg_rd[(int(rd, 2))] = self.reg_rd[int(rd, 2)] + 1
						
						rs1 = self.xyz_list[i][12:17]
						self.reg_rs1[int(rs1, 2)] = self.reg_rs1[int(rs1, 2)] + 1
						
						self.values[67] = self.values[67] + 1
					else:
						pass
						
				elif((self.xyz_list[i][0:7] == '1101000')):
					
					if ((self.xyz_list[i][7:12] == '00000')): #FCVT S

						rd = self.xyz_list[i][20:25]
						self.reg_rd[(int(rd, 2))] = self.reg_rd[int(rd, 2)] + 1
						
						rs1 = self.xyz_list[i][12:17]
						self.reg_rs1[int(rs1, 2)] = self.reg_rs1[int(rs1, 2)] + 1
						
						self.values[68] = self.values[68] + 1
						
						
					
				elif((self.xyz_list[i][0:7] == '1101000')):
					if ((self.xyz_list[i][7:12] == '00001')): #FCVT S WU

						rd = self.xyz_list[i][20:25]
						self.reg_rd[(int(rd, 2))] = self.reg_rd[int(rd, 2)] + 1
						
						rs1 = self.xyz_list[i][12:17]
						self.reg_rs1[int(rs1, 2)] = self.reg_rs1[int(rs1, 2)] + 1
						
						self.values[69] = self.values[69] + 1
						
						
				elif((self.xyz_list[i][0:7] == '1111000')):
					if ((self.xyz_list[i][7:12] == '00000') and (self.xyz_list[i][17:20] == '000')): #FMV W X

						rd = self.xyz_list[i][20:25]
						self.reg_rd[(int(rd, 2))] = self.reg_rd[int(rd, 2)] + 1
						
						rs1 = self.xyz_list[i][12:17]
						self.reg_rs1[int(rs1, 2)] = self.reg_rs1[int(rs1, 2)] + 1
						
						self.values[70] = self.values[70] + 1

			elif ((self.xyz_list[i][25:32] == '1110011')): #CSR INSTR
				if (self.xyz_list[i][0:12] == '101100000010'):
					self.INSTR_iter[0] = self.INSTR_iter[0] + 1 #minstret
				
				elif (self.xyz_list[i][0:12] == '101100000011'):
					self.INSTR_iter[1] = self.INSTR_iter[1] + 1 #mhpm 3
				
				elif (self.xyz_list[i][0:12] == '101100000100'):
					self.INSTR_iter[2] = self.INSTR_iter[2] + 1 #mhpm 4
					
				elif (self.xyz_list[i][0:12] == '101100000101'):
					self.INSTR_iter[3] = self.INSTR_iter[3] + 1 #mhpm 5
					
				elif (self.xyz_list[i][0:12] == '101100000110'):
					self.INSTR_iter[4] = self.INSTR_iter[4] + 1 #mhpm 6
					
				elif (self.xyz_list[i][0:12] == '101110000000'):
					self.INSTR_iter[5] = self.INSTR_iter[5] + 1 #mcycleh
					
				elif (self.xyz_list[i][0:12] == '101110000010'):
					self.INSTR_iter[6] = self.INSTR_iter[6] + 1 #minstreth
				
				elif (self.xyz_list[i][0:12] == '101110000011'):
					self.INSTR_iter[7] = self.INSTR_iter[7] + 1 #mhpm 3h
					
				elif (self.xyz_list[i][0:12] == '101110000100'):
					self.INSTR_iter[8] = self.INSTR_iter[8] + 1 #mhpm 4h
					
				elif (self.xyz_list[i][0:12] == '101110000101'):
					self.INSTR_iter[9] = self.INSTR_iter[9] + 1 #mhpm 5h
					
				elif (self.xyz_list[i][0:12] == '101110000110'):
					self.INSTR_iter[10] = self.INSTR_iter[10] + 1 #mhpm 6h
				
				elif (self.xyz_list[i][0:12] == '001100000000'):
					self.INSTR_iter[11] = self.INSTR_iter[11] + 1 #mstatus
					
				elif (self.xyz_list[i][0:12] == '001100000100'):
					self.INSTR_iter[12] = self.INSTR_iter[12] + 1 #mie
			
				elif (self.xyz_list[i][0:12] == '001100000101'):
					self.INSTR_iter[13] = self.INSTR_iter[13] + 1 #mtvec
					
				elif (self.xyz_list[i][0:12] == '001100100000'):
					self.INSTR_iter[14] = self.INSTR_iter[14] + 1 #mcountinhibit
					
				elif (self.xyz_list[i][0:12] == '001100100011'):
					self.INSTR_iter[15] = self.INSTR_iter[15] + 1 #mhpmevent3
					
				elif (self.xyz_list[i][0:12] == '001100100100'):
					self.INSTR_iter[16] = self.INSTR_iter[16] + 1 #mhpmevent4
					
				elif (self.xyz_list[i][0:12] == '001100100101'):
					self.INSTR_iter[17] = self.INSTR_iter[17] + 1 #mhpmevent5
					
				elif (self.xyz_list[i][0:12] == '001100100110'):
					self.INSTR_iter[18] = self.INSTR_iter[18] + 1 #mhpmevent6
					
				elif (self.xyz_list[i][0:12] == '001101000000'):
					self.INSTR_iter[19] = self.INSTR_iter[19] + 1 #mscracth
					
				elif (self.xyz_list[i][0:12] == '001101000001'):
					self.INSTR_iter[20] = self.INSTR_iter[20] + 1 #mepc
					
				elif (self.xyz_list[i][0:12] == '001101000010'):
					self.INSTR_iter[21] = self.INSTR_iter[21] + 1 #mcause
					
				elif (self.xyz_list[i][0:12] == '001101000011'):
					self.INSTR_iter[22] = self.INSTR_iter[22] + 1 #mtval
				
				elif (self.xyz_list[i][0:12] == '001101000100'):
					self.INSTR_iter[23] = self.INSTR_iter[23] + 1 #mip
					
				elif (self.xyz_list[i][0:12] == '011110100000'):
					self.INSTR_iter[24] = self.INSTR_iter[24] + 1 #tselect
					
				elif (self.xyz_list[i][0:12] == '011110100001'):
					self.INSTR_iter[25] = self.INSTR_iter[25] + 1 #tdata
					
				elif (self.xyz_list[i][0:12] == '011110100010'):
					self.INSTR_iter[26] = self.INSTR_iter[26] + 1 #tdata2
				
				elif (self.xyz_list[i][0:12] == '101100000000'):
					self.INSTR_iter[27] = self.INSTR_iter[27] + 1 #mcycle
					
				elif (self.xyz_list[i][0:12] == '001100000001'):
					self.INSTR_iter[28] = self.INSTR_iter[28] + 1 #misa
					
					
				elif (self.xyz_list[i][0:12] == '111100010001'):
					self.INSTR_iter[29] = self.INSTR_iter[29] + 1 #mvendriod
					
				elif (self.xyz_list[i][0:12] == '111100010010'):
					self.INSTR_iter[30] = self.INSTR_iter[30] + 1 #marchid
					
												
				elif (self.xyz_list[i][0:12] == '111100010011'):
					self.INSTR_iter[31] = self.INSTR_iter[31] + 1 #mimpid
					
				elif (self.xyz_list[i][0:12] == '111100010100'):
					self.INSTR_iter[32] = self.INSTR_iter[32] + 1 #mhartid
					
				elif (self.xyz_list[i][0:12] == '000000000001'):
					self.INSTR_iter[33] = self.INSTR_iter[33] + 1 #mhartid
					
				elif (self.xyz_list[i][0:12] == '000000000010'):
					self.INSTR_iter[34] = self.INSTR_iter[34] + 1 #mhartid
					
				elif (self.xyz_list[i][0:12] == '000000000011'):
					self.INSTR_iter[35] = self.INSTR_iter[35] + 1 #mhartid


				if(self.xyz_list[i][17:20] == '001'): #CSRRW
					rd = self.xyz_list[i][20:25]
					self.reg_rd[(int(rd, 2))] = self.reg_rd[int(rd, 2)] + 1 
					rs1 = self.xyz_list[i][12:17]
					self.reg_rs1[int(rs1, 2)] = self.reg_rs1[int(rs1, 2)] + 1
					
					self.values[71] = self.values[71] + 1
					
				elif(self.xyz_list[i][17:20] == '010'): #CSRRS
					rd = self.xyz_list[i][20:25]
					self.reg_rd[(int(rd, 2))] = self.reg_rd[int(rd, 2)] + 1
					rs1 = self.xyz_list[i][12:17]
					self.reg_rs1[int(rs1, 2)] = self.reg_rs1[int(rs1, 2)] + 1
					
					self.values[72] = self.values[72] + 1
					
				elif(self.xyz_list[i][17:20] == '011'): #CSRRC
					rd = self.xyz_list[i][20:25]
					self.reg_rd[(int(rd, 2))] = self.reg_rd[int(rd, 2)] + 1
					rs1 = self.xyz_list[i][12:17]
					self.reg_rs1[int(rs1, 2)] = self.reg_rs1[int(rs1, 2)] + 1
					
					self.values[73] = self.values[73] + 1
					
				elif(self.xyz_list[i][17:20] == '101'): #CSRRWI
					rd = self.xyz_list[i][20:25]
					self.reg_rd[(int(rd, 2))] = self.reg_rd[int(rd, 2)] + 1
					
					self.values[74] = self.values[74] + 1
					
				elif(self.xyz_list[i][17:20] == '110'): #CSRRSI
					rd = self.xyz_list[i][20:25]
					self.reg_rd[(int(rd, 2))] = self.reg_rd[int(rd, 2)] + 1
					
					self.values[75] = self.values[75] + 1
					
				elif(self.xyz_list[i][17:20] == '111'): #CSRRCI
					rd = self.xyz_list[i][20:25]
					self.reg_rd[(int(rd, 2))] = self.reg_rd[int(rd, 2)] + 1
					
					self.values[76] = self.values[76] + 1
			else:
				#remember to shift e-call to last value
				self.values[77] = self.values[77] + 1

		my_series = pd.Series(self.values)
		
		DICT = {'NAMES_OF_INSTR': self.instruction_names , 'INSTRUCTION_COUNT': self.values , 'REGISTER_NAMES': self.names_of_registers, 'RD': self.reg_rd, 'RS_1': self.reg_rs1, 'RS_2': self.reg_rs2, 'MISSCELENOUS': self.list_imm, 'VALUES' : self.imm_value, 'CSR_NUMBER_NAMES' : self.list_INSTR,'CSR_COUNT' : self.INSTR_iter}
		

		self.dfb = pd.DataFrame.from_dict(DICT)
		self.covg = directory()
		self.dfb.to_csv(self.covg)
		return self.values , self.instruction_names, self.names_of_registers,self.reg_rd,self.reg_rs1,self.reg_rs2
		
	def coverage_summary(self):
		
		values, instr_name, name_reg, rd, rs1, rs2 = self.COVERAGE_WORKING_RV32()
		RV32I_zero = 0
		RV32I_one = 0
		RV32M_zero = 0
		RV32M_one = 0
		RV32F_zero = 0
		RV32F_one = 0
		csr_zero = 0
		csr_one = 0
		total_values_I = len(values)
		total_values_M = len(values)
		total_values_F = len(values)
		total_values_csr = len(values) 
		rd_one = 0
		rd_zero = 0
		rs1_one = 0
		rs1_zero = 0
		rs2_one = 0
		rs2_zero = 0
		
		f_rd_one = 0
		f_rd_zero = 0
		f_rs1_one = 0
		f_rs1_zero = 0
		f_rs2_one = 0
		f_rs2_zero = 0
		
		total_rd = len(rd)
		total_rs1 = len(rs1)
		total_rs2 = len(rs2)
		
		for i in range(33):  
			if name_reg[i] and rd[i] == 0:  # Check the value at index 
				rd_zero += 1
			elif name_reg[i] and rd[i] >1:  # Check the value at index i
				rd_one += 1
			else:
				pass

		for i in range(33):
			if name_reg[i] and rs1[i] == 0:  # Check the value at index i
				rs1_zero += 1
			elif name_reg[i] and rs1[i] >1:  # Check the value at index i
				rs1_one += 1
			else:
				pass

		for i in range(33):
			if name_reg[i] and rs2[i] == 0:  # Check the value at index i
				rs2_zero += 1
			elif name_reg[i] and rs2[i] >1:  # Check the value at index i
				rs2_one += 1
			else:
				pass
				
		for i in range(32, 64):  
			if name_reg[i] and rd[i] == 0:  # Check the value at index 
				f_rd_zero += 1
			elif name_reg[i] and rd[i] >1:  # Check the value at index i
				f_rd_one += 1
				
			else:
				pass
				

		for i in range(32, 64):
			if name_reg[i] and rs1[i] == 0:  # Check the value at index i
				f_rs1_zero += 1
			elif name_reg[i] and rs1[i] >1:  # Check the value at index i
				f_rs1_one += 1
				
			else:
				pass

		for i in range(32, 64):
			if name_reg[i] and rs2[i] == 0:  # Check the value at index i
				f_rs2_zero += 1
			elif name_reg[i] and rs2[i] >1:  # Check the value at index i
				f_rs2_one += 1
				
			else:
				pass
				
		percentage_rd_zero = round((rd_zero / 32) * 100, 2)
		percentage_rd_one = round((rd_one / 32) * 100, 2)
		
		percentage_rs1_zero = round((rs1_zero / 32) * 100, 2)
		percentage_rs1_one = round((rs1_one / 32) * 100, 2)
		
		percentage_rs2_zero = round((rs2_zero / 32) * 100, 2)
		percentage_rs2_one = round((rs2_one / 32) * 100, 2)
		
		percentage_f_rd_zero = round((f_rd_zero / 32) * 100, 2)
		percentage_f_rd_one = round((f_rd_one / 32) * 100, 2)
		
		percentage_f_rs1_zero = round((f_rs1_zero / 32) * 100, 2)
		percentage_f_rs1_one = round((f_rs1_one / 32) * 100, 2)
		
		percentage_f_rs2_zero = round((f_rs2_zero / 32) * 100, 2)
		percentage_f_rs2_one = round((f_rs2_one / 32) * 100, 2)

		for i in range(37):  # Iterate over the first 36 elements
		    
		    if instr_name[i] and values[i] == 0:  # Check the value at index i
		        RV32I_zero += 1
		        
		    elif instr_name[i] and values[i] >1:  # Check the value at index i
		        RV32I_one += 1
		    else:
		        #print("INVALID CONDITION")
		        pass
		        
		for i in range(37, 45):  # Iterate over the 37-44 elements
		    
		    if instr_name[i] and values[i] == 0:  # Check the value at index i
		        RV32M_zero += 1
		       
		    elif instr_name[i] and values[i] >1:  # Check the value at index i
		        RV32M_one += 1
		    else:
		        #print("INVALID CONDITION")
		        pass
		        
		for i in range(45, 71):  # Iterate over the first 45-70 elements
		    
		    if instr_name[i] and values[i] == 0:  # Check the value at index i
		        RV32F_zero += 1
		    elif instr_name[i] and values[i] >1:  # Check the value at index i
		        RV32F_one += 1
		    else:
		        #print("INVALID CONDITION")
		        pass
		for i in range(71,77):  # Iterate over the 71-77 element
		    if instr_name[i] and values[i] == 0:  # Check the value at index i
		        csr_zero += 1
		    elif instr_name[i] and values[i] >1:  # Check the value at index i
		        csr_one += 1
		    else:
		        pass
		        #print("INVALID CONDITION")
		RV32_I = RV32I_one + csr_one
		

		percentage_RV32I_zero = round((RV32I_zero / total_values_I) * 100, 2)
		percentage_RV32I_one = round(((RV32I_one+csr_one) / 43) * 100, 2)
		
		percentage_RV32M_zero = round((RV32M_zero / total_values_M) * 100, 2)
		percentage_RV32M_one = round((RV32M_one / 8) * 100, 2)
		
		percentage_RV32F_zero = round((RV32F_zero / total_values_F) * 100, 2)
		percentage_RV32F_one = round((RV32F_one / 26) * 100, 2)
		
		percentage_csr_zero = round((csr_zero / total_values_csr) * 100, 2)
		percentage_csr_one = round((csr_one / 6) * 100, 2)
		

		total_percentage_I = round(((RV32I_zero + RV32I_one) / total_values_I) * 100, 2)
		total_percentage_M = round(((RV32M_zero + RV32M_one) / total_values_M) * 100, 2)
		total_percentage_F = round(((RV32F_zero + RV32F_one) / total_values_F) * 100, 2)
		total_percentage_csr = round(((csr_zero + csr_one) / total_values_csr) * 100, 2)
		
		TOTAL_PERCENTAGE = round((percentage_RV32I_one + percentage_RV32M_one+ percentage_RV32F_one + percentage_csr_one), 2)
		
		folder = 'log/Coverage'
		file_path = os.path.join(folder, "coverage_summary.txt")
		file = open(file_path,"w")
		
		# Here we write the summary of coverage
		file.write("\n\t***********************************************************")
		file.write("\n\t\t******This is the summary of Coverage report******\n")
		
		# This is the information of RV32_I
		file.write(f'\t\  Coverage_Group\t Coverage_Percenatage\t Coverage_Stats')
		file.write(f'\n\t    RV32I\t\t      {percentage_RV32I_one }%\t\t     {RV32_I}/43')
		file.write(f'\n\t    RV32M\t\t      {percentage_RV32M_one }%\t\t     {RV32M_one}/8')
		file.write(f'\n\t    RV32F\t\t      {percentage_RV32F_one }%\t\t     {RV32F_one}/26')
		file.write("\n\t***********************************************************")
		
		file.write("\n\t***********************************************************")
		file.write("\n\t\t******This is the summary of Coverage report (REGISTERS) ******\n")
		file.write(f'\t\  REGISTERS\t Coverage_Percenatage\t Coverage_Stats')
		file.write(f'\n\t    RD\t\t      {percentage_rd_one }%\t\t     {rd_one}/32')
		file.write(f'\n\t    RS1\t\t      {percentage_rs1_one }%\t\t     {rs1_one}/32')
		file.write(f'\n\t    RS2\t\t      {percentage_rs2_one }%\t\t     {rs2_one}/32')
		file.write("\n\t***********************************************************")
		
		file.write("\n\t***********************************************************")
		file.write("\n\t\t******This is the summary of Coverage report (FLOATING-POINT REGISTERS) ******\n")
		file.write(f'\t\  REGISTERS\t Coverage_Percenatage\t Coverage_Stats')
		file.write(f'\n\t    RD\t\t      {percentage_f_rd_one }%\t\t     {f_rd_one}/32')
		file.write(f'\n\t    RS1\t\t      {percentage_f_rs1_one }%\t\t     {f_rs1_one}/32')
		file.write(f'\n\t    RS2\t\t      {percentage_f_rs2_one }%\t\t     {f_rs2_one}/32')
		file.write("\n\t***********************************************************")
		file.close()
		
