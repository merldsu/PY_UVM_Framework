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

def get_int(signal):
	try:
		sig = int(signal.value)
	except ValueError:
		sig = 0
	return sig
	
class MONITOR(uvm_component):

	def build_phase(self):
		
		
		
		self.bfm=ConfigDB().get(self,"","bfm")
		self.gp_Sequencer = uvm_blocking_get_port("gp_Sequencer",self)
		#self.gp_drive = uvm_blocking_get_port("gp_drive",self)
		
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


