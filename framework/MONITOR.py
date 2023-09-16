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
import pyuvm
from pyuvm import *
from cocotb.triggers import Timer, FallingEdge, RisingEdge
import pandas as pd
import io


def get_int(signal):
	try:
		sig = int(signal.value)
	except ValueError:
		sig = 0
	return sig
	
class MONITOR(uvm_component):

	def build_phase(self):
		pass
	
class MONITOR_RV32(MONITOR):

	def build_phase(self):
		
		self.bfm=ConfigDB().get(self,"","bfm")
		self.gp_Sequencer = uvm_blocking_get_port("gp_Sequencer",self)

		
		self.array_pc = 0
		self.array_instruction = 0
		self.array_results = 0
		
		self.terminate = 0
		
	async def run_phase(self):
	
		self.raise_objection()
		self.logger.info("**********Execution Monitor**********")
		
		await FallingEdge(self.bfm.dut.rst)
		
		self.logger.info("Instructions is Receiving from RTL through BFM at Run Time (***CMD Monitor***)")
		
		while(self.terminate == 0):

			send_pc , send_instr = await self.gp_Sequencer.get()
			rec_PC , rec_Instr = await self.bfm.command_monitor()


			if (send_pc != rec_PC) :
				raise AssertionError(send_pc ,"PC is not same",rec_PC)
			
			elif (send_instr != rec_Instr):
				raise AssertionError(send_instr,"Instr is not same",rec_Instr)			
		
			
			if (rec_Instr == "0x00000073"):
				self.terminate = 1

		self.array_pc,self.array_instruction ,self.array_results = await self.bfm.result_monitor()
		self.drop_objection()
		
	def extract_phase(self):
		
		self.logger.info("Executing the Report for RTL (***RESULT Monitor***)")
		df_RES_MON=pd.DataFrame({"INSTR_ADD_RES_MON":self.array_pc,"INSTR_RES_MON": self.array_instruction , "RESULT_MONITOR": self.array_results})
		df_RES_MON.to_csv("RESULT_MONITOR.csv",index=False)
		
