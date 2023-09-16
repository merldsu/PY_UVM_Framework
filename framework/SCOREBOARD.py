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
from cocotb.triggers import ClockCycles
from pyuvm import *

import pandas as pd
import numpy as np
import csv
import logging
import Script as sp 
import os
from datetime import datetime 
import shutil
import time

class Scoreboard(uvm_component):

	
	# define the uvm phases function	
	def check_phase(self):
		self.logger.info('**********Execution Scoreboard**********')
		self.rv32_read_csv()
		self.logger.info('Read CSV file from ISS (Scoreboard)')
		self.logger.info('Read CSV file from RTL (Scoreboard)')
		self.report_score()
		self.logger.info('LOG the Results (Scoreboard)')

	# Create the function where we read two different CSV	
	def rv32_read_csv(self):
		
		#import RTL_CSV and ISS_CSV file
		self.df_RTL= pd.read_csv('RESULT_MONITOR.csv')
		self.df_ISS = pd.read_csv('ISS.csv')
		


		# Read the coloumns from RTL CSV (Monitor)
		
		

		self.RTL_INSTR_RV32 = self.df_RTL['INSTR_RES_MON'].tolist()
		self.RTL_RESULT_RV32 = self.df_RTL['RESULT_MONITOR'].tolist()
		
		
		# Read the coloumns from ISS CSV

		#ISS_PC_RV32 = df_ISS['PC'].tolist()
		self.ISS_INSTR_RV32 = self.df_ISS['INSTRUCTION'].tolist()
		self.ISS_RESULT_RV32 = self.df_ISS['RESULT_ISS'].tolist()
		self.ISS_ASS_RV32 = self.df_ISS['INSTR_ASSEMBLY'].tolist()
		
		n_iss_instr = 3
		n_iss_res = 3
		n_iss_assem = 3
		del self.ISS_INSTR_RV32[len(self.ISS_INSTR_RV32) - n_iss_instr :]
		del self.ISS_RESULT_RV32[len(self.ISS_RESULT_RV32) - n_iss_res  :]
		del self.ISS_ASS_RV32[len(self.ISS_ASS_RV32) - n_iss_assem  :]
		
		#self.ISS_INSTR_RV32.append('0x00000073')
		#self.ISS_RESULT_RV32.append('0x00000000')
		#self.ISS_ASS_RV32.append('ecall')
		
		return self.RTL_INSTR_RV32, self.RTL_RESULT_RV32, self.ISS_INSTR_RV32 , self.ISS_RESULT_RV32 , self.ISS_ASS_RV32

	# define the function where we compare the Results of ISS & RTL	
	def COMP(self,ins_rtl,ins_iss,res_rtl,res_iss):
		self.logger.info('Comparing the Results (***Scoreboard***)')
		list_status=[]
		for x in range(len(ins_rtl)):
			if (ins_rtl[x] == ins_iss[x] and res_rtl[x] == res_iss[x]):
				status="True"
				list_status.append(status)
			else:
				status="False"
				list_status.append(status)	
		return list_status

	# where generate the status of True or False
	def Status(self,RV32_Status):
			status_RV32_T = RV32_Status.count("True")
			status_RV32_F = RV32_Status.count("False")
			
			return status_RV32_T,status_RV32_F
	
	# Here we define the function that is responsible to generate CSV
	def report_score(self):
			
		self.inst_rtl , self.result_rtl , self.inst_iss , self.result_iss , self.ass_rv32 = self.rv32_read_csv()
		test_itr = 63		
		COMP_RTL_ISS = self.COMP(self.inst_rtl, self.inst_iss , self.result_rtl  , self.result_iss )
		stT,stF=self.Status(COMP_RTL_ISS)
		
		self.logger.info(f"The total Number of Instructions:{len(self.inst_rtl) - test_itr}") 
		self.logger.info(f"The total Number of Instructions Passed:{stT - test_itr}")
		self.logger.info(f"The total Number of Instructions Failed:{stF}")
		
		seed = cocotb.RANDOM_SEED
		now = datetime.now()
		Date = now.strftime('%Y-%m-%d')
		Time = now.strftime('%H-%M-%S')

		if stF > 0:
			status_r = "Fail"
		else:
			status_r = "Pass"
		
		formatted_info = f" {Date:<12} {Time:<12}     {os.getenv('Test','riscv_random_test'):<24}         {os.getenv('Iteration','10'):<28} {seed:<24}        {status_r}"
		sp.over_all_report(formatted_info)

		df_Sc=pd.DataFrame({'RTL_INSTR': self.inst_rtl,'ISS_INSTR': self.inst_iss,'RTL_RESULT': self.result_rtl,'ISS_RESULT': self.result_iss,"INSTR_ASSEMBLY" : self.ass_rv32 ,"STATUS":COMP_RTL_ISS})	
		df_Sc.to_csv('Final_Results.csv',index=False)	

