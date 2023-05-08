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


import pyuvm
import logging
from pyuvm import *

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge ,Timer,RisingEdge,ClockCycles

class Sequencer(uvm_component):
	
	def build_phase(self):
		self.count = 0
		self.Generator=ConfigDB().get(self,"","GENR")
		self.pp_Driver = uvm_blocking_put_port("pp_Driver",self)
		self.pp_Monitor = uvm_put_port("pp_Monitor",self)
		self.bfm=ConfigDB().get(self,"","bfm")
	
		
	async def run_phase(self):
		self.raise_objection()
		self.logger.info("**********Sequencer Execution**********") 
		GEN_PC = self.Generator.listpc
		GEN_DATA = self.Generator.listcounter
		self.logger.info("Instruction & Data is dispatch to Driver (***Sequencer***)")
		while (self.count < len(GEN_PC)):
			cmd_instr = (self.Generator.listpc[self.count],self.Generator.hex_listins[self.count])
			await self.pp_Driver.put(cmd_instr)
			await self.pp_Monitor.put(cmd_instr)
			self.count = self.count + 1
		self.count = 0
		#self.logger.info("Data is dispatch to Driver (***Sequencer***)")	
		while (self.count < len(GEN_DATA)) :
	
			cmd_data = (self.Generator.listcounter[self.count],self.Generator.listdata[self.count])
			await self.pp_Driver.put(cmd_data)
			self.count = self.count + 1
			
		cmd_instr = ("0xFFFFFFFF","0xFFFFFFFF")
		await self.pp_Driver.put(cmd_instr)
		self.drop_objection()