class MONITOR_SWERV(MONITOR):

	def build_phase(self):
		
		self.bfm=ConfigDB().get(self,"","bfm")
		
	async def run_phase(self):
	
		self.raise_objection()
		self.logger.info("**********Execution Monitor**********")
		await  self.bfm.result_monitor()
		self.drop_objection()	
		
	def extract_phase(self):
	#LISTS
		list_GPR = []
		list_x = []
		list_NBL = []
		list_NBS = []
		list_NBD = []
		value = []
		list_CSR = []
		symbol = []

		NBL_s = []
		NBS = []
		NBD = []
		CSR = []

		#VARIABLES

		#counters for result monitor
		a = 0
		a1 = 0
		a2 = 0
		a3 = 0

		lw = 0
		sw = 0
		csr = 0
		etc = 0


		df_exec = pd.read_csv('exec.log',sep=':', header=None, engine='python')
		df_exec = df_exec.drop([0])
		df_exec = df_exec.loc[1:,:]
		df_exec = df_exec.stack().str.replace(';',',').unstack()
		df_exec = df_exec.stack().str.replace('           ',',xxxxxxxxx,').unstack()
		df_exec = df_exec.stack().str.replace('              ;',',xxxxxxxx').unstack()
		df_exec = df_exec.stack().str.replace(',xxxxxxxxx,,xxxxxxxxx,',',xxxxxx,x,xxxxxxxx,xxxxxxxx,,').unstack()
		df_exec = df_exec.stack().str.replace('                         ',',xx,x,xxxxxxxx,xxxxxxxx,,').unstack()
		df_exec = df_exec.stack().str.replace('xxxxxxxxx','x').unstack()
		df_exec = df_exec.stack().str.replace(',        ','').unstack()
		df_exec = df_exec.stack().str.replace('         ','     ').unstack()
		df_exec = df_exec.stack().str.replace(' ','  ').unstack()
		df_exec = df_exec.stack().str.replace('  ',',').unstack()
		df_exec = df_exec.stack().str.replace(',,',',').unstack()
		df_exec = df_exec.stack().str.replace(',,,',',').unstack()
		df_exec = df_exec.stack().str.replace(',,,,',',').unstack()
		df_exec = df_exec.stack().str.replace(',,,,,',',').unstack()
		df_exec = df_exec.stack().str.replace(',,,,,,',',').unstack()
		df_exec = df_exec.stack().str.replace(',,,,,,,',',').unstack()
		df_exec = df_exec.stack().str.replace(',,,,,,,,',',').unstack()
		df_exec = df_exec.stack().str.replace(',,',',').unstack()
		df_exec = df_exec.stack().str.replace(',,',',').unstack()
		df_exec = df_exec.stack().str.replace('=',':').unstack()

		df_exec = df_exec[1].str.split(',', expand=True)
		df_exec = df_exec.loc[:,[3,4,5,6]]
		df_exec.columns = ['PC','INSTR_RES_MON','RESULT_MONITOR','NBL']
		df_exec.loc[:, 'SYMBOL'] = pd.Series(NBL_s + NBD + NBS + CSR, dtype='float64')
		df_exec = df_exec.reset_index(drop=True)

		for j in range(len(df_exec['PC'])):
			if (df_exec['NBL'][j] == 'nbL'):
				
				
				if ((df_exec['RESULT_MONITOR'][j][0:5]) == "zero:"):
					#list_NBL.append(df_exec['RESULT_MONITOR'][j])
					df_exec.drop([j], inplace=True)
				else:
					NBL_s.append(df_exec['NBL'][j])
					list_NBL.append(df_exec['RESULT_MONITOR'][j])
					df_exec.drop([j], inplace=True)

		####### THIS LINE IS BEING ADDED

			elif (df_exec['NBL'][j] == 'nbL+1'):
				NBL_s.append(df_exec['NBL'][j])
				list_NBL.append(df_exec['RESULT_MONITOR'][j])
				df_exec.drop([j], inplace=True)

			elif (df_exec['NBL'][j] == 'nbD+0'):

				NBD.append(df_exec['NBL'][j])
				#if ((df_exec['RESULT_MONITOR'][j][0:5]) == "zero:"):
				list_NBD.append(df_exec['RESULT_MONITOR'][j])
				df_exec.drop([j], inplace=True)
				#else:
					#list_NBD.append(df_exec['RESULT_MONITOR'][j])
					#df_exec.drop([j], inplace=True)


			elif (df_exec['NBL'][j] == 'nbD+1'):
				NBD.append(df_exec['NBL'][j])
				list_NBD.append(df_exec['RESULT_MONITOR'][j])
				df_exec.drop([j], inplace=True)

			elif df_exec['NBL'][j] == 'nbS':
				NBS.append(df_exec['NBL'][j])
				if ((df_exec['RESULT_MONITOR'][j][0:5]) == "zero:"):
					list_NBS.append(df_exec['RESULT_MONITOR'][j])
					df_exec.drop([j], inplace=True)


				else:
					list_NBS.append(df_exec['RESULT_MONITOR'][j])
					df_exec.drop([j], inplace=True)


			elif df_exec['NBL'][j] == 'csr':
				CSR.append(df_exec['NBL'][j])
				if ((df_exec['RESULT_MONITOR'][j][0:5]) == "zero:"):
					list_CSR.append(df_exec['RESULT_MONITOR'][j])
					df_exec.drop([j], inplace=True)
				else:
					list_CSR.append(df_exec['RESULT_MONITOR'][j])
					df_exec.drop([j], inplace=True)
			else:
				pass
		df_exec = df_exec.reset_index(drop=True)
		for u in range(len(df_exec['INSTR_RES_MON'])):
			value.append(bin(int(str(df_exec['INSTR_RES_MON'][u]), 16))[2:].zfill(32))

		for i in range(len(df_exec['INSTR_RES_MON'])):
			if (df_exec['RESULT_MONITOR'][i] == 'x') and (value[i][25:32] == '0000011'):
				df_exec.loc[i, 'RESULT_MONITOR'] = list_NBL[a]
				symbol.append(NBL_s[a])
				a += 1
				

			elif (df_exec['RESULT_MONITOR'][i] == 'x') and (value[i][25:32] == '0100011'):
				df_exec.loc[i, 'RESULT_MONITOR'] = list_NBS[a1]
				symbol.append(NBS[a1])
				a1 += 1
				

			elif (df_exec['RESULT_MONITOR'][i] == 'x') and (value[i][25:32] == '0110011'):
				df_exec.loc[i, 'RESULT_MONITOR'] = list_NBD[a2]
				symbol.append(NBD[a2])
				a2 += 1
				

			elif (df_exec['RESULT_MONITOR'][i] == 'x') and (value[i][25:32] == '1110011'):
				df_exec.loc[i, 'RESULT_MONITOR'] = list_CSR[a3]
				symbol.append(CSR[a3])
				a3 += 1
				
			else:
				symbol.append('')
		df_exec = df_exec.reset_index(drop=True)
		df_exec['SYMBOL'] = pd.Series(symbol)

		for i in range(len(value)):
			if (df_exec['RESULT_MONITOR'].loc[i][:5] == "zero:"):
				df_exec['RESULT_MONITOR'][i] = '00000000'
			elif ((df_exec['RESULT_MONITOR'][i][:4]) == "s10:" or (df_exec['RESULT_MONITOR'][i][:4]) == "s11:"):
				df_exec['RESULT_MONITOR'][i] = df_exec['RESULT_MONITOR'][i][4:]
			
			#adding this line for F_extension
			
			elif ((df_exec['RESULT_MONITOR'][i][:5]) == "ft10:" or (df_exec['RESULT_MONITOR'][i][:5]) == "ft11:"):
				df_exec['RESULT_MONITOR'][i] = df_exec['RESULT_MONITOR'][i][5:]
				
			elif ((df_exec['RESULT_MONITOR'][i][:5]) == "fs10:" or (df_exec['RESULT_MONITOR'][i][:5]) == "fs11:"):
				df_exec['RESULT_MONITOR'][i] = df_exec['RESULT_MONITOR'][i][5:]
				
			elif (df_exec['RESULT_MONITOR'].loc[i][:3] == "rm:"):
				df_exec = df_exec.drop(i)
			else:
				df_exec['RESULT_MONITOR'][i] = df_exec['RESULT_MONITOR'][i][3:]
		df_exec = df_exec.reset_index(drop=True)

		df_exec['PC'] = df_exec['PC'].apply(lambda x: '0x' + x.zfill(8))
		df_exec['RESULT_MONITOR'] = df_exec['RESULT_MONITOR'].str.replace(":","")
		df_exec['INSTR_RES_MON'] = df_exec['INSTR_RES_MON'].apply(lambda x1: '0x' + x1.zfill(8))
		df_exec['RESULT_MONITOR'] = df_exec['RESULT_MONITOR'].apply(lambda x2: '0x' + x2.zfill(8))

		df_exec = df_exec.drop('NBL', axis=1)
		df_exec = df_exec.reset_index(drop=True)

		removed_PC = []
		removed_INSTR = []
		removed_RESULT = []
		removed_symbol = []

		indexes_to_remove = []
		for i in range(len(df_exec['RESULT_MONITOR'])):
		    if (df_exec['SYMBOL'][i] == 'nbL+1' or (df_exec['SYMBOL'][i] == 'nbD+1' and df_exec['SYMBOL'][i] != 'nbL')):
		        indexes_to_remove.append(i)
		        removed_PC.append(df_exec['PC'][i])
		        removed_INSTR.append(df_exec['INSTR_RES_MON'][i])
		        removed_RESULT.append(df_exec['RESULT_MONITOR'][i])
		        removed_symbol.append(df_exec['SYMBOL'][i])

		df_exec = df_exec.drop(indexes_to_remove)
		df_exec = df_exec.reset_index(drop=True)
				
		result_df = pd.DataFrame({'PC': removed_PC,
		'INSTR': removed_INSTR,
		'RESULT': removed_RESULT,
		'SYMBOL': removed_symbol})

		df_exec = df_exec.reset_index(drop=True)

		df_exec.to_csv("RESULT_MONITOR.csv",index=False)
		df_exec = df_exec.drop('SYMBOL', axis=1)
		df_exec = df_exec.reset_index(drop=True)
		filename = 'removed_data.csv'
		result_df.to_csv(filename, index=False)
